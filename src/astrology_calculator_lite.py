"""
Lightweight astrology calculator wrapper
Gracefully handles missing heavy dependencies for Vercel deployment
"""
from typing import Dict, Optional

# Try to import the full astrology calculator
try:
    from astrology_calculator import AstrologyCalculator as FullAstrologyCalculator
    FULL_ASTROLOGY_AVAILABLE = True
except ImportError:
    FULL_ASTROLOGY_AVAILABLE = False
    FullAstrologyCalculator = None


class AstrologyCalculatorLite:
    """
    Lightweight wrapper for astrology calculations
    Falls back to basic functionality when heavy dependencies are not available
    """
    
    def __init__(self):
        if FULL_ASTROLOGY_AVAILABLE:
            self.calculator = FullAstrologyCalculator()
        else:
            self.calculator = None
    
    def is_available(self) -> bool:
        """Check if full astrology features are available"""
        return FULL_ASTROLOGY_AVAILABLE
    
    def calculate_birth_chart(self, *args, **kwargs) -> Dict:
        """
        Calculate birth chart if available, otherwise return error message
        """
        if not FULL_ASTROLOGY_AVAILABLE:
            return {
                'error': 'Astrology features not available',
                'message': 'Heavy dependencies (pyswisseph) are disabled in this deployment',
                'suggestion': 'For full astrology features, please use the Render deployment or run locally'
            }
        
        try:
            return self.calculator.calculate_birth_chart(*args, **kwargs)
        except Exception as e:
            return {
                'error': 'Calculation failed',
                'message': str(e)
            }
    
    def get_planetary_positions(self, *args, **kwargs) -> Dict:
        """Get planetary positions if available"""
        if not FULL_ASTROLOGY_AVAILABLE:
            return {
                'error': 'Astrology features not available',
                'message': 'Heavy dependencies (pyswisseph) are disabled in this deployment'
            }
        
        try:
            return self.calculator.get_planetary_positions(*args, **kwargs)
        except Exception as e:
            return {
                'error': 'Calculation failed',
                'message': str(e)
            }


# Export the lite version
AstrologyCalculator = AstrologyCalculatorLite
