from django.core.paginator import Paginator

from yatube.settings import POST_PER_PAGE


def sort_post_per_page(posts):
    paginator = Paginator(posts, POST_PER_PAGE)
    return paginator
