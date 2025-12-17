from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4

class CreateApplicationRequest(BaseModel):
    customer_id: str = Field(min_length=1)
    merchant_id: str = Field(min_length=1)
    amount: int = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    term_months: int = Field(gt=0, le=72)

class Application(BaseModel):
    id: UUID
    customer_id: str
    merchant_id: str
    amount: int
    currency: str
    term_months: int
    status: str
    created_at: datetime

def new_application(req: CreateApplicationRequest) -> Application:
    return Application(
        id=uuid4(),
        customer_id=req.customer_id,
        merchant_id=req.merchant_id,
        amount=req.amount,
        currency=req.currency.upper(),
        term_months=req.term_months,
        status="CREATED",
        created_at=datetime.now(timezone.utc),
    )
