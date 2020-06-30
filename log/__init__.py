from .logConfig import LogConfig


def info(msg: str) -> None: LogConfig(msg).log_info()


def error(msg: str) -> None: LogConfig(msg).log_error()


def critical(msg: str) -> None: LogConfig(msg).log_critical()
