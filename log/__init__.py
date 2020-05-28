from .log_config import Log


def info(msg: str) -> None: Log(msg).log_info()


def error(msg: str) -> None: Log(msg).log_error()


def critical(msg: str) -> None: Log(msg).log_critical()
