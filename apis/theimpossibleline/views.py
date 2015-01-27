from django.conf import settings
from django.views.decorators.http import require_http_methods
from apis.theimpossibleline.engines import EngineFactory


@require_http_methods(["GET"])
def info(request):
    engine = EngineFactory.get_engine(request)
    return engine.info()

