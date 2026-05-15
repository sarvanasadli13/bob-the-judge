"""
Unit tests for tenant configuration module.
"""

from decimal import Decimal

import pytest

from parity.tenant_config import (
    TenantProfile,
    get_default_tenant,
    list_tenants,
    load_tenant,
)


class TestTenantConfig:
    """Test suite for tenant configuration functionality."""

    def test_list_tenants(self):
        """list_tenants returns the 4 reference profile IDs."""
        tenants = list_tenants()

        assert isinstance(tenants, list)
        assert len(tenants) >= 4
        for tid in ("tier1_global", "tier2_regional", "community_bank", "demo_default"):
            assert tid in tenants

    def test_load_tier1_global(self):
        """Tier-1 global profile: strictest tolerances."""
        tenant = load_tenant("tier1_global")

        assert isinstance(tenant, TenantProfile)
        assert tenant.tenant_id == "tier1_global"
        assert tenant.tier == "tier1"
        assert tenant.parity_threshold_pct == 99.0
        assert tenant.fee_tolerance_usd == Decimal("0.01")
        assert tenant.anomaly_sigma_threshold == 1.5
        assert "Large Bank" in tenant.ffiec_category
        assert tenant.basel_operational_risk_weight == 0.12

    def test_load_tier2_regional(self):
        """Tier-2 regional profile: standard Wilson 95% CI thresholds."""
        tenant = load_tenant("tier2_regional")

        assert tenant.tenant_id == "tier2_regional"
        assert tenant.tier == "tier2"
        assert tenant.parity_threshold_pct == 95.0
        assert tenant.fee_tolerance_usd == Decimal("0.02")
        assert tenant.anomaly_sigma_threshold == 2.0
        assert "Regional Bank" in tenant.ffiec_category
        assert tenant.basel_operational_risk_weight == 0.15

    def test_load_community_bank(self):
        """Community bank profile: relaxed thresholds for smaller institutions."""
        tenant = load_tenant("community_bank")

        assert tenant.tenant_id == "community_bank"
        assert tenant.tier == "community"
        assert tenant.parity_threshold_pct == 90.0
        assert tenant.fee_tolerance_usd == Decimal("0.05")
        assert tenant.anomaly_sigma_threshold == 2.5
        assert "Community Bank" in tenant.ffiec_category

    def test_load_demo_default(self):
        """Demo profile: backward-compatible tier-2 defaults."""
        tenant = load_tenant("demo_default")

        assert tenant.tenant_id == "demo_default"
        assert tenant.parity_threshold_pct == 95.0
        assert tenant.fee_tolerance_usd == Decimal("0.02")
        assert tenant.anomaly_sigma_threshold == 2.0

    def test_get_default_tenant(self):
        """Default tenant resolves to demo_default."""
        tenant = get_default_tenant()

        assert isinstance(tenant, TenantProfile)
        assert tenant.tenant_id == "demo_default"

    def test_load_invalid_tenant(self):
        """Unknown tenant ID raises ValueError."""
        with pytest.raises(ValueError, match="Tenant 'invalid_tenant' not found"):
            load_tenant("invalid_tenant")

    def test_tenant_to_dict(self):
        """to_dict serialises Decimal fields as floats for JSON."""
        tenant = load_tenant("tier1_global")
        d = tenant.to_dict()

        assert isinstance(d, dict)
        assert d["tenant_id"] == "tier1_global"
        assert d["parity_threshold_pct"] == 99.0
        assert d["fee_tolerance_usd"] == 0.01
        assert "ffiec_category" in d
        assert "basel_operational_risk_weight" in d

    def test_tenant_thresholds_ordering(self):
        """Tier 1 < Tier 2 < Community in tolerance (stricter → looser)."""
        tier1 = load_tenant("tier1_global")
        tier2 = load_tenant("tier2_regional")
        community = load_tenant("community_bank")

        assert tier1.parity_threshold_pct > tier2.parity_threshold_pct
        assert tier2.parity_threshold_pct > community.parity_threshold_pct

        assert tier1.fee_tolerance_usd < tier2.fee_tolerance_usd
        assert tier2.fee_tolerance_usd < community.fee_tolerance_usd

        assert tier1.anomaly_sigma_threshold < tier2.anomaly_sigma_threshold
        assert tier2.anomaly_sigma_threshold <= community.anomaly_sigma_threshold

    def test_psd2_jurisdiction_flags(self):
        """All profiles expose a boolean psd2_jurisdiction flag."""
        for tenant_id in list_tenants():
            tenant = load_tenant(tenant_id)
            assert isinstance(tenant.psd2_jurisdiction, bool)

    def test_requires_cto_signoff_flags(self):
        """All profiles expose a boolean requires_cto_signoff flag."""
        for tenant_id in list_tenants():
            tenant = load_tenant(tenant_id)
            assert isinstance(tenant.requires_cto_signoff, bool)

    def test_max_daily_exposure_positive(self):
        """Every profile has a positive max daily exposure cap."""
        for tenant_id in list_tenants():
            tenant = load_tenant(tenant_id)
            assert tenant.max_daily_exposure_usd > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
