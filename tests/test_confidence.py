"""
Unit tests for confidence interval module.
"""

import pytest
from parity.confidence import (
    wilson_score_interval,
    bootstrap_interval,
    bayesian_credible_interval,
    funnel_plot_bounds,
    compare_intervals,
    get_interval_consensus,
    ConfidenceInterval
)


class TestConfidenceIntervals:
    """Test suite for confidence interval calculations."""
    
    def test_wilson_score_perfect_parity(self):
        """Test Wilson score with 100% parity."""
        ci = wilson_score_interval(successes=100, trials=100, confidence=0.95)

        assert isinstance(ci, ConfidenceInterval)
        assert ci.method == "wilson"
        assert ci.point_estimate == 100.0
        assert ci.lower > 95.0  # Should be high but not 100
        assert ci.upper == pytest.approx(100.0)
        assert ci.confidence_level == 0.95
    
    def test_wilson_score_zero_parity(self):
        """Test Wilson score with 0% parity."""
        ci = wilson_score_interval(successes=0, trials=100, confidence=0.95)
        
        assert ci.point_estimate == 0.0
        assert ci.lower == 0.0
        assert ci.upper < 5.0  # Should be low but not 0
    
    def test_wilson_score_medium_parity(self):
        """Test Wilson score with 95% parity (lower bound near 88-89 for n=100)."""
        ci = wilson_score_interval(successes=95, trials=100, confidence=0.95)

        assert 85.0 < ci.lower < 95.0
        assert 95.0 < ci.upper < 100.0
        assert ci.point_estimate == 95.0
    
    def test_wilson_score_empty_sample(self):
        """Test Wilson score with zero trials."""
        ci = wilson_score_interval(successes=0, trials=0, confidence=0.95)
        
        assert ci.lower == 0.0
        assert ci.upper == 0.0
        assert ci.point_estimate == 0.0
    
    def test_bootstrap_interval_perfect_parity(self):
        """Test bootstrap interval with 100% parity."""
        ci = bootstrap_interval(successes=100, trials=100, confidence=0.95)
        
        assert isinstance(ci, ConfidenceInterval)
        assert ci.method == "bootstrap"
        assert ci.point_estimate == 100.0
        assert ci.lower > 90.0
        assert ci.upper == 100.0
    
    def test_bootstrap_interval_medium_parity(self):
        """Test bootstrap interval with 95% parity."""
        ci = bootstrap_interval(successes=95, trials=100, confidence=0.95, n_bootstrap=1000)
        
        assert 85.0 < ci.lower < 95.0
        assert 95.0 < ci.upper <= 100.0
        assert ci.point_estimate == 95.0
    
    def test_bootstrap_interval_reproducible(self):
        """Test bootstrap interval is reproducible with fixed seed."""
        ci1 = bootstrap_interval(successes=95, trials=100, confidence=0.95)
        ci2 = bootstrap_interval(successes=95, trials=100, confidence=0.95)
        
        # Should be identical due to fixed seed in implementation
        assert ci1.lower == ci2.lower
        assert ci1.upper == ci2.upper
    
    def test_bayesian_interval_uniform_prior(self):
        """Test Bayesian interval with uniform prior."""
        ci = bayesian_credible_interval(
            successes=95, trials=100, confidence=0.95,
            prior_alpha=1.0, prior_beta=1.0
        )
        
        assert isinstance(ci, ConfidenceInterval)
        assert ci.method == "bayesian"
        assert 85.0 < ci.lower < 95.0
        assert 95.0 < ci.upper < 100.0
    
    def test_bayesian_interval_informative_prior(self):
        """Test Bayesian interval with informative prior."""
        # Prior suggesting high parity (alpha=95, beta=5)
        ci = bayesian_credible_interval(
            successes=90, trials=100, confidence=0.95,
            prior_alpha=95.0, prior_beta=5.0
        )
        
        # Posterior should be influenced by strong prior
        assert ci.point_estimate > 0.90
    
    def test_funnel_plot_bounds_large_sample(self):
        """Test funnel plot bounds for large sample."""
        lower, upper = funnel_plot_bounds(n=1000, target_rate=95.0, confidence=0.95)
        
        assert isinstance(lower, float)
        assert isinstance(upper, float)
        assert lower < 95.0 < upper
        assert upper - lower < 5.0  # Narrow bounds for large sample
    
    def test_funnel_plot_bounds_small_sample(self):
        """Test funnel plot bounds for small sample."""
        lower, upper = funnel_plot_bounds(n=20, target_rate=95.0, confidence=0.95)
        
        assert lower < 95.0 < upper
        assert upper - lower > 10.0  # Wide bounds for small sample
    
    def test_funnel_plot_bounds_zero_sample(self):
        """Test funnel plot bounds with zero sample."""
        lower, upper = funnel_plot_bounds(n=0, target_rate=95.0, confidence=0.95)
        
        assert lower == 0.0
        assert upper == 100.0
    
    def test_compare_intervals_structure(self):
        """Test compare_intervals returns correct structure."""
        result = compare_intervals(successes=95, trials=100, confidence=0.95)
        
        assert isinstance(result, dict)
        assert "wilson" in result
        assert "bootstrap" in result
        assert "bayesian" in result
        assert "funnel" in result
        assert "sample_size" in result
        assert "successes" in result
        assert "confidence_level" in result
        
        # Check Wilson structure
        assert "lower" in result["wilson"]
        assert "upper" in result["wilson"]
        assert "point" in result["wilson"]
        assert "width" in result["wilson"]
    
    def test_compare_intervals_consistency(self):
        """Test that all methods give reasonable results."""
        result = compare_intervals(successes=95, trials=100, confidence=0.95)
        
        # All methods should have similar point estimates
        assert 94.0 < result["wilson"]["point"] < 96.0
        assert 94.0 < result["bootstrap"]["point"] < 96.0
        assert 94.0 < result["bayesian"]["point"] < 96.0
        
        # All lower bounds should be below point estimate
        assert result["wilson"]["lower"] < result["wilson"]["point"]
        assert result["bootstrap"]["lower"] < result["bootstrap"]["point"]
        assert result["bayesian"]["lower"] < result["bayesian"]["point"]
        
        # All upper bounds should be above point estimate
        assert result["wilson"]["upper"] > result["wilson"]["point"]
        assert result["bootstrap"]["upper"] > result["bootstrap"]["point"]
        assert result["bayesian"]["upper"] > result["bayesian"]["point"]
    
    def test_get_interval_consensus_agreement(self):
        """Test consensus when methods agree."""
        consensus = get_interval_consensus(successes=95, trials=100, confidence=0.95)
        
        assert isinstance(consensus, dict)
        assert "consensus_lower" in consensus
        assert "consensus_upper" in consensus
        assert "consensus_width" in consensus
        assert "methods_agree" in consensus
        assert "all_intervals" in consensus
        
        # Consensus should be most conservative (widest)
        assert consensus["consensus_lower"] <= consensus["all_intervals"]["wilson"]["lower"]
        assert consensus["consensus_upper"] >= consensus["all_intervals"]["wilson"]["upper"]
    
    def test_get_interval_consensus_disagreement(self):
        """Test consensus detection of disagreement."""
        # Small sample might cause disagreement
        consensus = get_interval_consensus(successes=9, trials=10, confidence=0.95)
        
        # Check that disagreement detection works
        assert isinstance(consensus["methods_agree"], bool)
        assert "lower_range" in consensus
        assert "upper_range" in consensus
    
    def test_confidence_interval_width(self):
        """Test ConfidenceInterval width calculation."""
        ci = ConfidenceInterval("test", 85.0, 95.0, 90.0, 0.95)
        
        assert ci.width() == 10.0
    
    def test_confidence_interval_contains(self):
        """Test ConfidenceInterval contains method."""
        ci = ConfidenceInterval("test", 85.0, 95.0, 90.0, 0.95)
        
        assert ci.contains(90.0)
        assert ci.contains(85.0)
        assert ci.contains(95.0)
        assert not ci.contains(84.9)
        assert not ci.contains(95.1)
    
    def test_wilson_vs_bootstrap_similarity(self):
        """Test that Wilson and Bootstrap give similar results for large samples."""
        wilson = wilson_score_interval(successes=950, trials=1000, confidence=0.95)
        bootstrap = bootstrap_interval(successes=950, trials=1000, confidence=0.95, n_bootstrap=5000)
        
        # Should be within 2% of each other for large samples
        assert abs(wilson.lower - bootstrap.lower) < 2.0
        assert abs(wilson.upper - bootstrap.upper) < 2.0
    
    def test_confidence_level_99(self):
        """Test 99% confidence level produces wider intervals."""
        ci_95 = wilson_score_interval(successes=95, trials=100, confidence=0.95)
        ci_99 = wilson_score_interval(successes=95, trials=100, confidence=0.99)
        
        # 99% CI should be wider than 95% CI
        assert ci_99.width() > ci_95.width()
        assert ci_99.lower < ci_95.lower
        assert ci_99.upper > ci_95.upper


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
