from fastapi import APIRouter

from app.fraud.api.v1.endpoints import transaction_router

routers = APIRouter()
router_list = [transaction_router]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)
