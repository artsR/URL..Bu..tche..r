from django.apps import AppConfig



class UrlbutcherConfig(AppConfig):
    name = 'urlbutcher'

    def ready(self):
        import urlbutcher.signals
