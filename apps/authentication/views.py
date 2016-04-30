import logging
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

log = logging.getLogger(__name__)


@sensitive_post_parameters('password')
def login_override(request):
    redirect_url = request.GET.get('next', '')
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                log.debug('User %s logged in' % username)
                messages.success(request, 'You successfully logged in!')
                if redirect_url:
                    return HttpResponseRedirect(redirect_url)
                return HttpResponseRedirect('/')
            else:
                log.debug('Tried to login non active user: %s' % username)
                messages.error(request, 'Something went wrong!')
        else:
            messages.error(request, 'Wrong username or password!')
    else:
        # Some redirect to previous page here
        pass
    return render(request, 'authentication/login.html', {'request': request})


def logout_override(request):
    logout(request)
    log.debug('Logged out user')
    messages.success(request, 'You successfully logged out!')
    return HttpResponseRedirect('/')
