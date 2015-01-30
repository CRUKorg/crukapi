from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from apis.models import RequestLogV1
from portal.forms import PortalLoginForm


def hello_world(request):
    return HttpResponse("Hello World!!")


@login_required()
def portal_home(request):
    template_data = {
        'total_api_requests': RequestLogV1.objects.all().count()}
    return render(request, 'portal/pages/portal_home.html', template_data)


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