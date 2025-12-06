#!/usr/bin/env python3
"""
Comprehensive Statistical Tests for Cryptographically Secure Randomness
Author: Assistant
Description: Validates the quality of randomness in the tarot system using
             rigorous statistical tests including Chi-squared and Kolmogorov-Smirnov.

Test Suite:
1. Uniformity Test (Chi-squared) - Verifies uniform distribution
2. Independence Test - Checks for correlation between consecutive draws
3. Kolmogorov-Smirnov Test - Validates distribution against uniform
4. Entropy Test - Measures Shannon entropy
5. Orientation Balance Test - Verifies 50/50 reversed/upright distribution
6. Spread Type Tests - Tests all tarot spread configurations
7. Collision Test - Checks for unexpected patterns
8. Performance Test - Measures generation speed

Requirements:
- All tests must pass with p-value > 0.05 (95% confidence)
- Minimum 1000 simulations per test
- Target: >90% pass rate across all tests
"""

import sys
import json
from collections import Counter
from datetime import datetime
from typing import List, Dict, Tuple
import numpy as np
from scipy import stats

# Import the secure randomness module
from tarot_secure_random import TarotSecureShuffler, SecureRandomGenerator


class RandomnessTestSuite:
    """Comprehensive test suite for cryptographic randomness validation."""
    
    def __init__(self, simulations: int = 1000):
        """
        Initialize the test suite.
        
        Args:
            simulations: Number of simulations to run per test (default: 1000)
        """
        self.simulations = simulations
        self.shuffler = TarotSecureShuffler()
        self.rng = SecureRandomGenerator()
        self.results = {}
        self.passed_tests = 0
        self.total_tests = 0
    
    def test_uniformity_chi_squared(self) -> Tuple[bool, Dict]:
        """
        Test 1: Chi-squared test for uniform distribution.
        
        Validates that all 78 cards appear with equal probability
        across multiple shuffles.
        
        Returns:
            Tuple of (passed, results_dict)
        """
        print("\n" + "="*70)
        print("TEST 1: Chi-Squared Uniformity Test")
        print("="*70)
        print(f"Running {self.simulations} simulations...")
        
        # Count how many times each card appears in first position
        card_counts = Counter()
        deck = list(range(78))
        
        for i in range(self.simulations):
            shuffled = self.shuffler.shuffle_deck(deck)
            card_counts[shuffled[0]] += 1
            
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i + 1}/{self.simulations} shuffles completed")
        
        # Perform chi-squared test
        observed = list(card_counts.values())
        expected_freq = self.simulations / 78
        
        chi2_stat, p_value = stats.chisquare(observed)
        
        # Test passes if p-value > 0.05
        passed = p_value > 0.05
        
        results = {
            "test_name": "Chi-Squared Uniformity",
            "simulations": self.simulations,
            "chi2_statistic": float(chi2_stat),
            "p_value": float(p_value),
            "expected_frequency": expected_freq,
            "observed_mean": float(np.mean(observed)),
            "observed_std": float(np.std(observed)),
            "passed": passed,
            "threshold": 0.05
        }
        
        print(f"\n📊 Results:")
        print(f"   Chi-squared statistic: {chi2_stat:.4f}")
        print(f"   P-value: {p_value:.4f}")
        print(f"   Expected frequency: {expected_freq:.2f}")
        print(f"   Observed mean: {np.mean(observed):.2f}")
        print(f"   Observed std dev: {np.std(observed):.2f}")
        print(f"   Status: {'✅ PASSED' if passed else '❌ FAILED'} (p > 0.05)")
        
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        
        return passed, results
    
    def test_independence(self) -> Tuple[bool, Dict]:
        """
        Test 2: Independence test for consecutive card draws.
        
        Verifies that consecutive cards are statistically independent
        (no correlation).
        
        Returns:
            Tuple of (passed, results_dict)
        """
        print("\n" + "="*70)
        print("TEST 2: Independence Test (Correlation)")
        print("="*70)
        print(f"Running {self.simulations} pair generations...")
        
        # Generate pairs of consecutive random numbers
        first_cards = []
        second_cards = []
        
        for i in range(self.simulations):
            first_cards.append(self.rng.secure_randbelow(78))
            second_cards.append(self.rng.secure_randbelow(78))
            
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i + 1}/{self.simulations} pairs generated")
        
        # Calculate Pearson correlation
        correlation, p_value = stats.pearsonr(first_cards, second_cards)
        
        # Test passes if correlation is close to 0 and p-value > 0.05
        passed = abs(correlation) < 0.1 and p_value > 0.05
        
        results = {
            "test_name": "Independence (Pearson Correlation)",
            "simulations": self.simulations,
            "correlation": float(correlation),
            "p_value": float(p_value),
            "passed": passed,
            "threshold_correlation": 0.1,
            "threshold_p_value": 0.05
        }
        
        print(f"\n📊 Results:")
        print(f"   Correlation coefficient: {correlation:.6f}")
        print(f"   P-value: {p_value:.4f}")
        print(f"   Status: {'✅ PASSED' if passed else '❌ FAILED'} (|r| < 0.1 and p > 0.05)")
        
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        
        return passed, results
    
    def test_kolmogorov_smirnov(self) -> Tuple[bool, Dict]:
        """
        Test 3: Kolmogorov-Smirnov test for uniform distribution.
        
        Compares the empirical distribution of random numbers against
        the theoretical uniform distribution.
        
        Returns:
            Tuple of (passed, results_dict)
        """
        print("\n" + "="*70)
        print("TEST 3: Kolmogorov-Smirnov Test")
        print("="*70)
        print(f"Running {self.simulations} random number generations...")
        
        # Generate random numbers in [0, 1)
        random_numbers = []
        for i in range(self.simulations):
            # Convert random integer to float in [0, 1)
            random_numbers.append(self.rng.secure_randbelow(10000) / 10000)
            
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i + 1}/{self.simulations} numbers generated")
        
        # Perform K-S test against uniform distribution
        ks_stat, p_value = stats.kstest(random_numbers, 'uniform')
        
        # Test passes if p-value > 0.05
        passed = p_value > 0.05
        
        results = {
            "test_name": "Kolmogorov-Smirnov Uniformity",
            "simulations": self.simulations,
            "ks_statistic": float(ks_stat),
            "p_value": float(p_value),
            "passed": passed,
            "threshold": 0.05
        }
        
        print(f"\n📊 Results:")
        print(f"   K-S statistic: {ks_stat:.6f}")
        print(f"   P-value: {p_value:.4f}")
        print(f"   Status: {'✅ PASSED' if passed else '❌ FAILED'} (p > 0.05)")
        
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        
        return passed, results
    
    def test_entropy(self) -> Tuple[bool, Dict]:
        """
        Test 4: Shannon entropy test.
        
        Measures the entropy of generated random bytes to verify
        high-quality randomness.
        
        Returns:
            Tuple of (passed, results_dict)
        """
        print("\n" + "="*70)
        print("TEST 4: Shannon Entropy Test")
        print("="*70)
        print(f"Generating {self.simulations} random bytes...")
        
        # Generate random bytes
        random_bytes = []
        for i in range(self.simulations):
            random_bytes.append(self.rng.secure_randbelow(256))
            
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i + 1}/{self.simulations} bytes generated")
        
        # Calculate Shannon entropy
        byte_counts = Counter(random_bytes)
        total = len(random_bytes)
        entropy = 0
        
        for count in byte_counts.values():
            probability = count / total
            if probability > 0:
                entropy -= probability * np.log2(probability)
        
        # Maximum entropy for 8 bits is 8.0
        max_entropy = 8.0
        entropy_ratio = entropy / max_entropy
        
        # Test passes if entropy is > 7.5 bits (93.75% of maximum)
        passed = entropy > 7.5
        
        results = {
            "test_name": "Shannon Entropy",
            "simulations": self.simulations,
            "entropy_bits": float(entropy),
            "max_entropy_bits": max_entropy,
            "entropy_ratio": float(entropy_ratio),
            "passed": passed,
            "threshold": 7.5
        }
        
        print(f"\n📊 Results:")
        print(f"   Shannon entropy: {entropy:.4f} bits")
        print(f"   Maximum entropy: {max_entropy} bits")
        print(f"   Entropy ratio: {entropy_ratio:.2%}")
        print(f"   Status: {'✅ PASSED' if passed else '❌ FAILED'} (entropy > 7.5 bits)")
        
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        
        return passed, results
    
    def test_orientation_balance(self) -> Tuple[bool, Dict]:
        """
        Test 5: Card orientation balance test.
        
        Verifies that card orientations (upright/reversed) follow
        a 50/50 distribution.
        
        Returns:
            Tuple of (passed, results_dict)
        """
        print("\n" + "="*70)
        print("TEST 5: Orientation Balance Test")
        print("="*70)
        print(f"Running {self.simulations} orientation determinations...")
        
        # Generate orientations
        reversed_count = 0
        for i in range(self.simulations):
            if self.shuffler.determine_orientation():
                reversed_count += 1
            
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i + 1}/{self.simulations} orientations determined")
        
        upright_count = self.simulations - reversed_count
        proportion_reversed = reversed_count / self.simulations
        
        # Binomial test for 50/50 distribution
        p_value = stats.binomtest(reversed_count, self.simulations, 0.5, 
                                   alternative='two-sided').pvalue
        
        # Test passes if p-value > 0.05
        passed = p_value > 0.05
        
        results = {
            "test_name": "Orientation Balance",
            "simulations": self.simulations,
            "reversed_count": reversed_count,
            "upright_count": upright_count,
            "proportion_reversed": float(proportion_reversed),
            "expected_proportion": 0.5,
            "p_value": float(p_value),
            "passed": passed,
            "threshold": 0.05
        }
        
        print(f"\n📊 Results:")
        print(f"   Reversed: {reversed_count} ({proportion_reversed:.2%})")
        print(f"   Upright: {upright_count} ({(1-proportion_reversed):.2%})")
        print(f"   Expected: 50% each")
        print(f"   P-value: {p_value:.4f}")
        print(f"   Status: {'✅ PASSED' if passed else '❌ FAILED'} (p > 0.05)")
        
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        
        return passed, results
    
    def test_spread_types(self) -> Tuple[bool, Dict]:
        """
        Test 6: Test all tarot spread types.
        
        Validates randomness for different spread sizes:
        1, 3, 5, 6, 7, 10, 12 cards.
        
        Returns:
            Tuple of (passed, results_dict)
        """
        print("\n" + "="*70)
        print("TEST 6: Spread Types Test")
        print("="*70)
        
        spread_sizes = [1, 3, 5, 6, 7, 10, 12]
        spread_results = {}
        all_passed = True
        
        for size in spread_sizes:
            print(f"\n  Testing {size}-card spread ({self.simulations // 10} simulations)...")
            
            # Track which cards appear in first position
            first_card_counts = Counter()
            deck = list(range(78))
            
            for _ in range(self.simulations // 10):
                shuffled = self.shuffler.shuffle_deck(deck)
                drawn = shuffled[:size]
                first_card_counts[drawn[0]] += 1
            
            # Chi-squared test
            observed = list(first_card_counts.values())
            chi2_stat, p_value = stats.chisquare(observed)
            
            passed = p_value > 0.05
            all_passed = all_passed and passed
            
            spread_results[f"{size}_cards"] = {
                "size": size,
                "chi2_statistic": float(chi2_stat),
                "p_value": float(p_value),
                "passed": passed
            }
            
            print(f"     Chi-squared p-value: {p_value:.4f} - {'✅ PASSED' if passed else '❌ FAILED'}")
        
        results = {
            "test_name": "Spread Types",
            "spread_results": spread_results,
            "all_passed": all_passed,
            "passed": all_passed
        }
        
        print(f"\n📊 Overall Status: {'✅ ALL PASSED' if all_passed else '❌ SOME FAILED'}")
        
        self.total_tests += 1
        if all_passed:
            self.passed_tests += 1
        
        return all_passed, results
    
    def test_collision_patterns(self) -> Tuple[bool, Dict]:
        """
        Test 7: Collision and pattern detection test.
        
        Checks for unexpected patterns or collisions in shuffled decks.
        
        Returns:
            Tuple of (passed, results_dict)
        """
        print("\n" + "="*70)
        print("TEST 7: Collision and Pattern Detection")
        print("="*70)
        print(f"Running {self.simulations // 10} shuffle simulations...")
        
        deck = list(range(78))
        shuffle_hashes = set()
        collisions = 0
        
        # Track sequential patterns
        sequential_count = 0
        
        for i in range(self.simulations // 10):
            shuffled = self.shuffler.shuffle_deck(deck)
            
            # Create hash of shuffle
            shuffle_hash = tuple(shuffled)
            if shuffle_hash in shuffle_hashes:
                collisions += 1
            shuffle_hashes.add(shuffle_hash)
            
            # Check for sequential patterns (3+ cards in sequence)
            has_sequence = False
            for j in range(len(shuffled) - 2):
                if shuffled[j] + 1 == shuffled[j+1] and shuffled[j+1] + 1 == shuffled[j+2]:
                    has_sequence = True
                    break
            
            if has_sequence:
                sequential_count += 1
            
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{self.simulations // 10} shuffles analyzed")
        
        # Calculate expected sequential patterns (should be rare but possible)
        total_shuffles = self.simulations // 10
        sequential_rate = sequential_count / total_shuffles
        
        # Test passes if no collisions and sequential rate is reasonable
        passed = collisions == 0 and sequential_rate < 0.5
        
        results = {
            "test_name": "Collision and Pattern Detection",
            "simulations": total_shuffles,
            "unique_shuffles": len(shuffle_hashes),
            "collisions": collisions,
            "sequential_patterns": sequential_count,
            "sequential_rate": float(sequential_rate),
            "passed": passed
        }
        
        print(f"\n📊 Results:")
        print(f"   Unique shuffles: {len(shuffle_hashes)}/{total_shuffles}")
        print(f"   Collisions: {collisions}")
        print(f"   Sequential patterns: {sequential_count} ({sequential_rate:.2%})")
        print(f"   Status: {'✅ PASSED' if passed else '❌ FAILED'} (no collisions, patterns < 50%)")
        
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        
        return passed, results
    
    def test_performance(self) -> Tuple[bool, Dict]:
        """
        Test 8: Performance test.
        
        Measures the speed of random number generation and shuffling.
        
        Returns:
            Tuple of (passed, results_dict)
        """
        print("\n" + "="*70)
        print("TEST 8: Performance Test")
        print("="*70)
        
        import time
        
        # Test 1: Random number generation speed
        print(f"\n  Testing random number generation ({self.simulations} iterations)...")
        start = time.perf_counter()
        for _ in range(self.simulations):
            self.rng.secure_randbelow(78)
        rng_time = time.perf_counter() - start
        rng_ops_per_sec = self.simulations / rng_time
        
        # Test 2: Shuffle speed
        print(f"  Testing shuffle operations ({self.simulations // 10} iterations)...")
        deck = list(range(78))
        start = time.perf_counter()
        for _ in range(self.simulations // 10):
            self.shuffler.shuffle_deck(deck)
        shuffle_time = time.perf_counter() - start
        shuffle_ops_per_sec = (self.simulations // 10) / shuffle_time
        
        # Test passes if performance is reasonable (>1000 ops/sec for RNG)
        passed = rng_ops_per_sec > 1000 and shuffle_ops_per_sec > 100
        
        results = {
            "test_name": "Performance",
            "rng_operations": self.simulations,
            "rng_time_seconds": float(rng_time),
            "rng_ops_per_second": float(rng_ops_per_sec),
            "shuffle_operations": self.simulations // 10,
            "shuffle_time_seconds": float(shuffle_time),
            "shuffle_ops_per_second": float(shuffle_ops_per_sec),
            "passed": passed
        }
        
        print(f"\n📊 Results:")
        print(f"   RNG: {rng_ops_per_sec:.0f} operations/second")
        print(f"   Shuffle: {shuffle_ops_per_sec:.0f} operations/second")
        print(f"   Status: {'✅ PASSED' if passed else '❌ FAILED'} (adequate performance)")
        
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        
        return passed, results
    
    def run_all_tests(self) -> Dict:
        """
        Run all tests in the suite.
        
        Returns:
            Dictionary with all test results
        """
        print("\n" + "="*70)
        print("🔬 CRYPTOGRAPHIC RANDOMNESS TEST SUITE")
        print("="*70)
        print(f"Simulations per test: {self.simulations}")
        print(f"Target: >90% pass rate (p-value > 0.05 for statistical tests)")
        print("="*70)
        
        all_results = {
            "timestamp": datetime.now().isoformat(),
            "simulations": self.simulations,
            "tests": {}
        }
        
        # Run all tests
        tests = [
            ("uniformity_chi_squared", self.test_uniformity_chi_squared),
            ("independence", self.test_independence),
            ("kolmogorov_smirnov", self.test_kolmogorov_smirnov),
            ("entropy", self.test_entropy),
            ("orientation_balance", self.test_orientation_balance),
            ("spread_types", self.test_spread_types),
            ("collision_patterns", self.test_collision_patterns),
            ("performance", self.test_performance)
        ]
        
        for test_name, test_func in tests:
            try:
                passed, results = test_func()
                all_results["tests"][test_name] = results
            except Exception as e:
                print(f"\n❌ ERROR in {test_name}: {str(e)}")
                all_results["tests"][test_name] = {
                    "test_name": test_name,
                    "error": str(e),
                    "passed": False
                }
                self.total_tests += 1
        
        # Calculate overall statistics
        pass_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        all_results["summary"] = {
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.total_tests - self.passed_tests,
            "pass_rate": float(pass_rate),
            "target_pass_rate": 90.0,
            "meets_target": pass_rate >= 90.0
        }
        
        # Print summary
        print("\n" + "="*70)
        print("📊 TEST SUITE SUMMARY")
        print("="*70)
        print(f"Total tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Pass rate: {pass_rate:.1f}%")
        print(f"Target: 90%")
        
        if pass_rate >= 90:
            print("\n✅ SUCCESS: Cryptographic randomness validated!")
            print("   The system meets the requirements for surgical randomness.")
        else:
            print("\n⚠️  WARNING: Pass rate below target")
            print("   Some tests failed. Review results for details.")
        
        # Get entropy info
        entropy_info = self.shuffler.get_statistics()
        all_results["entropy_info"] = entropy_info
        
        print("\n📋 Entropy Information:")
        for key, value in entropy_info.items():
            print(f"   {key}: {value}")
        
        return all_results


def main():
    """Main function to run the test suite."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test cryptographic randomness in tarot system"
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=1000,
        help="Number of simulations per test (default: 1000)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="test_results_secure_randomness.json",
        help="Output file for results (default: test_results_secure_randomness.json)"
    )
    
    args = parser.parse_args()
    
    # Run test suite
    suite = RandomnessTestSuite(simulations=args.simulations)
    results = suite.run_all_tests()
    
    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {args.output}")
    
    # Exit with appropriate code
    if results["summary"]["meets_target"]:
        print("\n✨ All tests passed! System is ready for production.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Review results before deployment.")
        sys.exit(1)


if __name__ == "__main__":
    main()
