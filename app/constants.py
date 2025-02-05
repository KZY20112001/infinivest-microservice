from enum import Enum

    
class AppConstants(Enum):
    ALLOWED_BANKS = ['ocbc', 'sc']
    ALLOWED_PORTFOLIO_CATEGORIES = ['large_cap_blend', 'small_cap_blend', 'international_stocks', 'emerging_markets', 'intermediate_bonds', 'international_bonds', 'commodities', 'reits']