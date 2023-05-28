from apps.base.models import WeekDay


class CreateDefaultModelsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._create_week_days()
        response = self.get_response(request)
        return response

    @staticmethod
    def _create_week_days():
        week_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                     "Saturday", "Sunday"]
        for idx, title in enumerate(week_list, start=1):
            WeekDay.objects.get_or_create(title=title, position=idx)
