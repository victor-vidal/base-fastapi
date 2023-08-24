from app.fraud.repository import TransactionRepository, AnalysisRepository

from app.shared.services.base_service import BaseService


class TransactionService(BaseService):
    def __init__(
        self,
        transaction_repository: TransactionRepository,
    ):
        self.transaction_repository = transaction_repository
        super().__init__(transaction_repository)


class AnalysisService(BaseService):
    def __init__(
        self,
        analysis_repository: AnalysisRepository,
    ):
        self.analysis_repository = analysis_repository
        super().__init__(analysis_repository)
