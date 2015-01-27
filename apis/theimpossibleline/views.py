from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def info(request):
    pass