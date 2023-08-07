from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.analytics.core.container import AnalyticsContainer
from app.analytics.core.dependencies import get_current_active_user
from app.analytics.model.user import User
from app.analytics.schema.post_tag_schema import FindTag, FindTagResult, Tag, UpsertTag
from app.analytics.services.tag_service import TagService

from app.shared.schema.base_schema import Blank

router = APIRouter(
    prefix="/tag",
    tags=["tag"],
)


@router.get("", response_model=FindTagResult)
@inject
async def get_tag_list(
    find_query: FindTag = Depends(),
    service: TagService = Depends(Provide[AnalyticsContainer.tag_service]),
):
    return service.get_list(find_query)


@router.get("/{tag_id}", response_model=Tag)
@inject
async def get_tag(
    tag_id: int,
    service: TagService = Depends(Provide[AnalyticsContainer.tag_service]),
):
    return service.get_by_id(tag_id)


@router.post("", response_model=Tag)
@inject
async def create_tag(
    tag: UpsertTag,
    service: TagService = Depends(Provide[AnalyticsContainer.tag_service]),
    current_user: User = Depends(get_current_active_user),
):
    return service.add(tag)


@router.patch("/{tag_id}", response_model=Tag)
@inject
async def update_tag(
    tag_id: int,
    tag: UpsertTag,
    service: TagService = Depends(Provide[AnalyticsContainer.tag_service]),
    current_user: User = Depends(get_current_active_user),
):
    return service.patch(tag_id, tag)


@router.delete("/{tag_id}", response_model=Blank)
@inject
async def delete_tag(
    tag_id: int,
    service: TagService = Depends(Provide[AnalyticsContainer.tag_service]),
    current_user: User = Depends(get_current_active_user),
):
    return service.remove_by_id(tag_id)
