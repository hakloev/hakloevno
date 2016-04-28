from django.shortcuts import render
from apps.blog.models import BlogEntry


def home_files(request, file_name):
    """
    Function for returning home files (humans||robots.txt)
    """
    return render(request, file_name, {}, content_type='text/plain')


def index(request):
    blog_entries = BlogEntry.objects.published()[:5]
    return render(request, template_name='index.html', context={
        'blog_entries': blog_entries
    })
