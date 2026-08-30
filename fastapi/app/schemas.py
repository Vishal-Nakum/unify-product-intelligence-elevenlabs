from typing import Literal,Optional
from pydantic import BaseModel,Field

class ProductMetricsRequest(BaseModel):
    metric: Literal["nps","monthly_active_users","mobile_active_users","free_to_paid_conversion_pct","retention_30d_pct","avg_session_minutes","p95_api_latency_ms"]
    start_month: Optional[str]=Field(None,description="YYYY-MM-DD")
    end_month: Optional[str]=Field(None,description="YYYY-MM-DD")

class SupportRequest(BaseModel):
    start_month: Optional[str]=Field(None,description="YYYY-MM")
    end_month: Optional[str]=Field(None,description="YYYY-MM")
    category: Optional[str]=None
    priority: Optional[str]=None
    churn_risk: Optional[str]=None
    account_id: Optional[str]=None
    limit: int=Field(20,ge=1,le=100)
    model_config = {
        "json_schema_extra": {
            "example": {
                "start_month": None,
                "end_month": None,
                "category": None,
                "priority": None,
                "churn_risk": None,
                "account_id": None,
                "limit": 20
            }
        }
    }

class CustomerHealthRequest(BaseModel):
    segment: Optional[Literal["SMB","Mid-Market","Enterprise"]]=None
    risk_level: Optional[Literal["Low","Medium","High","Critical"]]=None
    minimum_arr: Optional[float]=Field(None,ge=0)
    limit: int=Field(20,ge=1,le=100)

class FeedbackSearchRequest(BaseModel):
    query: Optional[str]=None
    month: Optional[str]=None
    platform: Optional[str]=None
    sentiment: Optional[str]=None
    category: Optional[str]=None
    limit: int=Field(20,ge=1,le=100)

class ExecutiveSummaryRequest(BaseModel):
    question: str=Field(...,min_length=3,max_length=500)
