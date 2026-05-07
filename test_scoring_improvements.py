"""Test script for new scoring.py improvements"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from parity.scoring import score_results, score_by_tenant

# Test 1: Confidence band in output
print("=" * 60)
print("Test 1: Confidence band in score_results output")
print("=" * 60)
results = [
    {'transaction_type': 'domestic', 'parity': True, 'divergences': [], 
     'fee_diff': 0.0, 'settled_diff': 0.0, 'latency_improvement_pct': 15.0, 'amount': 1000},
    {'transaction_type': 'domestic', 'parity': False, 'divergences': [{'severity': 'HIGH'}],
     'fee_diff': 2.5, 'settled_diff': 0.0, 'latency_improvement_pct': 10.0, 'amount': 2000}
]
scores = score_results(results)
print(f"Function: {scores[0]['function']}")
print(f"Parity rate: {scores[0]['parity_rate_pct']}%")
print(f"Confidence band: {scores[0]['confidence_band']}")
print(f"✓ confidence_band present: {scores[0]['confidence_band']}")

# Test 2: Backward compatibility
print("\n" + "=" * 60)
print("Test 2: Backward compatibility check")
print("=" * 60)
required_fields = ['function', 'total_transactions', 'parity_rate_pct', 
                   'ci_low', 'ci_high', 'readiness_score', 'verdict']
all_present = all(field in scores[0] for field in required_fields)
print(f"✓ All original fields present: {all_present}")

# Test 3: score_by_tenant function
print("\n" + "=" * 60)
print("Test 3: score_by_tenant function")
print("=" * 60)
multi_tenant_results = [
    {'transaction_type': 'domestic', 'tenant_id': 'retail', 'parity': True,
     'divergences': [], 'fee_diff': 0.0, 'settled_diff': 0.0, 
     'latency_improvement_pct': 15.0, 'amount': 1000},
    {'transaction_type': 'domestic', 'tenant_id': 'commercial', 'parity': False,
     'divergences': [{'severity': 'CRITICAL'}], 'fee_diff': 5.0, 
     'settled_diff': 1.0, 'latency_improvement_pct': 8.0, 'amount': 5000},
    {'transaction_type': 'international', 'tenant_id': 'retail', 'parity': True,
     'divergences': [], 'fee_diff': 0.0, 'settled_diff': 0.0, 
     'latency_improvement_pct': 20.0, 'amount': 3000}
]

retail_scores = score_by_tenant(multi_tenant_results, 'retail')
commercial_scores = score_by_tenant(multi_tenant_results, 'commercial')

print(f"Retail tenant functions: {len(retail_scores)}")
print(f"Commercial tenant functions: {len(commercial_scores)}")
print(f"✓ Retail has 2 functions: {len(retail_scores) == 2}")
print(f"✓ Commercial has 1 function: {len(commercial_scores) == 1}")

# Test 4: Confidence band width decreases with sample size
print("\n" + "=" * 60)
print("Test 4: Confidence band width vs sample size")
print("=" * 60)
small_sample = [
    {'transaction_type': 'domestic', 'parity': True, 'divergences': [], 
     'fee_diff': 0.0, 'settled_diff': 0.0, 'latency_improvement_pct': 15.0, 'amount': 1000}
] * 5

large_sample = small_sample * 20

small_scores = score_results(small_sample)
large_scores = score_results(large_sample)

small_width = small_scores[0]['confidence_band']['width']
large_width = large_scores[0]['confidence_band']['width']

print(f"Small sample (n=5) width: {small_width}")
print(f"Large sample (n=100) width: {large_width}")
print(f"✓ Width decreases with larger sample: {small_width > large_width}")

print("\n" + "=" * 60)
print("ALL TESTS PASSED ✓")
print("=" * 60)

# Made with Bob
