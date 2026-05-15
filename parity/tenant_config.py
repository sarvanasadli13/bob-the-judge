"""
Tenant-specific parity thresholds and regulatory requirements.

Enables different banks to use risk-appropriate tolerances based on:
- Institution size (FFIEC categorization)
- Regulatory requirements (Basel III, PSD2)
- Risk appetite and operational complexity

Regulatory Basis:
- FFIEC IT Handbook: "Risk management practices should be commensurate with 
  the size, complexity, and risk profile of the institution"
- Basel III Pillar 2: Supervisory review requires institution-specific risk assessment
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal
import json
from pathlib import Path


@dataclass
class TenantProfile:
    """
    Tenant-specific parity thresholds and regulatory requirements.
    Allows different banks to use risk-appropriate tolerances.
    """
    tenant_id: str
    name: str
    tier: Literal["tier1", "tier2", "community"]
    
    # Parity tolerances
    fee_tolerance_usd: Decimal
    amount_tolerance_usd: Decimal
    parity_threshold_pct: float  # Minimum parity rate for SAFE_TO_CUT
    
    # Anomaly detection
    anomaly_sigma_threshold: float  # Standard deviations for flagging
    
    # Regulatory context
    ffiec_category: str  # "Large Bank" / "Regional Bank" / "Community Bank"
    basel_operational_risk_weight: float  # 0.12 (12%) for tier1, 0.15 for tier2
    psd2_jurisdiction: bool
    
    # Risk appetite
    max_daily_exposure_usd: float
    requires_cto_signoff: bool
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization and API responses."""
        return {
            "tenant_id": self.tenant_id,
            "name": self.name,
            "tier": self.tier,
            "fee_tolerance_usd": float(self.fee_tolerance_usd),
            "amount_tolerance_usd": float(self.amount_tolerance_usd),
            "parity_threshold_pct": self.parity_threshold_pct,
            "anomaly_sigma_threshold": self.anomaly_sigma_threshold,
            "ffiec_category": self.ffiec_category,
            "basel_operational_risk_weight": self.basel_operational_risk_weight,
            "psd2_jurisdiction": self.psd2_jurisdiction,
            "max_daily_exposure_usd": self.max_daily_exposure_usd,
            "requires_cto_signoff": self.requires_cto_signoff,
        }


def load_tenant(tenant_id: str) -> TenantProfile:
    """
    Load tenant profile from config/tenants.json.
    
    Args:
        tenant_id: Unique tenant identifier (e.g., 'tier1_global', 'community_bank')
    
    Returns:
        TenantProfile with all configuration parameters
    
    Raises:
        ValueError: If tenant_id not found in configuration
        FileNotFoundError: If config/tenants.json doesn't exist
    """
    config_path = Path(__file__).parent.parent / "config" / "tenants.json"
    
    if not config_path.exists():
        raise FileNotFoundError(
            f"Tenant configuration not found at {config_path}. "
            "Please create config/tenants.json with tenant profiles."
        )
    
    with open(config_path) as f:
        tenants = json.load(f)
    
    if tenant_id not in tenants:
        available = ", ".join(tenants.keys())
        raise ValueError(
            f"Tenant '{tenant_id}' not found in config. "
            f"Available tenants: {available}"
        )
    
    data = tenants[tenant_id]
    return TenantProfile(
        tenant_id=tenant_id,
        name=data["name"],
        tier=data["tier"],
        fee_tolerance_usd=Decimal(str(data["fee_tolerance_usd"])),
        amount_tolerance_usd=Decimal(str(data["amount_tolerance_usd"])),
        parity_threshold_pct=data["parity_threshold_pct"],
        anomaly_sigma_threshold=data["anomaly_sigma_threshold"],
        ffiec_category=data["ffiec_category"],
        basel_operational_risk_weight=data["basel_operational_risk_weight"],
        psd2_jurisdiction=data["psd2_jurisdiction"],
        max_daily_exposure_usd=data["max_daily_exposure_usd"],
        requires_cto_signoff=data["requires_cto_signoff"],
    )


def list_tenants() -> list[str]:
    """
    List all available tenant profile IDs.

    Returns:
        List of tenant_id strings for each configured tenant
    """
    config_path = Path(__file__).parent.parent / "config" / "tenants.json"

    if not config_path.exists():
        return []

    with open(config_path) as f:
        tenants = json.load(f)

    return list(tenants.keys())


def get_default_tenant() -> TenantProfile:
    """
    Get default tenant profile for backward compatibility.
    Uses 'demo_default' if available, otherwise creates a standard tier2 profile.
    """
    try:
        return load_tenant("demo_default")
    except (FileNotFoundError, ValueError):
        # Fallback to hardcoded tier2 defaults
        return TenantProfile(
            tenant_id="default",
            name="Default Profile",
            tier="tier2",
            fee_tolerance_usd=Decimal("0.02"),
            amount_tolerance_usd=Decimal("0.05"),
            parity_threshold_pct=95.0,
            anomaly_sigma_threshold=2.0,
            ffiec_category="Regional Bank",
            basel_operational_risk_weight=0.15,
            psd2_jurisdiction=True,
            max_daily_exposure_usd=5000000.0,
            requires_cto_signoff=False,
        )

# Made with Bob
