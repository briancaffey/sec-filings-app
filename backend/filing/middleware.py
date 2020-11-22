from filing.models import FilingList


class PeriodMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        period = view_kwargs.get("period", None)
        if period:
            period = FilingList.objects.filter(quarter=period).first()
            request.period = period
