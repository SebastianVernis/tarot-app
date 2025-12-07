#!/usr/bin/env python3
"""
Final Integration Test - Verify all components work together
"""
print("="*70)
print("🔬 FINAL INTEGRATION TEST")
print("="*70)

# Test 1: Import all modules
print("\n✓ Test 1: Importing modules...")
try:
    from tarot_secure_random import TarotSecureShuffler, SecureRandomGenerator
    from tarot_reader import LectorTarot, TipoTirada, MazoTarot
    print("  ✅ All modules imported successfully")
except Exception as e:
    print(f"  ❌ Import failed: {e}")
    exit(1)

# Test 2: Create instances
print("\n✓ Test 2: Creating instances...")
try:
    shuffler = TarotSecureShuffler()
    rng = SecureRandomGenerator()
    lector = LectorTarot()
    mazo = MazoTarot()
    print("  ✅ All instances created successfully")
except Exception as e:
    print(f"  ❌ Instance creation failed: {e}")
    exit(1)

# Test 3: Verify deck size
print("\n✓ Test 3: Verifying deck composition...")
try:
    assert len(mazo.cartas) == 78, f"Expected 78 cards, got {len(mazo.cartas)}"
    print(f"  ✅ Deck has correct size: {len(mazo.cartas)} cards")
except Exception as e:
    print(f"  ❌ Deck verification failed: {e}")
    exit(1)

# Test 4: Test secure shuffle
print("\n✓ Test 4: Testing secure shuffle...")
try:
    original = list(range(78))
    shuffled = shuffler.shuffle_deck(original)
    assert len(shuffled) == 78, "Shuffled deck size mismatch"
    assert set(shuffled) == set(original), "Shuffled deck missing cards"
    assert shuffled != original, "Deck not shuffled (extremely unlikely)"
    print("  ✅ Secure shuffle works correctly")
except Exception as e:
    print(f"  ❌ Shuffle test failed: {e}")
    exit(1)

# Test 5: Test orientation generation
print("\n✓ Test 5: Testing orientation generation...")
try:
    orientations = [shuffler.determine_orientation() for _ in range(100)]
    true_count = sum(orientations)
    false_count = len(orientations) - true_count
    ratio = true_count / len(orientations)
    assert 0.3 < ratio < 0.7, f"Orientation ratio out of range: {ratio}"
    print(f"  ✅ Orientation balance: {true_count}T/{false_count}F (ratio: {ratio:.2f})")
except Exception as e:
    print(f"  ❌ Orientation test failed: {e}")
    exit(1)

# Test 6: Test all spread types
print("\n✓ Test 6: Testing all spread types...")
spread_types = [
    (TipoTirada.UNA_CARTA, 1),
    (TipoTirada.TRES_CARTAS, 3),
    (TipoTirada.DECISION, 5),
    (TipoTirada.RELACION, 6),
    (TipoTirada.AMOR, 7),
    (TipoTirada.CRUZ_CELTA, 10),
    (TipoTirada.ANUAL, 12)
]

try:
    for tipo, expected_cards in spread_types:
        lectura = lector.realizar_lectura(tipo, "Test question")
        actual_cards = len(lectura["cartas"])
        assert actual_cards == expected_cards, f"{tipo.value}: Expected {expected_cards}, got {actual_cards}"
    print(f"  ✅ All {len(spread_types)} spread types work correctly")
except Exception as e:
    print(f"  ❌ Spread type test failed: {e}")
    exit(1)

# Test 7: Verify entropy info
print("\n✓ Test 7: Checking entropy information...")
try:
    entropy_info = shuffler.get_statistics()
    assert entropy_info["entropy_available"] == True, "Entropy not available"
    assert entropy_info["entropy_source"] == "os.urandom()", "Wrong entropy source"
    assert "CSPRNG" in entropy_info["algorithm"], "Wrong algorithm"
    print("  ✅ Entropy information verified")
    print(f"     Source: {entropy_info['entropy_source']}")
    print(f"     Algorithm: {entropy_info['algorithm']}")
    if "kernel_entropy_bits" in entropy_info:
        print(f"     Kernel entropy: {entropy_info['kernel_entropy_bits']} bits")
except Exception as e:
    print(f"  ❌ Entropy check failed: {e}")
    exit(1)

# Test 8: Verify no predictable patterns
print("\n✓ Test 8: Checking for predictable patterns...")
try:
    # Generate multiple shuffles and verify they're different
    shuffles = []
    for _ in range(10):
        shuffled = shuffler.shuffle_deck(list(range(78)))
        shuffles.append(tuple(shuffled))
    
    unique_shuffles = len(set(shuffles))
    assert unique_shuffles == 10, f"Found duplicate shuffles: {unique_shuffles}/10 unique"
    print(f"  ✅ No predictable patterns detected ({unique_shuffles}/10 unique shuffles)")
except Exception as e:
    print(f"  ❌ Pattern check failed: {e}")
    exit(1)

# Test 9: Performance check
print("\n✓ Test 9: Performance verification...")
try:
    import time
    
    # Test RNG performance
    start = time.perf_counter()
    for _ in range(1000):
        rng.secure_randbelow(78)
    rng_time = time.perf_counter() - start
    rng_ops = 1000 / rng_time
    
    # Test shuffle performance
    start = time.perf_counter()
    for _ in range(100):
        shuffler.shuffle_deck(list(range(78)))
    shuffle_time = time.perf_counter() - start
    shuffle_ops = 100 / shuffle_time
    
    assert rng_ops > 1000, f"RNG too slow: {rng_ops:.0f} ops/s"
    assert shuffle_ops > 100, f"Shuffle too slow: {shuffle_ops:.0f} ops/s"
    
    print(f"  ✅ Performance acceptable")
    print(f"     RNG: {rng_ops:.0f} ops/second")
    print(f"     Shuffle: {shuffle_ops:.0f} ops/second")
except Exception as e:
    print(f"  ❌ Performance check failed: {e}")
    exit(1)

# Final summary
print("\n" + "="*70)
print("📊 INTEGRATION TEST SUMMARY")
print("="*70)
print("Total Tests: 9")
print("Passed: 9")
print("Failed: 0")
print("\n✅ ALL INTEGRATION TESTS PASSED!")
print("\n🎉 System is ready for production use")
print("="*70)
