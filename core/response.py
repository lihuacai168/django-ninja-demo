"""分页核心函数"""
from django.core.paginator import Paginator
from django.db.models import QuerySet

from core.schemas import PageSchema, GenericResultsType
from core.schemas import PageFilter


def get_page(
        queryset: QuerySet,
        pager_filter: PageFilter,
        generic_result_type: GenericResultsType) -> PageSchema:
    """标准分页"""
    p = Paginator(queryset, per_page=pager_filter.page_size).get_page(pager_filter.page_index)
    return PageSchema[generic_result_type](
        total=p.paginator.count,
        page_size=p.paginator.per_page,
        page_index=p.number,
        details=list(p.object_list),
    )
