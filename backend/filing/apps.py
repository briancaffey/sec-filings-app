from django.apps import AppConfig


class FilingConfig(AppConfig):
    name = "filing"

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import filing.signals
