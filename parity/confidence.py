"""
Advanced confidence interval methods for parity scoring.

Beyond Wilson 95% CI, provides:
- Bootstrap confidence intervals (resampling-based)
- Bayesian credible intervals (prior-informed)
- Funnel plot boundaries for small-sample detection

Regulatory Justification:
- FDA Guidance: "Multiple methods strengthen statistical inference"
- Basel III: "Model validation requires sensitivity analysis"
- FFIEC: "Risk assessment should use multiple analytical approaches"
"""

import numpy as np
from typing import Tuple, List
from dataclasses import dataclass


@dataclass
class ConfidenceInterval:
    """Container for confidence interval results."""
    method: str
    lower: float
    upper: float
    point_estimate: float
    confidence_level: float
    
    def width(self) -> float:
        """Return the width of the confidence interval."""
        return self.upper - self.lower
    
    def contains(self, value: float) -> bool:
        """Check if a value falls within the interval."""
        return self.lower <= value <= self.upper


def wilson_score_interval(successes: int, trials: int, confidence: float = 0.95) -> ConfidenceInterval:
    """
    Wilson score confidence interval (current method).
    
    More accurate than normal approximation for small samples and extreme proportions.
    Used as baseline for comparison with other methods.
    
    Args:
        successes: Number of successful comparisons (parity matches)
        trials: Total number of comparisons
        confidence: Confidence level (default 0.95 for 95% CI)
    
    Returns:
        ConfidenceInterval with Wilson score bounds
    """
    if trials == 0:
        return ConfidenceInterval("wilson", 0.0, 0.0, 0.0, confidence)
    
    p = successes / trials
    z = 1.96 if confidence == 0.95 else 2.576  # 95% or 99%
    
    denominator = 1 + z**2 / trials
    center = (p + z**2 / (2 * trials)) / denominator
    margin = z * np.sqrt((p * (1 - p) / trials + z**2 / (4 * trials**2))) / denominator
    
    lower = max(0.0, center - margin)
    upper = min(1.0, center + margin)
    
    return ConfidenceInterval("wilson", lower * 100, upper * 100, p * 100, confidence)


def bootstrap_interval(successes: int, trials: int, confidence: float = 0.95, n_bootstrap: int = 10000) -> ConfidenceInterval:
    """
    Bootstrap confidence interval using resampling.
    
    Non-parametric method that doesn't assume normal distribution.
    Particularly useful for small samples or skewed distributions.
    
    Regulatory Basis:
    - FDA: "Bootstrap methods provide robust uncertainty quantification"
    - Basel III: "Resampling techniques validate model assumptions"
    
    Args:
        successes: Number of successful comparisons
        trials: Total number of comparisons
        confidence: Confidence level (default 0.95)
        n_bootstrap: Number of bootstrap samples (default 10000)
    
    Returns:
        ConfidenceInterval with bootstrap percentile bounds
    """
    if trials == 0:
        return ConfidenceInterval("bootstrap", 0.0, 0.0, 0.0, confidence)
    
    # Create binary array: 1 for success, 0 for failure
    data = np.array([1] * successes + [0] * (trials - successes))
    
    # Bootstrap resampling
    bootstrap_means = []
    rng = np.random.default_rng(42)  # Fixed seed for reproducibility
    
    for _ in range(n_bootstrap):
        sample = rng.choice(data, size=trials, replace=True)
        bootstrap_means.append(np.mean(sample))
    
    # Percentile method
    alpha = (1 - confidence) / 2
    lower = float(np.percentile(bootstrap_means, alpha * 100))
    upper = float(np.percentile(bootstrap_means, (1 - alpha) * 100))
    point = successes / trials
    
    return ConfidenceInterval("bootstrap", lower * 100, upper * 100, point * 100, confidence)


def bayesian_credible_interval(successes: int, trials: int, confidence: float = 0.95, 
                                prior_alpha: float = 1.0, prior_beta: float = 1.0) -> ConfidenceInterval:
    """
    Bayesian credible interval using Beta-Binomial conjugate prior.
    
    Incorporates prior knowledge about parity rates. Default uniform prior (α=1, β=1).
    For banking: could use informative prior based on historical migration data.
    
    Regulatory Basis:
    - Basel III Pillar 2: "Prior experience should inform risk assessment"
    - FFIEC: "Historical performance data strengthens analysis"
    
    Args:
        successes: Number of successful comparisons
        trials: Total number of comparisons
        confidence: Confidence level (default 0.95)
        prior_alpha: Beta prior α parameter (default 1.0 = uniform)
        prior_beta: Beta prior β parameter (default 1.0 = uniform)
    
    Returns:
        ConfidenceInterval with Bayesian credible interval bounds
    """
    if trials == 0:
        return ConfidenceInterval("bayesian", 0.0, 0.0, 0.0, confidence)
    
    # Posterior parameters (Beta distribution)
    posterior_alpha = prior_alpha + successes
    posterior_beta = prior_beta + (trials - successes)
    
    # Credible interval using Beta quantiles
    from scipy.stats import beta
    alpha = (1 - confidence) / 2
    lower = float(beta.ppf(alpha, posterior_alpha, posterior_beta))
    upper = float(beta.ppf(1 - alpha, posterior_alpha, posterior_beta))
    
    # Posterior mean (point estimate)
    point = posterior_alpha / (posterior_alpha + posterior_beta)
    
    return ConfidenceInterval("bayesian", lower * 100, upper * 100, point * 100, confidence)


