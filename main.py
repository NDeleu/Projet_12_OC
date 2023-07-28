import sentry_sdk
import app.models
from app.controllers.first_init_database.check_empty_db import check_administrator_existence
from app.controllers.first_init_database.create_first_admin import create_first_administrator
from app.controllers.cli_controller import cli


if __name__ == '__main__':
    sentry_sdk.init(
        dsn="https://93a5e8099f404fb2ab2dc4c47dfcdecf@o4505604593876992.ingest.sentry.io/4505604598202368",

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )

    session = app.models.session

    if check_administrator_existence():
        cli(obj=session)

    else:
        create_first_administrator()
        cli(obj=session)
