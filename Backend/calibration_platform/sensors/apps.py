from django.apps import AppConfig
import os

class SensorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sensors"

    def ready(self):
        # Run only on Render
        if os.environ.get("RENDER") != "true":
            return

        try:
            from django.core.management import call_command
            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='sensors_sensor';"
                )
                table_exists = cursor.fetchone()[0]

            if not table_exists:
                return

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM sensors_sensor;")
                count = cursor.fetchone()[0]

            if count == 0:
                call_command("loaddata", "sensors.json", verbosity=0)

        except Exception as e:
            print("Sensor auto-load skipped:", e)
