import warnings

from loguru import logger
from rich.logging import RichHandler

logger = logger.bind(name="plateaukit")

logger.configure(
    handlers=[
        {
            "sink": RichHandler(markup=True),
            "format": "{message}",
            "level": "INFO",
        }
    ]
)


# https://loguru.readthedocs.io/en/stable/resources/recipes.html#capturing-standard-stdout-stderr-and-warnings
def capture_warnings():
    global warnings
    showwarning_ = warnings.showwarning

    def showwarning(message, *args, **kwargs):
        logger.debug(message)
        # showwarning_(message, *args, **kwargs)

    warnings.showwarning = showwarning


capture_warnings()


def set_log_level(level: str):
    """Set the log level.

    Args:
        level: Log level
    """
    logger.configure(
        handlers=[
            {"sink": RichHandler(markup=True), "format": "{message}", "level": level}
        ]
    )
