from django.views import generic
from . import models


class BlogIndex(generic.ListView):
    queryset = models.BlogEntry.objects.published()
    template_name = 'blog/index.html'
    paginate_by = 2


class BlogPostDetail(generic.DetailView):
    model = models.BlogEntry
    template_name = 'blog/details.html'


class TagDetail(generic.ListView):
    model = models.BlogEntry
    template_name = 'blog/tag_details.html'

    def get_queryset(self):
        queryset = models.BlogEntry.objects.filter(tags__slug=self.kwargs['tag'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TagDetail, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context