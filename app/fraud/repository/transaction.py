from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.fraud.model import Transaction, TransactionAnalysis

from app.shared.repository.base_repository import BaseRepository


class TransactionRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Transaction)


class AnalysisRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, TransactionAnalysis)
