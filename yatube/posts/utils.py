from django.core.paginator import Paginator
from django.conf import settings


def paginate_objects(posts, request):
    page_number = request.GET.get('page')
    paginator = Paginator(posts, settings.POST_PER_PAGE)
    page_obj = paginator.get_page(page_number)
    return page_obj
