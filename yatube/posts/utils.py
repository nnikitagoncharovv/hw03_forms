from django.core.paginator import Paginator


def get_page(queryset, page: int, per_page: int):
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    return page_obj
