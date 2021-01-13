from django.apps import AppConfig


class FoodConfig(AppConfig):
    name = 'Food'
    verbose_name = 'UserViews'

    def ready(self):
        import Food.signals
