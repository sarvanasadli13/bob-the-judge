from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime


TransactionType = Literal["domestic", "international", "instant", "scheduled", "wire_transfer"]


class PaymentRequest(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction ID")
    amount: float = Field(..., gt=0, description="Payment amount")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO 4217 code")
    payer_account: str
    payee_account: str
    transaction_type: TransactionType = "domestic"
    timestamp: Optional[datetime] = None


class PaymentResponse(BaseModel):
    transaction_id: str
    processed_amount: float
    fee: float
    total_charged: float
    currency: str
    status: Literal["approved", "declined", "pending"]
    audit_log: str
    processing_time_ms: float
    system: Literal["legacy", "modern"]
