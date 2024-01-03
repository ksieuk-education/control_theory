import logging
import os

import lib.app as app

logger = logging.getLogger(__name__)


def run() -> None:
    settings = app.Settings()
    application = app.Application.from_settings(settings)

    try:
        application.start()
    finally:
        application.dispose()


def main() -> None:
    # try:
        run()
        # exit(os.EX_OK)
    # except SystemExit:
    #     exit(os.EX_OK)
    # # except app.ApplicationError:
    # #     exit(os.EX_SOFTWARE)
    # except KeyboardInterrupt:
    #     logger.info("Exited with keyboard interruption")
    #     exit()
    # except BaseException:
    #     logger.exception("Unexpected error occurred")
    #     exit()
    # except:
    #     pass


if __name__ == "__main__":
    main()
