from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.fraud.api.v1.routes import routers as v1_routers
from app.fraud.core.container import FraudContainer

from app.settings.config import configs
from app.shared.util.class_object import singleton
from app.shared.idp import FastAPIKeycloak


@singleton
class AppCreator:
    def __init__(self):
        # set app default
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            docs_url="/api/docs/swagger",
            redoc_url="/api/docs/redoc",
            openapi_url="/api/docs",
            version="0.0.1",
        )
        # self.idp = FastAPIKeycloak(
        #     server_url="http://127.0.0.1:8080/auth", # esse path tá errado
        #     client_id="internal",
        #     client_secret="KN5rAlD8IF74nrm5DfQP5nbfiav7yRbn",
        #     admin_client_secret="HgW92WSYUIwWGB2z2dR2ha46zmyJHwKB",
        #     realm="dev",
        #     callback_uri="http://127.0.0.1:8081/callback" # não sei qual seria esse
        # )

        # set db and container
        self.fraud_container = FraudContainer()
        self.fraud_db = self.fraud_container.db()
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
fraud_db = app_creator.fraud_db
fraud_container = app_creator.fraud_container
