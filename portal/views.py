import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
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
    requests_by_day = requests.extra(select={'day': 'date(created)'}).values('day').annotate(count=Count('created'))
    request_chart_data = [['Day', 'Classifications']]
    for classification_by_day in requests_by_day:
        request_chart_data.append(["%s" % str(classification_by_day['day']), classification_by_day['count']])

    registration_requests = requests.filter(path=reverse("api_projects_impossible_line_signup"))
    registrations_by_day = requests.extra(select={'day': 'date(created)'}).values('day').annotate(count=Count('created'))
    registrations_chart_data = [['Day', 'Classifications']]
    for classification_by_day in registrations_by_day:
        registrations_chart_data.append(["%s" % str(classification_by_day['day']), classification_by_day['count']])

    template_data = {
        'total_registrations': registration_requests.count(),
        'total_api_requests': requests.count(),
        'chart_requests_over_time': json.dumps(request_chart_data),
        'chart_registrations_over_time': json.dumps(registrations_chart_data)}
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