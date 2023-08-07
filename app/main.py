from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.analytics.api.v1.routes import routers as v1_routers
from app.analytics.core.container import AnalyticsContainer

from app.settings.config import configs
from app.shared.util.class_object import singleton


@singleton
class AppCreator:
    def __init__(self):
        # set app default
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            openapi_url=f"{configs.API}/openapi.json",
            version="0.0.1",
        )

        # set db and container
        self.analytics_container = AnalyticsContainer()
        self.analytics_db = self.analytics_container.db()
        # self.db.create_database()

        # set cors
        if configs.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # set routes
        @self.app.get("/")
        def root():
            return "service is working"

        self.app.include_router(v1_routers, prefix=configs.API_V1_STR)


app_creator = AppCreator()
app = app_creator.app
analytics_db = app_creator.analytics_db
analytics_container = app_creator.analytics_container
