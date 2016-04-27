from django.contrib.syndication.views import Feed
from .models import BlogEntry


class LatestPosts(Feed):
    title = 'Hakloev Blog'
    link = '/feed/'
    description = 'Latest Posts'

    def items(self):
        return BlogEntry.objects.published()[:5]