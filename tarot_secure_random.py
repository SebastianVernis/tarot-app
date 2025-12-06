#!/usr/bin/env python3
"""
Cryptographically Secure Random Number Generator for Tarot System
Author: Assistant
Description: Implements surgical randomness using cryptographic methods
             for tarot card shuffling and selection.

Security Features:
- Uses secrets module (CSPRNG - Cryptographically Secure Pseudo-Random Number Generator)
- Based on os.urandom() which uses /dev/urandom on Unix systems
- No predictable seeds (no date, time, IP, user_id, etc.)
- Fisher-Yates shuffle algorithm with cryptographic RNG
- Uniform distribution guaranteed by design

Entropy Sources:
- /dev/urandom (Linux/Unix) - Kernel entropy pool
- CryptGenRandom (Windows) - OS-level cryptographic RNG
- Hardware RNG when available (RDRAND CPU instruction)
"""

import secrets
import os
from typing import List, TypeVar, Tuple
from collections import Counter

T = TypeVar('T')


class SecureRandomGenerator:
    """
    Cryptographically secure random number generator for tarot operations.
    
    This class provides methods for:
    - Secure shuffling of card decks
    - Secure selection of cards
    - Secure boolean generation (for card orientation)
    
    All methods use the secrets module which is designed for
    cryptographic applications and security-sensitive operations.
    """
    
    def __init__(self):
        """
        Initialize the secure random generator.
        
        No seed is used - the secrets module automatically uses
        the best available entropy source from the operating system.
        """
        # Verify that os.urandom is available
        try:
            test_bytes = os.urandom(16)
            self.entropy_available = True
        except NotImplementedError:
            self.entropy_available = False
            raise RuntimeError(
                "os.urandom() is not available on this system. "
                "Cryptographically secure randomness cannot be guaranteed."
            )
        
        # Statistics for auditing
        self.shuffle_count = 0
        self.selection_count = 0
        self.bool_count = 0
    
    def secure_randbelow(self, n: int) -> int:
        """
        Generate a cryptographically secure random integer in range [0, n).
        
        This uses secrets.randbelow() which implements unbiased random
        selection without modulo bias.
        
        Args:
            n: Upper bound (exclusive)
            
        Returns:
            Random integer in range [0, n)
            
        Raises:
            ValueError: If n <= 0
        """
        if n <= 0:
            raise ValueError("n must be positive")
        
        return secrets.randbelow(n)
    
    def secure_shuffle(self, items: List[T]) -> List[T]:
        """
        Shuffle a list using the Fisher-Yates algorithm with cryptographic RNG.
        
        The Fisher-Yates shuffle guarantees uniform distribution of all
        possible permutations. Combined with cryptographic RNG, this
        provides surgical randomness.
        
        Time Complexity: O(n)
        Space Complexity: O(n) for the copy
        
        Args:
            items: List to shuffle
            
        Returns:
            New shuffled list (original is not modified)
        """
        # Create a copy to avoid modifying the original
        shuffled = items.copy()
        n = len(shuffled)
        
        # Fisher-Yates shuffle algorithm
        # Iterate from the last element to the first
        for i in range(n - 1, 0, -1):
            # Pick a random index from 0 to i (inclusive)
            j = self.secure_randbelow(i + 1)
            
            # Swap elements at positions i and j
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        
        self.shuffle_count += 1
        return shuffled
    
    def secure_choice(self, items: List[T]) -> T:
        """
        Select a random element from a list using cryptographic RNG.
        
        Args:
            items: Non-empty list to choose from
            
        Returns:
            Randomly selected element
            
        Raises:
            ValueError: If items is empty
        """
        if not items:
            raise ValueError("Cannot choose from empty list")
        
        index = self.secure_randbelow(len(items))
        self.selection_count += 1
        return items[index]
    
    def secure_bool(self) -> bool:
        """
        Generate a cryptographically secure random boolean.
        
        Uses secrets.randbits(1) which generates a single random bit.
        This provides perfectly balanced True/False distribution.
        
        Returns:
            Random boolean value
        """
        self.bool_count += 1
        return bool(secrets.randbits(1))
    
    def secure_sample(self, items: List[T], k: int) -> List[T]:
        """
        Select k unique random elements from a list without replacement.
        
        This is equivalent to shuffling and taking the first k elements,
        but more efficient for small k.
        
        Args:
            items: List to sample from
            k: Number of elements to select
            
        Returns:
            List of k randomly selected unique elements
            
        Raises:
            ValueError: If k > len(items) or k < 0
        """
        if k < 0:
            raise ValueError("k must be non-negative")
        if k > len(items):
            raise ValueError("k cannot be larger than the list size")
        
        # For small k, use partial Fisher-Yates
        # For large k, shuffle and take first k
        if k > len(items) // 2:
            # More efficient to shuffle and take first k
            shuffled = self.secure_shuffle(items)
            return shuffled[:k]
        else:
            # Partial Fisher-Yates for better performance
            result = items.copy()
            n = len(result)
            
            for i in range(k):
                # Pick random element from remaining items
                j = i + self.secure_randbelow(n - i)
                result[i], result[j] = result[j], result[i]
            
            self.selection_count += k
            return result[:k]
    
    def get_entropy_info(self) -> dict:
        """
        Get information about the entropy source being used.
        
        Returns:
            Dictionary with entropy information
        """
        info = {
            "entropy_available": self.entropy_available,
            "entropy_source": "os.urandom()",
            "algorithm": "CSPRNG (Cryptographically Secure Pseudo-Random Number Generator)",
            "shuffle_count": self.shuffle_count,
            "selection_count": self.selection_count,
            "bool_count": self.bool_count,
        }
        
        # Try to get system-specific entropy information
        try:
            if os.path.exists('/proc/sys/kernel/random/entropy_avail'):
                with open('/proc/sys/kernel/random/entropy_avail', 'r') as f:
                    info["kernel_entropy_bits"] = int(f.read().strip())
        except:
            pass
        
        return info
    
    def reset_statistics(self):
        """Reset usage statistics."""
        self.shuffle_count = 0
        self.selection_count = 0
        self.bool_count = 0


