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
