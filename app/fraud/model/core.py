from __future__ import annotations

import datetime as dt
from typing import List
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship

from app.shared.constants import TransactionStatus, DeviceType, ScreenOrientation


class Rule(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field()
    action: TransactionStatus = Field()


class Transaction(SQLModel, table=True):
    id: str = Field(primary_key=True)
    description: str = Field()
    same_holder: bool = Field()
    currency: str = Field(nullable=True)
    transaction_value: float = Field()
    transaction_time: dt.datetime = Field()
    datetime_program: dt.datetime = Field(nullable=True)
    customer_doc: str = Field(nullable=True)
    receptor_doc: str = Field(nullable=True)

    # device
    device_fingerprint: str = Field(nullable=True)
    device_timezone: str = Field(nullable=True)
    device_vendor: str = Field(nullable=True)
    device_version: str = Field(nullable=True)
    device_language: str = Field(nullable=True)
    device_user_agent: str = Field(nullable=True)
    device_model: str = Field(nullable=True)
    device_platform: str = Field(nullable=True)
    device_category: DeviceType = Field(nullable=True)  # Assuming DeviceType is an Enum
    device_ip: str = Field(nullable=True)

    device_longitude: float = Field(nullable=True)
    device_latitude: float = Field(nullable=True)

    device_memory: float = Field(nullable=True)
    device_cpu_count: int = Field(nullable=True)

    device_cookies_enabled: bool = Field(nullable=True)
    device_screen_resolution_x: int = Field(nullable=True)
    device_screen_resolution_y: int = Field(nullable=True)
    device_screen_orientation: ScreenOrientation = Field(nullable=True)


class TransactionAnalysis(SQLModel, table=True):
    id: int = Field(primary_key=True)
    internal_id: UUID = Field(
        default_factory=uuid4,
    )
    client_id: int = Field()
    model_id: str = Field(nullable=True)
    transaction_id: str = Field(nullable=True)
    # rules_triggered: List[Rule] = Relationship()
    prediction: float = Field(nullable=True)
    action: str = Field(nullable=True)
    input_data: str = Field(nullable=True)
    response: str = Field(nullable=True)
    error: str = Field(nullable=True)
    created_at: dt.datetime = Field()
    status_id: str = Field(nullable=True)
