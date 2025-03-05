from pydantic import BaseModel
from typing import List,Optional

class Portfolio(BaseModel):
    largeCapBlend: float
    smallCapBlend: float
    internationalStocks: float
    emergingMarkets: float
    intermediateBonds: float
    internationalBonds: float
    cash: float

class PortfolioResponse(BaseModel):
    portfolio: Portfolio
    reason: str

class Asset(BaseModel):
    name: Optional[str] = None    
    symbol: str
    percentage: float
        
class AssetAllocationResponse(BaseModel):
    assets: List[Asset]