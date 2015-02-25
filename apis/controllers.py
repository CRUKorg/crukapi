from apis.decorators import async
from apis.models import RequestLogV1


class RequestLogController(object):

    @classmethod
    @async
    def log_request_async(cls, project, request):
        yield
        cls.log_request(project, request)

    @classmethod
    def log_request(cls, project, request):
        log_entry = RequestLogV1(project=project, path=request.path)
        log_entry.save()
        log_entry.add_attributes(request.GET if request.method == "GET" else request.POST)
