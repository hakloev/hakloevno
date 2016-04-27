from django.shortcuts import render


def home_files(request, file_name):
    """
    Function for returning home files (humans||robots.txt)
    """
    return render(request, file_name, {}, content_type='text/plain')