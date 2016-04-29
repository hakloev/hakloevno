from django.views import generic
from . import models


class BlogIndex(generic.ListView):
    queryset = models.BlogEntry.objects.published()
    template_name = 'blog/index.html'
    paginate_by = 2


class BlogPostDetail(generic.DetailView):
    model = models.BlogEntry
    template_name = 'blog/details.html'

