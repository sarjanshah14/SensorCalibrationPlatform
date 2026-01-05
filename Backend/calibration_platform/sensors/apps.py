from django.apps import AppConfig
import os

class SensorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sensors"

    def ready(self):
        # Only run on Render
        if os.environ.get("RENDER") != "true":
            return

        try:
            from django.core.management import call_command
            from django.db import connection

            def table_exists(table_name):
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=%s;",
                        [table_name],
                    )
                    return cursor.fetchone()[0] == 1

            def table_is_empty(table_name):
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                    return cursor.fetchone()[0] == 0

            # Order MATTERS (foreign keys)
            fixtures = [
                ("sensors_sensor", "sensors.json"),
                ("sensors_reading", "readings.json"),
                ("sensors_calibration", "calibrations.json"),
                ("sensors_anomaly", "anomalies.json"),
            ]

            for table, fixture in fixtures:
                if table_exists(table) and table_is_empty(table):
                    call_command("loaddata", fixture, verbosity=0)

        except Exception as e:
            print("Auto-load skipped:", e)
