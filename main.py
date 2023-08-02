import sentry_sdk
import app.models
from configparser import ConfigParser
from app.controllers.first_init_database.check_empty_db import check_administrator_existence
from app.controllers.first_init_database.create_first_admin import create_first_administrator
from app.controllers.cli_controller import cli


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')

    sentry_dsn = config.get('sentry', 'dsn', raw=True)

    sentry_sdk.init(
        dsn=sentry_dsn,

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
