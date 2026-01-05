from django.apps import AppConfig
import os

class SensorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sensors"

    def ready(self):
        if not os.environ.get("RENDER"):
            return

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()

            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="admin123"
                )
        except Exception:
            # Avoid crashing Gunicorn
            pass
