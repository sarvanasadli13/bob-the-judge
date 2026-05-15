"""
Drift detection for monitoring parity degradation over time.

Implements statistical process control (SPC) methods:
- CUSUM (Cumulative Sum) for detecting sustained shifts
- EWMA (Exponentially Weighted Moving Average) for trend detection
- Run history tracking with SQLite persistence

Regulatory Justification:
- FFIEC: "Ongoing monitoring of operational risk indicators"
- Basel III: "Continuous assessment of operational risk exposure"
- PSD2: "Regular monitoring of payment service quality"
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import json


@dataclass
class RunRecord:
    """Single analysis run record for drift tracking."""
    run_id: str
    timestamp: datetime
    tenant_id: str
    function_name: str
    parity_rate_pct: float
    total_transactions: int
    anomaly_count: int
    avg_fee_diff_usd: float
    verdict: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        d = asdict(self)
        d['timestamp'] = self.timestamp.isoformat()
        return d


class DriftDetector:
    """
    Detects drift in parity rates using statistical process control methods.
    
    Tracks historical runs and flags when parity degrades beyond expected variation.
    """
    
    def __init__(self, db_path: str = "data/run_history.db"):
        """
        Initialize drift detector with SQLite database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS run_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                tenant_id TEXT NOT NULL,
                function_name TEXT NOT NULL,
                parity_rate_pct REAL NOT NULL,
                total_transactions INTEGER NOT NULL,
                anomaly_count INTEGER NOT NULL,
                avg_fee_diff_usd REAL NOT NULL,
                verdict TEXT NOT NULL,
                UNIQUE(run_id, function_name, tenant_id)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_function_time 
            ON run_history(function_name, timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tenant_function 
            ON run_history(tenant_id, function_name)
        """)
        
        conn.commit()
        conn.close()
    
    def record_run(self, run_id: str, tenant_id: str, scores: List[dict]):
        """
        Record a complete analysis run to history.
        
        Args:
            run_id: Unique identifier for this run
            tenant_id: Tenant profile used for analysis
            scores: List of function scores from scoring module
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        for score in scores:
            cursor.execute("""
                INSERT INTO run_history 
                (run_id, timestamp, tenant_id, function_name, parity_rate_pct, 
                 total_transactions, anomaly_count, avg_fee_diff_usd, verdict)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_id,
                timestamp,
                tenant_id,
                score['function'],
                score['parity_rate_pct'],
                score['total_transactions'],
                score.get('anomaly_count', 0),
                score['avg_fee_diff_usd'],
                score['verdict']
            ))
        
        conn.commit()
        conn.close()
    
    def get_history(self, function_name: str, tenant_id: Optional[str] = None, 
                    limit: int = 100) -> List[RunRecord]:
        """
        Retrieve historical runs for a function.
        
        Args:
            function_name: Payment function to query
            tenant_id: Optional tenant filter
            limit: Maximum number of records to return
        
        Returns:
            List of RunRecord objects, newest first
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cols = "run_id, timestamp, tenant_id, function_name, parity_rate_pct, total_transactions, anomaly_count, avg_fee_diff_usd, verdict"
        if tenant_id:
            cursor.execute(f"""
                SELECT {cols} FROM run_history
                WHERE function_name = ? AND tenant_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (function_name, tenant_id, limit))
        else:
            cursor.execute(f"""
                SELECT {cols} FROM run_history
                WHERE function_name = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (function_name, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        records = []
        for row in rows:
            records.append(RunRecord(
                run_id=row[0],
                timestamp=datetime.fromisoformat(row[1]),
                tenant_id=row[2],
                function_name=row[3],
                parity_rate_pct=row[4],
                total_transactions=row[5],
                anomaly_count=row[6],
                avg_fee_diff_usd=row[7],
                verdict=row[8]
            ))
        
        return records
    
    def cusum_detect(self, function_name: str, tenant_id: str, 
                     target_rate: float = 95.0, threshold: float = 5.0) -> Dict:
        """
        CUSUM (Cumulative Sum) drift detection.
        
        Detects sustained shifts in parity rate. More sensitive to gradual drift
        than simple threshold checks.
        
        Regulatory Basis:
        - FFIEC: "Early warning indicators for operational risk"
        - Basel III: "Timely identification of emerging risks"
        
        Args:
            function_name: Payment function to analyze
            tenant_id: Tenant profile for context
            target_rate: Expected parity rate (default 95%)
            threshold: CUSUM threshold for alarm (default 5.0)
        
        Returns:
            Dictionary with CUSUM statistics and drift flag
        """
        history = self.get_history(function_name, tenant_id, limit=50)
        
        if len(history) < 5:
            return {
                "drift_detected": False,
                "reason": "Insufficient history (need ≥5 runs)",
                "cusum_value": 0.0,
                "runs_analyzed": len(history)
            }
        
        # Calculate CUSUM (cumulative deviations from target)
        cusum = 0.0
        max_cusum = 0.0
        
        for record in reversed(history):  # Oldest to newest
            deviation = target_rate - record.parity_rate_pct
            cusum = max(0, cusum + deviation)  # One-sided CUSUM (detect degradation)
            max_cusum = max(max_cusum, cusum)
        
        drift_detected = cusum > threshold
        
        return {
            "drift_detected": drift_detected,
            "cusum_value": cusum,
            "max_cusum": max_cusum,
            "threshold": threshold,
            "runs_analyzed": len(history),
            "current_rate": history[0].parity_rate_pct if history else 0.0,
            "target_rate": target_rate,
            "severity": "HIGH" if cusum > threshold * 2 else "MEDIUM" if drift_detected else "LOW"
        }
    
    def ewma_detect(self, function_name: str, tenant_id: str, 
                    lambda_param: float = 0.2, control_limit: float = 3.0) -> Dict:
        """
        EWMA (Exponentially Weighted Moving Average) drift detection.
        
        Gives more weight to recent observations while considering history.
        Good for detecting both gradual and sudden shifts.
        
        Regulatory Basis:
        - Basel III: "Weighted historical data for risk assessment"
        - FFIEC: "Trend analysis for operational metrics"
        
        Args:
            function_name: Payment function to analyze
            tenant_id: Tenant profile for context
            lambda_param: Smoothing parameter (0-1, default 0.2)
            control_limit: Number of standard deviations for alarm (default 3.0)
        
        Returns:
            Dictionary with EWMA statistics and drift flag
        """
        history = self.get_history(function_name, tenant_id, limit=50)
        
        if len(history) < 5:
            return {
                "drift_detected": False,
                "reason": "Insufficient history (need ≥5 runs)",
                "ewma_value": 0.0,
                "runs_analyzed": len(history)
            }
        
        # Calculate EWMA
        rates = [r.parity_rate_pct for r in reversed(history)]
        ewma = rates[0]  # Initialize with first observation
        
        for rate in rates[1:]:
            ewma = lambda_param * rate + (1 - lambda_param) * ewma
        
        # Calculate control limits
        import numpy as np
        mean_rate = np.mean(rates)
        std_rate = np.std(rates)
        
        # EWMA standard deviation
        ewma_std = std_rate * np.sqrt(lambda_param / (2 - lambda_param))
        
        lower_limit = mean_rate - control_limit * ewma_std
        upper_limit = mean_rate + control_limit * ewma_std
        
        drift_detected = ewma < lower_limit or ewma > upper_limit
        
        return {
            "drift_detected": drift_detected,
            "ewma_value": ewma,
            "mean_rate": mean_rate,
            "std_rate": std_rate,
            "lower_limit": lower_limit,
            "upper_limit": upper_limit,
            "control_limit_sigma": control_limit,
            "runs_analyzed": len(history),
            "current_rate": history[0].parity_rate_pct if history else 0.0,
            "severity": "HIGH" if abs(ewma - mean_rate) > 2 * control_limit * ewma_std else "MEDIUM" if drift_detected else "LOW"
        }
    
    def get_drift_summary(self, function_name: str, tenant_id: str) -> Dict:
        """
        Get comprehensive drift analysis combining multiple methods.
        
        Args:
            function_name: Payment function to analyze
            tenant_id: Tenant profile for context
        
        Returns:
            Dictionary with all drift detection results and consensus
        """
        cusum = self.cusum_detect(function_name, tenant_id)
        ewma = self.ewma_detect(function_name, tenant_id)
        history = self.get_history(function_name, tenant_id, limit=10)
        
        # Consensus: drift if either method detects it
        drift_detected = cusum.get("drift_detected", False) or ewma.get("drift_detected", False)
        
        # Calculate trend (improving/degrading/stable)
        if len(history) >= 3:
            recent_rates = [h.parity_rate_pct for h in history[:3]]
            older_rates = [h.parity_rate_pct for h in history[3:6]] if len(history) >= 6 else recent_rates
            
            recent_avg = sum(recent_rates) / len(recent_rates)
            older_avg = sum(older_rates) / len(older_rates)
            
            if recent_avg < older_avg - 2.0:
                trend = "DEGRADING"
            elif recent_avg > older_avg + 2.0:
                trend = "IMPROVING"
            else:
                trend = "STABLE"
        else:
            trend = "INSUFFICIENT_DATA"
        
        return {
            "function_name": function_name,
            "tenant_id": tenant_id,
            "drift_detected": drift_detected,
            "trend": trend,
            "cusum": cusum,
            "ewma": ewma,
            "recent_history": [h.to_dict() for h in history[:5]],
            "total_runs": len(history),
            "recommendation": self._get_recommendation(drift_detected, trend, cusum, ewma)
        }
    
    def _get_recommendation(self, drift_detected: bool, trend: str, 
                           cusum: Dict, ewma: Dict) -> str:
        """Generate actionable recommendation based on drift analysis."""
        if not drift_detected:
            return "No drift detected. Continue monitoring."
        
        if trend == "DEGRADING":
            severity = max(
                ["LOW", "MEDIUM", "HIGH"].index(cusum.get("severity", "LOW")),
                ["LOW", "MEDIUM", "HIGH"].index(ewma.get("severity", "LOW"))
            )
            severity_label = ["LOW", "MEDIUM", "HIGH"][severity]
            
            if severity_label == "HIGH":
                return "URGENT: Significant parity degradation detected. Investigate immediately and consider blocking cutover."
            elif severity_label == "MEDIUM":
                return "WARNING: Parity trending downward. Increase monitoring frequency and investigate root cause."
            else:
                return "CAUTION: Minor parity variation detected. Monitor next few runs closely."
        
        return "Drift detected but trend unclear. Continue monitoring and gather more data."

# Made with Bob
