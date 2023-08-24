import boto3

from dependency_injector import containers, providers

from app.settings.config import configs
from app.fraud.repository.transaction import TransactionRepository, AnalysisRepository
from app.fraud.services.transaction import TransactionService, AnalysisService

from app.shared.core.database import Database


class FraudContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.fraud.api.v1.endpoints.transaction",
            "app.fraud.core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    storage = providers.Factory(
        boto3.client,
        service_name="s3",
        endpoint_url=configs.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=configs.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=configs.AWS_SECRET_ACCESS_KEY,
    )

    transaction_repository = providers.Factory(
        TransactionRepository, session_factory=db.provided.session
    )
    analysis_repository = providers.Factory(
        AnalysisRepository, session_factory=db.provided.session
    )

    transaction_service = providers.Factory(
        TransactionService, transaction_repository=transaction_repository
    )
    analysis_service = providers.Factory(
        AnalysisService, analysis_repository=analysis_repository
    )
