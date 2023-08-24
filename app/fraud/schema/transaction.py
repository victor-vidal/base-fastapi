from __future__ import annotations

import datetime as dt
from datetime import datetime
from typing import Dict, List, Literal, Optional, Union
from uuid import UUID, uuid4


from pydantic import BaseModel, Field


from app.shared.constants import (
    DecisorAgent,
    TransactionStatus,
    DeviceType,
    ScreenOrientation,
    DecisorAgent,
)
from app.shared.schema import FlatJSONObject


class Rule(BaseModel):
    id: int = Field(description="Id of the rule.", example=15)
    name: str = Field(..., example="block all transactions from mobile.")
    action: Literal[
        TransactionStatus.APPROVED, TransactionStatus.REJECTED, TransactionStatus.REVIEW
    ] = Field(example=TransactionStatus.REJECTED)


class Transaction(BaseModel):
    id: str = Field(
        description="Id of the transaction, if you use a integer based id, convert to string in request time so we can support all range of id's, like UUID.",
        example="4b425c1c-a9e8-4f7e-b7e7-4cc201c3f798",
    )
    description: str = Field(
        description="Description of the transaction.",
        example="Pay my apartment rent.",
    )
    same_holder: bool = Field(
        description="If customer and receptor are the same.", example=False
    )
    currency: Optional[str] = Field(
        description="ISO 4217 currency code format.",
        example="EUR",
    )
    transaction_value: float = Field(
        description="Transaction value.",
        example=130.99,
    )
    transaction_time: dt.datetime = Field(
        description="Datetime in ISO 8601 format (yyyy-MM-dd'T'HH:mm:ss.SSSXXX) of the transaction.",
        example="2015-03-21T11:07:22.956087",
    )
    datetime_program: Optional[dt.datetime] = Field(
        description="Datetime in ISO 8601 format (yyyy-MM-dd'T'HH:mm:ss.SSSXXX) that represents the time the transaction was scheduled.",
        example="2015-03-21T11:07:22.956087",
    )
    customer_doc: Optional[str] = Field(example="XX.XXX.XXX/0001-XX")
    receptor_doc: Optional[str] = Field(example="XX.XXX.XXX/0001-XX")

    # Device
    device_fingerprint: Optional[str] = Field(
        description="Device fingerprint to help identifiyng the same user across diferent sessions",
        example="36004ba1725dfc57ff731cf770228c7e",
    )
    device_timezone: Optional[str] = Field(
        description="Timezone from tz database", example="America/Sao_Paulo"
    )
    device_vendor: Optional[str] = Field(example="Google")
    device_version: Optional[str] = Field(example="7.13.1")
    device_language: Optional[str] = Field(example="pt-BR")
    device_user_agent: Optional[str] = Field(
        description="User agent of the browser",
        example="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    )
    device_model: Optional[str] = Field(
        example="SM-J810M",
    )
    device_platform: Optional[str] = Field(
        description="Platform of the device, e.g. Windows, Linux, Mac, Android, iOS, etc.",
        example="Win32",
    )
    device_category: Optional[
        Literal[
            DeviceType.DESKTOP,
            DeviceType.MOBILE,
        ]
    ] = Field(
        example=DeviceType.MOBILE,
    )
    device_ip: Optional[str] = Field(example="127.0.0.1")

    device_longitude: Optional[float] = Field(example=-43.9687074)
    device_latitude: Optional[float] = Field(example=75.9234567)

    device_memory: Optional[float] = Field(
        description="Device memory in gigabytes", example=8
    )
    device_cpu_count: Optional[int] = Field(
        description="CPU count of the device", example=4
    )

    device_cookies_enabled: Optional[bool] = Field(example=True)
    device_screen_resolution_x: Optional[int] = Field(example=1920)
    device_screen_resolution_y: Optional[int] = Field(example=1080)
    device_screen_orientation: Optional[
        Literal[
            ScreenOrientation.PORTRAIT_PRIMARY,
            ScreenOrientation.PORTRAIT_SECONDARY,
            ScreenOrientation.LANDSCAPE_PRIMARY,
            ScreenOrientation.LANDSCAPE_SECONDARY,
        ]
    ] = Field(
        description="Screen Orientation of the device, e.g. portrait, landscape, etc.",
        example=ScreenOrientation.PORTRAIT_PRIMARY,
    )


class CreateTransaction(BaseModel):
    transaction: Transaction = Field(description="Informations about the transaction.")
    extra_data: Optional[FlatJSONObject] = Field(
        description=" ".join(
            [
                "This is a flat object, that is, no nested structures like lists and objects are allowed inside this object.",
                "Only primitive types are allowed, as seen in the example.",
                "If the model was trained with data that goes beyond our base layout, you can include these extra fields here.",
                "And even if the current model doesn't have this extra information yet, you can add it here",
                "to use in the future as data to new models.",
                "You can anonymize these field names and values, our models won't care about the actual value.",
                "Just ensure there will be field-wise consistency, not mixing types.",
            ]
        ),
        example={
            "custom_field_1": "value of custom field",
            "custom_field_2": 10.53,
            "custom_field_3": False,
        },
    )
    _schema_version: str = "1"

    class Config:
        underscore_attrs_are_private = True


class TransactionUpdate(BaseModel):
    status: Optional[
        Literal[
            TransactionStatus.PROCESSING,
            TransactionStatus.CANCELLED,
            TransactionStatus.REVIEW,
            TransactionStatus.APPROVED,
            TransactionStatus.REJECTED,
            TransactionStatus.FRAUD,
            TransactionStatus.FRIENDLY_FRAUD,
            TransactionStatus.TRADE_DISAGREEMENT,
            TransactionStatus.AUTOFRAUD,
        ]
    ] = Field(
        description=" ".join(
            [
                "Status of the transaction.",
                f"{TransactionStatus.PROCESSING}: First status of the Transaction.",
                f"{TransactionStatus.CANCELLED}: Transaction was cancelled, could be manually, by algorithm, rule, third_party.",
                f"{TransactionStatus.REVIEW}: Transaction is awaiting review, could be manually, by algorithm, rule, third_party.",
                f"{TransactionStatus.APPROVED}: Transaction approved, could be manually, by algorithm, rule, third_party.",
                f"{TransactionStatus.REJECTED}: Transaction rejected, could be manually, by algorithm, rule, third_party.",
                f"{TransactionStatus.FRAUD}: Transaction certainly identified as fraud after being approved, normally associated with a chargeback.",
                f"{TransactionStatus.FRIENDLY_FRAUD}: User mistake. Eg: User child did the transaction.",
                f"{TransactionStatus.TRADE_DISAGREEMENT}: Any sort of trade disagreement.",
                f"{TransactionStatus.AUTOFRAUD}: User used his own true informations like address and credit card, but requests a chargeback. ",
                "Eg: He claims he didn't receive the product.",
            ]
        ),
        example=TransactionStatus.FRAUD,
    )

    decisor_agent: Optional[
        Literal[
            DecisorAgent.MANUAL,
            DecisorAgent.ALGORITHM,
            DecisorAgent.RULE,
            DecisorAgent.THIRD_PARTY,
        ]
    ] = Field(
        description=" ".join(
            [
                "Who decided the status change.",
                "The manual decisor has precedence over the algorithm and rule decision.",
                "The rule has precedence over the algorithm decision.",
                "MANUAL: A human analyst decided to reject or approve the Transaction.",
                "ALGORITHM: DataRudder algorithm was used to decide the status of the transaction.",
                "RULE: A DataRudder rule triggered and used to decide the status of the transaction.",
                "THIRD_PARTY: Could be another antifraud or another institution involved in the process.",
            ]
        ),
        example=DecisorAgent.ALGORITHM,
    )

    changed_at: Optional[dt.datetime] = Field(
        description="Datetime in ISO 8601 format (yyyy-MM-dd'T'HH:mm:ss.SSSXXX).",
        example="2015-03-21T11:07:22.956087",
    )

    description: Optional[str] = Field(
        description="Description of the status change.",
        example="Transaction was approved by the algorithm.",
    )


class TransactionUpdateWithId(TransactionUpdate):
    id: str = Field(
        description="Id of the Transaction, if you use a integer based id, convert to string in request time so we can support all range of id's, like UUID.",
        example="4b425c1c-a9e8-4f7e-b7e7-4cc201c3f798",
    )


class BatchTransactionUpdate(BaseModel):
    transactions: List[TransactionUpdateWithId] = Field(
        description=(
            "List of status changes in transactions to update, "
            "a single transaction can appear multiple times in this list, "
            "considering multiple status changes."
        )
    )


class CreateTransactionResponse(BaseModel):
    id: str = Field(example="4b425c1c-a9e8-4f7e-b7e7-4cc201c3f798")
    score: Optional[float] = Field(
        description=(
            "Output from or Artificial Inteligence model,"
            "you can interpret as the probability of this application being fraudulent."
            "The higher the score, the more likely the application is fraudulent."
            "The score is between 0 and 1."
        ),
        example=0.87,
    )
    action: Literal[
        TransactionStatus.APPROVED, TransactionStatus.REJECTED, TransactionStatus.REVIEW
    ] = Field(
        description="Action suggested based on combination of Rule actions and model score.",
        example=TransactionStatus.REJECTED,
    )
    rules_triggered: Optional[List[Rule]]
    in_request_milliseconds: float
    timings: Optional[Dict[str, float]]


class TransactionUpdateRequest(BaseModel):
    transaction_id: Optional[str]
    body: str
    client_id: int
    created_at: Optional[dt.datetime] = Field(default_factory=datetime.utcnow)


class TransactionUpdateResponse(BaseModel):
    id: str = Field(example="4b425c1c-a9e8-4f7e-b7e7-4cc201c3f798")


class BatchTransactionUpdateResponse(BaseModel):
    batch_id: str = Field(example="4b425c1c-a9e8-4f7e-b7e7-4cc201c3f798")


class TransactionAnalysis(BaseModel):
    internal_id: Optional[UUID] = Field(default_factory=uuid4)
    client_id: int = Field()
    model_id: Optional[str] = Field()
    transaction_id: Optional[str] = Field()
    # rules_triggered: Optional[List[Rule]] = []
    prediction: Optional[float] = Field()
    action: Optional[str] = Field()
    input_data: str = Field()
    response: Optional[str] = Field()
    error: Optional[str] = Field()
    created_at: datetime = Field()
    status_id: Optional[str] = Field()

    class Config:
        arbitrary_types_allowed = True


class Analysis(BaseModel):
    transaction_id: str
    client_id: int
    prediction: int
    status: str
