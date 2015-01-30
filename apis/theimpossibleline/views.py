from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from apis.theimpossibleline.engines import EngineFactory


@require_http_methods(["GET", "POST"])
@csrf_exempt
def proxy(request):
    engine = EngineFactory.get_engine(request)
    return engine.proxy()

