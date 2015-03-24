from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from apis.models import RequestLogV1
from portal.forms import PortalLoginForm


def hello_world(request):
    return HttpResponse("Hello World!!")


@login_required()
def portal_home(request):
    return redirect('portal_api_theimpossibleline')


@login_required()
def api_theimpossibleline(request):
    requests = RequestLogV1.objects.filter(project="theimpossibleline")
    template_data = {
        'total_registrations': requests.filter(path=reverse("api_projects_impossible_line_signup")).count(),
        'total_api_requests': requests.count()}
    return render(request, 'portal/pages/apis/theimpossibleline.html', template_data)


def portal_login(request):
    if request.user.is_authenticated():
        return redirect('portal_home')
    form = PortalLoginForm(initial=request.GET)
    if request.method == "POST":
        form = PortalLoginForm(request.POST, request=request)
        if form.is_valid():  # This calls user validation and login
            return redirect('portal_home')
    template_data = {'form': form}
    return render(request, 'portal/pages/login.html', template_data)