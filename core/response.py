from django.core.paginator import Paginator
from django.db.models import QuerySet

from core.schemas import PageSchema, GenericResultsType
from core.schemas import PageFilter


def get_page(
        qs: QuerySet,
        f: PageFilter,
        t: GenericResultsType) -> PageSchema:
    p = Paginator(qs, per_page=f.page_size).get_page(f.page_index)
    return PageSchema[t](
        total=p.paginator.count,
        page_size=p.paginator.per_page,
        page_index=p.number,
        details=list(p.object_list),
    )
