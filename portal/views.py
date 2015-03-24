import json
import datetime
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
    def create_chart_data(sequence):
        chart_data = [['Day', 'Requests']]
        if not sequence:
            return chart_data
        min_date = sorted(sequence, key=lambda x: x['day'])[0]['day']
        if type(min_date) is not datetime.date:
            min_date = datetime.datetime.strptime(min_date, "%Y-%m-%d")
        max_date = sorted(sequence, key=lambda x: x['day'], reverse=True)[0]['day']
        if type(max_date) is not datetime.date:
            max_date = datetime.datetime.strptime(max_date, "%Y-%m-%d")
        sequence_dict = {}
        for s in sequence:
            sequence_dict[s['day']] = s['count']
        new_sequence = []
        while min_date <= max_date:
            key = min_date.strftime("%Y-%m-%d")
            new_sequence.append({'day': key, 'count': sequence_dict.get(key, 0)})
            min_date += datetime.timedelta(days=1)
        for s in new_sequence:
            chart_data.append(["%s" % str(s['day']), s['count']])
        return chart_data

    requests = RequestLogV1.objects.filter(project="theimpossibleline").order_by("created")
    requests_by_day = requests.extra(select={'day': 'date(created)'}).values('day').annotate(count=Count('created'))
    request_chart_data = create_chart_data(requests_by_day)

    registration_requests = requests.filter(path=reverse("api_projects_impossible_line_signup"))
    registrations_by_day = registration_requests.extra(select={'day': 'date(created)'}).values('day').annotate(count=Count('created'))
    registrations_chart_data = create_chart_data(registrations_by_day)

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