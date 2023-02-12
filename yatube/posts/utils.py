from django.core.paginator import Paginator
from django.conf import settings


def get_page(queryset, request):
    paginator = Paginator(queryset, settings.NUMBER_OF_POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return page_obj
