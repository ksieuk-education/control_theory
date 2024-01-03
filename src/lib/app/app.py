import logging
import logging.config as logging_config
import sys
import typing

import PyQt6.QtWidgets as pyqt6_qtwidgets

import lib.app.settings as app_settings
import lib.app.split_settings as app_split_settings
import lib.ui.services as _ui_services

logger = logging.getLogger(__name__)


class Application:
    def __init__(
        self,
        settings: app_settings.Settings,
        qapplication: pyqt6_qtwidgets.QApplication,
        ui_service: _ui_services.UiService,
    ) -> None:
        self._settings = settings
        self._qapplication = qapplication
        self._ui_service = ui_service

    @classmethod
    def from_settings(cls, settings: app_settings.Settings) -> "Application":
        # Logging

        logging_config.dictConfig(app_split_settings.get_logging_config(**settings.logger.model_dump()))

        logger.info("Initializing application")

        # Clients

        logger.info("Initializing clients")
        qapplication = pyqt6_qtwidgets.QApplication(sys.argv)

        # Services

        logger.info("Initializing services")
        ui_service = _ui_services.UiService(settings=settings.ui)

        application = Application(
            settings=settings,
            qapplication=qapplication,
            ui_service=ui_service,
        )

        logger.info("Initializing application finished")

        return application

    def start(self) -> None:
        self._ui_service.show()
        self._qapplication.exec()

    def dispose(self) -> None:
        pass
