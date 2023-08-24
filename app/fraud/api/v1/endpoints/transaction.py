import pandas as pd
import joblib
from io import BytesIO

from typing import List
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from boto3.session import Session

from app.fraud.core.container import FraudContainer

from app.fraud.services.transaction import TransactionService, AnalysisService
from app.fraud.schema.transaction import (
    Transaction,
    TransactionAnalysis,
)
from app.shared.schema.base_schema import FindBase
from app.settings.config import configs


router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
)


def predict(model, data):
    df = pd.DataFrame(data)

    # Drop columns that are not suitable for classification
    columns_to_drop = [
        "id",
        "description",
        "same_holder",
        "currency",
        "transaction_time",
        "datetime_program",
        "customer_doc",
        "receptor_doc",
        "device_fingerprint",
        "device_timezone",
        "device_vendor",
        "device_version",
        "device_language",
        "device_user_agent",
        "device_model",
        "device_platform",
        "device_category",
        "device_ip",
        "device_memory",
        "device_cpu_count",
        "device_cookies_enabled",
        "device_screen_orientation",
    ]
    df = df.drop(columns=columns_to_drop, axis=1)

    return model.predict(df)


@router.get("", response_model=List[Transaction])
@inject
async def get_post_list(
    find_query: FindBase = Depends(),
    service: TransactionService = Depends(Provide[FraudContainer.transaction_service]),
):
    return service.get_list(find_query)["founds"]


@router.post("/predict_only/", response_model=TransactionAnalysis)
@inject
async def create_transaction(
    transaction: Transaction,
    storage: Session.client = Depends(Provide[FraudContainer.storage]),
):
    response = storage.get_object(
        Bucket=configs.AWS_STORAGE_BUCKET_NAME, Key="test_model/random_forest_model.pkl"
    )

    loaded_model = joblib.load(BytesIO(response["Body"].read()))

    transaction_dict = {
        "id": transaction.id,
        "description": transaction.description,
        "same_holder": transaction.same_holder,
        "currency": transaction.currency,
        "transaction_value": transaction.transaction_value,
        "transaction_time": transaction.transaction_time,
        "datetime_program": transaction.datetime_program,
        "customer_doc": transaction.customer_doc,
        "receptor_doc": transaction.receptor_doc,
        "device_fingerprint": transaction.device_fingerprint,
        "device_timezone": transaction.device_timezone,
        "device_vendor": transaction.device_vendor,
        "device_version": transaction.device_version,
        "device_language": transaction.device_language,
        "device_user_agent": transaction.device_user_agent,
        "device_model": transaction.device_model,
        "device_platform": transaction.device_platform,
        "device_category": transaction.device_category,
        "device_ip": transaction.device_ip,
        "device_longitude": transaction.device_longitude,
        "device_latitude": transaction.device_latitude,
        "device_memory": transaction.device_memory,
        "device_cpu_count": transaction.device_cpu_count,
        "device_cookies_enabled": transaction.device_cookies_enabled,
        "device_screen_resolution_x": transaction.device_screen_resolution_x,
        "device_screen_resolution_y": transaction.device_screen_resolution_y,
        "device_screen_orientation": transaction.device_screen_orientation,
    }

    prediction = predict(loaded_model, [transaction_dict])[0]

    return TransactionAnalysis(
        **{
            "client_id": 15,
            "model_id": "random_forest_model.pkl",
            "transaction_id": transaction.id,
            "prediction": prediction,
            "action": "ACCEPTED" if prediction == 0 else "REJECTED",
            "created_at": "2015-03-21T11:07:22.956087",
            "input_data": "",
        }
    )


@router.post("", response_model=TransactionAnalysis)
@inject
async def create_transaction(
    transaction: Transaction,
    transaction_service: TransactionService = Depends(
        Provide[FraudContainer.transaction_service]
    ),
    analysis_service: AnalysisService = Depends(
        Provide[FraudContainer.analysis_service]
    ),
    storage: Session.client = Depends(Provide[FraudContainer.storage]),
):
    transaction = transaction_service.add(transaction)

    response = storage.get_object(
        Bucket=configs.AWS_STORAGE_BUCKET_NAME, Key="test_model/random_forest_model.pkl"
    )

    loaded_model = joblib.load(BytesIO(response["Body"].read()))

    transaction_dict = {
        "id": transaction.id,
        "description": transaction.description,
        "same_holder": transaction.same_holder,
        "currency": transaction.currency,
        "transaction_value": transaction.transaction_value,
        "transaction_time": transaction.transaction_time,
        "datetime_program": transaction.datetime_program,
        "customer_doc": transaction.customer_doc,
        "receptor_doc": transaction.receptor_doc,
        "device_fingerprint": transaction.device_fingerprint,
        "device_timezone": transaction.device_timezone,
        "device_vendor": transaction.device_vendor,
        "device_version": transaction.device_version,
        "device_language": transaction.device_language,
        "device_user_agent": transaction.device_user_agent,
        "device_model": transaction.device_model,
        "device_platform": transaction.device_platform,
        "device_category": transaction.device_category,
        "device_ip": transaction.device_ip,
        "device_longitude": transaction.device_longitude,
        "device_latitude": transaction.device_latitude,
        "device_memory": transaction.device_memory,
        "device_cpu_count": transaction.device_cpu_count,
        "device_cookies_enabled": transaction.device_cookies_enabled,
        "device_screen_resolution_x": transaction.device_screen_resolution_x,
        "device_screen_resolution_y": transaction.device_screen_resolution_y,
        "device_screen_orientation": transaction.device_screen_orientation,
    }

    prediction = predict(loaded_model, [transaction_dict])[0]

    analysis = analysis_service.add(
        TransactionAnalysis(
            **{
                "client_id": 15,
                "model_id": "random_forest_model.pkl",
                "transaction_id": transaction.id,
                "prediction": prediction,
                "action": "ACCEPTED" if prediction == 0 else "REJECTED",
                "created_at": "2015-03-21T11:07:22.956087",
                "input_data": "",
            }
        )
    )

    return analysis