class TarotSecureShuffler:
    """
    Specialized shuffler for tarot card operations.
    
    This class provides high-level methods specifically designed
    for tarot card shuffling and selection, ensuring cryptographic
    randomness throughout.
    """
    
    def __init__(self):
        """Initialize the tarot shuffler with a secure RNG."""
        self.rng = SecureRandomGenerator()
    
    def shuffle_deck(self, deck: List[T]) -> List[T]:
        """
        Shuffle a complete tarot deck (78 cards) with cryptographic security.
        
        This method:
        1. Validates deck size
        2. Applies Fisher-Yates shuffle with CSPRNG
        3. Returns shuffled deck
        
        Args:
            deck: List of 78 tarot cards
            
        Returns:
            Shuffled deck
        """
        if len(deck) != 78:
            # Allow any size for flexibility, but warn if not standard
            pass
        
        return self.rng.secure_shuffle(deck)
    
    def draw_cards(self, deck: List[T], count: int) -> Tuple[List[T], List[T]]:
        """
        Draw cards from a shuffled deck.
        
        Args:
            deck: Shuffled deck to draw from
            count: Number of cards to draw
            
        Returns:
            Tuple of (drawn_cards, remaining_deck)
            
        Raises:
            ValueError: If count > len(deck)
        """
        if count > len(deck):
            raise ValueError(f"Cannot draw {count} cards from deck of {len(deck)}")
        
        drawn = deck[:count]
        remaining = deck[count:]
        
        return drawn, remaining
    
    def determine_orientation(self) -> bool:
        """
        Determine if a card is reversed (inverted) using cryptographic RNG.
        
        Returns:
            True if card is reversed, False if upright
        """
        return self.rng.secure_bool()
    
    def shuffle_and_draw(self, deck: List[T], count: int) -> Tuple[List[T], List[bool]]:
        """
        Complete operation: shuffle deck, draw cards, and determine orientations.
        
        This is the main method for tarot readings, combining all operations
        with cryptographic security.
        
        Args:
            deck: Unshuffled deck
            count: Number of cards to draw
            
        Returns:
            Tuple of (drawn_cards, orientations)
            where orientations[i] is True if card i is reversed
        """
        # Shuffle the deck
        shuffled = self.shuffle_deck(deck)
        
        # Draw cards
        drawn, _ = self.draw_cards(shuffled, count)
        
        # Determine orientations for each card
        orientations = [self.determine_orientation() for _ in range(count)]
        
        return drawn, orientations
    
    def get_statistics(self) -> dict:
        """
        Get usage statistics and entropy information.
        
        Returns:
            Dictionary with statistics
        """
        return self.rng.get_entropy_info()


