from pydantic import BaseModel

class Portfolio(BaseModel):
    large_cap_blend: float
    small_cap_blend: float
    international_stocks: float
    emerging_markets: float
    intermediate_bonds: float
    international_bonds: float
    cash: float
    commodities: float
    reits: float

class PortfolioResponse(BaseModel):
    portfolio: Portfolio
    reason: str
