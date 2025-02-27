from pydantic import BaseModel
from typing import List

class Portfolio(BaseModel):
    large_cap_blend: float
    small_cap_blend: float
    international_stocks: float
    emerging_markets: float
    intermediate_bonds: float
    international_bonds: float
    cash: float


class PortfolioResponse(BaseModel):
    portfolio: Portfolio
    reason: str

class Asset(BaseModel):
    symbol: str
    percentage: float

class AssetAllocationResponse(BaseModel):
    assets: List[Asset]