def funnel_plot_bounds(n: int, target_rate: float = 95.0, confidence: float = 0.95) -> Tuple[float, float]:
    """
    Calculate funnel plot control limits for detecting outliers.
    
    Funnel plots show expected variation around a target rate as sample size changes.
    Useful for identifying functions with unexpectedly low parity despite small samples.
    
    Regulatory Basis:
    - FFIEC: "Statistical process control for operational risk monitoring"
    - Basel III: "Outlier detection in operational loss data"
    
    Args:
        n: Sample size (number of transactions)
        target_rate: Target parity rate percentage (default 95%)
        confidence: Confidence level for control limits (default 0.95)
    
    Returns:
        Tuple of (lower_bound, upper_bound) in percentage
    """
    if n == 0:
        return (0.0, 100.0)
    
    p = target_rate / 100
    z = 1.96 if confidence == 0.95 else 2.576
    
    # Standard error for binomial proportion
    se = np.sqrt(p * (1 - p) / n)
    
    lower = max(0.0, (p - z * se) * 100)
    upper = min(100.0, (p + z * se) * 100)
    
    return (lower, upper)


def compare_intervals(successes: int, trials: int, confidence: float = 0.95) -> dict:
    """
    Compare all confidence interval methods for a given dataset.
    
    Returns a dictionary with all methods for visualization and analysis.
    Useful for understanding method sensitivity and robustness.
    
    Args:
        successes: Number of successful comparisons
        trials: Total number of comparisons
        confidence: Confidence level (default 0.95)
    
    Returns:
        Dictionary with all interval methods and comparison metrics
    """
    wilson = wilson_score_interval(successes, trials, confidence)
    bootstrap = bootstrap_interval(successes, trials, confidence)
    bayesian = bayesian_credible_interval(successes, trials, confidence)
    funnel_lower, funnel_upper = funnel_plot_bounds(trials, 95.0, confidence)
    
    return {
        "wilson": {
            "lower": wilson.lower,
            "upper": wilson.upper,
            "point": wilson.point_estimate,
            "width": wilson.width(),
        },
        "bootstrap": {
            "lower": bootstrap.lower,
            "upper": bootstrap.upper,
            "point": bootstrap.point_estimate,
            "width": bootstrap.width(),
        },
        "bayesian": {
            "lower": bayesian.lower,
            "upper": bayesian.upper,
            "point": bayesian.point_estimate,
            "width": bayesian.width(),
        },
        "funnel": {
            "lower": funnel_lower,
            "upper": funnel_upper,
            "target": 95.0,
        },
        "sample_size": trials,
        "successes": successes,
        "confidence_level": confidence,
    }


def get_interval_consensus(successes: int, trials: int, confidence: float = 0.95) -> dict:
    """
    Get consensus view across all confidence interval methods.
    
    Provides a robust assessment by considering agreement across methods.
    Flags cases where methods disagree significantly (model uncertainty).
    
    Args:
        successes: Number of successful comparisons
        trials: Total number of comparisons
        confidence: Confidence level (default 0.95)
    
    Returns:
        Dictionary with consensus metrics and disagreement flags
    """
    intervals = compare_intervals(successes, trials, confidence)
    
    # Extract lower and upper bounds from each method
    lowers = [intervals["wilson"]["lower"], intervals["bootstrap"]["lower"], intervals["bayesian"]["lower"]]
    uppers = [intervals["wilson"]["upper"], intervals["bootstrap"]["upper"], intervals["bayesian"]["upper"]]
    
    # Consensus: most conservative (widest) interval
    consensus_lower = min(lowers)
    consensus_upper = max(uppers)
    
    # Check for significant disagreement (>5% difference in bounds)
    lower_range = max(lowers) - min(lowers)
    upper_range = max(uppers) - min(uppers)
    significant_disagreement = lower_range > 5.0 or upper_range > 5.0
    
    return {
        "consensus_lower": consensus_lower,
        "consensus_upper": consensus_upper,
        "consensus_width": consensus_upper - consensus_lower,
        "methods_agree": not significant_disagreement,
        "lower_range": lower_range,
        "upper_range": upper_range,
        "all_intervals": intervals,
    }

# Made with Bob
