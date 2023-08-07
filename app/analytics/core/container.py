from dependency_injector import containers, providers

from app.settings.config import configs
from app.analytics.repository import *
from app.analytics.services import *

from app.shared.core.database import Database

class AnalyticsContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.analytics.api.v1.endpoints.auth",
            "app.analytics.api.v1.endpoints.post",
            "app.analytics.api.v1.endpoints.tag",
            "app.analytics.api.v1.endpoints.user",
            "app.analytics.core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.ANALYTICS_DATABASE_URI)

    post_repository = providers.Factory(PostRepository, session_factory=db.provided.session)
    tag_repository = providers.Factory(TagRepository, session_factory=db.provided.session)
    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    post_service = providers.Factory(PostService, post_repository=post_repository, tag_repository=tag_repository)
    tag_service = providers.Factory(TagService, tag_repository=tag_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