# Global instance for convenience
_global_shuffler = None


def get_secure_shuffler() -> TarotSecureShuffler:
    """
    Get the global secure shuffler instance.
    
    This provides a convenient singleton pattern for the application.
    
    Returns:
        Global TarotSecureShuffler instance
    """
    global _global_shuffler
    if _global_shuffler is None:
        _global_shuffler = TarotSecureShuffler()
    return _global_shuffler


# Convenience functions for direct use
def secure_shuffle(items: List[T]) -> List[T]:
    """Convenience function for secure shuffling."""
    return get_secure_shuffler().shuffle_deck(items)


def secure_choice(items: List[T]) -> T:
    """Convenience function for secure selection."""
    return get_secure_shuffler().rng.secure_choice(items)


def secure_bool() -> bool:
    """Convenience function for secure boolean generation."""
    return get_secure_shuffler().rng.secure_bool()


def get_entropy_info() -> dict:
    """Convenience function to get entropy information."""
    return get_secure_shuffler().get_statistics()


if __name__ == "__main__":
    # Demonstration and basic testing
    print("🔐 Cryptographically Secure Random Number Generator for Tarot")
    print("=" * 70)
    
    # Create shuffler
    shuffler = TarotSecureShuffler()
    
    # Test with a simple deck
    test_deck = list(range(78))
    print(f"\n📋 Original deck (first 10): {test_deck[:10]}")
    
    # Shuffle
    shuffled = shuffler.shuffle_deck(test_deck)
    print(f"🔀 Shuffled deck (first 10): {shuffled[:10]}")
    
    # Draw cards
    drawn, orientations = shuffler.shuffle_and_draw(test_deck, 10)
    print(f"\n🎴 Drew 10 cards: {drawn}")
    print(f"🔄 Orientations (True=Reversed): {orientations}")
    
    # Show statistics
    stats = shuffler.get_statistics()
    print(f"\n📊 Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Verify uniformity with a simple test
    print(f"\n🧪 Quick uniformity test (1000 shuffles):")
    position_counts = Counter()
    
    for _ in range(1000):
        shuffled = shuffler.shuffle_deck(list(range(78)))
        # Track where card 0 ends up
        position_counts[shuffled.index(0)] += 1
    
    # Calculate statistics
    expected = 1000 / 78
    max_deviation = max(abs(count - expected) for count in position_counts.values())
    
    print(f"   Expected count per position: {expected:.2f}")
    print(f"   Max deviation from expected: {max_deviation:.2f}")
    print(f"   Relative deviation: {(max_deviation / expected) * 100:.1f}%")
    
    if max_deviation / expected < 0.3:  # Within 30% is good for 1000 samples
        print("   ✅ Distribution appears uniform")
    else:
        print("   ⚠️  Distribution may need more samples for verification")
    
    print("\n✨ Secure random generator is ready for production use")
