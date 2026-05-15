"""
Unit tests for drift detection module.
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from parity.drift_detection import DriftDetector, RunRecord


class TestDriftDetection:
    """Test suite for drift detection functionality."""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        yield db_path
        # Cleanup
        Path(db_path).unlink(missing_ok=True)
    
    @pytest.fixture
    def detector(self, temp_db):
        """Create a DriftDetector instance with temporary database."""
        return DriftDetector(db_path=temp_db)
    
    @pytest.fixture
    def sample_scores(self):
        """Sample function scores for testing."""
        return [
            {
                "function": "Domestic Wire Transfer",
                "parity_rate_pct": 100.0,
                "total_transactions": 80,
                "anomaly_count": 0,
                "avg_fee_diff_usd": 0.0001,
                "verdict": "SAFE_TO_CUT"
            },
            {
                "function": "International Wire Transfer",
                "parity_rate_pct": 0.0,
                "total_transactions": 80,
                "anomaly_count": 15,
                "avg_fee_diff_usd": 794.50,
                "verdict": "DO_NOT_CUT"
            }
        ]
    
    def test_detector_initialization(self, detector):
        """Test DriftDetector initializes correctly."""
        assert detector is not None
        assert Path(detector.db_path).exists()
    
    def test_record_run(self, detector, sample_scores):
        """Test recording a run to history."""
        detector.record_run(
            run_id="test_run_001",
            tenant_id="tier2_regional",
            scores=sample_scores
        )
        
        # Verify records were created
        history = detector.get_history("Domestic Wire Transfer", "tier2_regional")
        assert len(history) == 1
        assert history[0].run_id == "test_run_001"
        assert history[0].function_name == "Domestic Wire Transfer"
        assert history[0].parity_rate_pct == 100.0
    
    def test_get_history_empty(self, detector):
        """Test getting history when no runs exist."""
        history = detector.get_history("Nonexistent Function", "tier2_regional")
        assert len(history) == 0
    
    def test_get_history_with_limit(self, detector, sample_scores):
        """Test getting history with limit."""
        # Record multiple runs
        for i in range(10):
            detector.record_run(
                run_id=f"test_run_{i:03d}",
                tenant_id="tier2_regional",
                scores=sample_scores
            )
        
        # Get limited history
        history = detector.get_history("Domestic Wire Transfer", "tier2_regional", limit=5)
        assert len(history) == 5
    
    def test_get_history_tenant_filter(self, detector, sample_scores):
        """Test getting history filtered by tenant."""
        # Record runs for different tenants
        detector.record_run("run_tier1", "tier1_global", sample_scores)
        detector.record_run("run_tier2", "tier2_regional", sample_scores)
        
        # Get history for specific tenant
        history_tier1 = detector.get_history("Domestic Wire Transfer", "tier1_global")
        history_tier2 = detector.get_history("Domestic Wire Transfer", "tier2_regional")
        
        assert len(history_tier1) == 1
        assert len(history_tier2) == 1
        assert history_tier1[0].tenant_id == "tier1_global"
        assert history_tier2[0].tenant_id == "tier2_regional"
    
    def test_cusum_detect_insufficient_data(self, detector):
        """Test CUSUM detection with insufficient data."""
        result = detector.cusum_detect("Domestic Wire Transfer", "tier2_regional")
        
        assert result["drift_detected"] is False
        assert "Insufficient history" in result["reason"]
        assert result["runs_analyzed"] == 0
    
    def test_cusum_detect_no_drift(self, detector, sample_scores):
        """Test CUSUM detection when no drift exists."""
        # Record 10 runs with stable parity
        for i in range(10):
            scores = [{
                "function": "Domestic Wire Transfer",
                "parity_rate_pct": 95.0 + (i % 3),  # 95-97% variation
                "total_transactions": 80,
                "anomaly_count": 0,
                "avg_fee_diff_usd": 0.0001,
                "verdict": "SAFE_TO_CUT"
            }]
            detector.record_run(f"run_{i:03d}", "tier2_regional", scores)
        
        result = detector.cusum_detect("Domestic Wire Transfer", "tier2_regional", target_rate=95.0)
        
        assert result["drift_detected"] is False
        assert result["cusum_value"] < 5.0
        assert result["runs_analyzed"] >= 5
    
    def test_cusum_detect_with_drift(self, detector):
        """Test CUSUM detection when drift exists."""
        # Record runs with degrading parity
        for i in range(10):
            parity = 95.0 - (i * 2.0)  # Degrading from 95% to 77%
            scores = [{
                "function": "Domestic Wire Transfer",
                "parity_rate_pct": parity,
                "total_transactions": 80,
                "anomaly_count": 0,
                "avg_fee_diff_usd": 0.0001,
                "verdict": "SAFE_TO_CUT" if parity > 90 else "HOLD_INVESTIGATE"
            }]
            detector.record_run(f"run_{i:03d}", "tier2_regional", scores)
        
        result = detector.cusum_detect("Domestic Wire Transfer", "tier2_regional", target_rate=95.0, threshold=5.0)
        
        assert result["drift_detected"] is True
        assert result["cusum_value"] > 5.0
        assert result["severity"] in ["MEDIUM", "HIGH"]
    
    def test_ewma_detect_insufficient_data(self, detector):
        """Test EWMA detection with insufficient data."""
        result = detector.ewma_detect("Domestic Wire Transfer", "tier2_regional")
        
        assert result["drift_detected"] is False
        assert "Insufficient history" in result["reason"]
    
    def test_ewma_detect_stable(self, detector):
        """Test EWMA detection with stable parity."""
        # Record runs with stable parity
        for i in range(10):
            scores = [{
                "function": "Domestic Wire Transfer",
                "parity_rate_pct": 95.0,
                "total_transactions": 80,
                "anomaly_count": 0,
                "avg_fee_diff_usd": 0.0001,
                "verdict": "SAFE_TO_CUT"
            }]
            detector.record_run(f"run_{i:03d}", "tier2_regional", scores)
        
        result = detector.ewma_detect("Domestic Wire Transfer", "tier2_regional")

        assert not result["drift_detected"]
        assert 94.0 < result["ewma_value"] < 96.0
    
    def test_get_drift_summary_insufficient_data(self, detector):
        """Test drift summary with insufficient data."""
        summary = detector.get_drift_summary("Domestic Wire Transfer", "tier2_regional")
        
        assert summary["drift_detected"] is False
        assert summary["total_runs"] < 5
        assert summary["trend"] == "INSUFFICIENT_DATA"
    
    def test_get_drift_summary_stable(self, detector):
        """Test drift summary with stable parity."""
        # Record stable runs
        for i in range(10):
            scores = [{
                "function": "Domestic Wire Transfer",
                "parity_rate_pct": 95.0,
                "total_transactions": 80,
                "anomaly_count": 0,
                "avg_fee_diff_usd": 0.0001,
                "verdict": "SAFE_TO_CUT"
            }]
            detector.record_run(f"run_{i:03d}", "tier2_regional", scores)
        
        summary = detector.get_drift_summary("Domestic Wire Transfer", "tier2_regional")

        assert not summary["drift_detected"]
        assert summary["trend"] == "STABLE"
        assert "No drift detected" in summary["recommendation"]
    
    def test_get_drift_summary_degrading(self, detector):
        """Test drift summary with degrading trend."""
        # Record degrading runs
        for i in range(10):
            parity = 95.0 - (i * 1.5)  # Degrading
            scores = [{
                "function": "Domestic Wire Transfer",
                "parity_rate_pct": parity,
                "total_transactions": 80,
                "anomaly_count": 0,
                "avg_fee_diff_usd": 0.0001,
                "verdict": "SAFE_TO_CUT" if parity > 90 else "HOLD_INVESTIGATE"
            }]
            detector.record_run(f"run_{i:03d}", "tier2_regional", scores)
        
        summary = detector.get_drift_summary("Domestic Wire Transfer", "tier2_regional")
        
        assert summary["trend"] == "DEGRADING"
        assert len(summary["recent_history"]) > 0
    
    def test_get_drift_summary_improving(self, detector):
        """Test drift summary with improving trend."""
        # Record improving runs
        for i in range(10):
            parity = 85.0 + (i * 1.5)  # Improving
            scores = [{
                "function": "Domestic Wire Transfer",
                "parity_rate_pct": parity,
                "total_transactions": 80,
                "anomaly_count": 0,
                "avg_fee_diff_usd": 0.0001,
                "verdict": "HOLD_INVESTIGATE" if parity < 90 else "SAFE_TO_CUT"
            }]
            detector.record_run(f"run_{i:03d}", "tier2_regional", scores)
        
        summary = detector.get_drift_summary("Domestic Wire Transfer", "tier2_regional")
        
        assert summary["trend"] == "IMPROVING"
    
    def test_run_record_to_dict(self):
        """Test RunRecord to_dict conversion."""
        record = RunRecord(
            run_id="test_001",
            timestamp=datetime.now(timezone.utc),
            tenant_id="tier2_regional",
            function_name="Domestic Wire Transfer",
            parity_rate_pct=95.0,
            total_transactions=80,
            anomaly_count=0,
            avg_fee_diff_usd=0.0001,
            verdict="SAFE_TO_CUT"
        )
        
        record_dict = record.to_dict()
        
        assert isinstance(record_dict, dict)
        assert record_dict["run_id"] == "test_001"
        assert record_dict["tenant_id"] == "tier2_regional"
        assert record_dict["parity_rate_pct"] == 95.0
        assert "timestamp" in record_dict
    
    def test_multiple_functions_tracking(self, detector):
        """Test tracking multiple functions independently."""
        scores = [
            {
                "function": "Domestic Wire Transfer",
                "parity_rate_pct": 100.0,
                "total_transactions": 80,
                "anomaly_count": 0,
                "avg_fee_diff_usd": 0.0001,
                "verdict": "SAFE_TO_CUT"
            },
            {
                "function": "International Wire Transfer",
                "parity_rate_pct": 50.0,
                "total_transactions": 80,
                "anomaly_count": 10,
                "avg_fee_diff_usd": 500.0,
                "verdict": "DO_NOT_CUT"
            }
        ]
        
        detector.record_run("test_run", "tier2_regional", scores)
        
        domestic_history = detector.get_history("Domestic Wire Transfer", "tier2_regional")
        intl_history = detector.get_history("International Wire Transfer", "tier2_regional")
        
        assert len(domestic_history) == 1
        assert len(intl_history) == 1
        assert domestic_history[0].parity_rate_pct == 100.0
        assert intl_history[0].parity_rate_pct == 50.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
