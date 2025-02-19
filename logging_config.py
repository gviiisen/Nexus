# coding=utf-8
import datetime
import io
import json
import logging
from logging import addLevelName, handlers
import os
import sys
import traceback
import colorlog
from filelock import FileLock

logger = logging.getLogger()
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
_levelToName = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG",
    NOTSET: "NOTSET",
}
_nameToLevel = {
    "CRITICAL": CRITICAL,
    "FATAL": FATAL,
    "ERROR": ERROR,
    "WARN": WARNING,
    "WARNING": WARNING,
    "INFO": INFO,
    "DEBUG": DEBUG,
    "NOTSET": NOTSET,
}


def rewrite_logging():
    origin_info = logging.info
    origin_warning = logging.warning
    origin_error = logging.error

    def info(*args):
        args = [str(x) for x in args]
        origin_info("".join(args))

    def warning(*args):
        args = [str(x) for x in args]
        origin_warning("".join(args))

    def error(*args):
        args = [str(x) for x in args]
        origin_error("".join(args))

    logging.info = info
    logging.warning = warning
    logging.error = error


def hidden_debug_logger():

    def _log(
        level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1
    ):

        sinfo = None
        _srcfile = os.path.normcase(addLevelName.__code__.co_filename)
        if _srcfile:
            # IronPython doesn't track Python frames, so findCaller raises an
            # exception on some versions of IronPython. We trap it here so that
            # IronPython can use logging.
            try:
                f = sys._getframe(1).f_back
                if level != DEBUG:
                    f = f.f_back.f_back
                # On some versions of IronPython, currentframe() returns None if
                # IronPython isn't run with -X:Frames.
                if f is None:
                    fn, lno, func, sinfo = (
                        "(unknown file)",
                        0,
                        "(unknown function)",
                        None,
                    )
                co = f.f_code
                sinfo = None
                if stack_info:
                    with io.StringIO() as sio:
                        sio.write("Stack (most recent call last):\n")
                        traceback.print_stack(f, file=sio)
                        sinfo = sio.getvalue()
                        if sinfo[-1] == "\n":
                            sinfo = sinfo[:-1]
                fn, lno, func, sinfo = co.co_filename, f.f_lineno, co.co_name, sinfo
            except ValueError:  # pragma: no cover
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:  # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        filename = fn.split("\\")
        filename = filename[len(filename) - 1]
        filename = filename.split("/")
        filename = filename[len(filename) - 1]
        msg = (
            f"[{datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S,%f')[:-3]}] [{_levelToName[level]}] [{filename}:{lno}] "
            + msg
        )
        msg = (
            msg.encode("utf-8")
            .decode("utf-8")
            .encode("gbk", "ignore")
            .decode("gbk")
            .encode("utf-8")
            .decode("utf-8")
        )
        record = logger.makeRecord(
            logger.name, level, fn, lno, msg, args, exc_info, func, extra, sinfo
        )
        logger.handle(record)

    origin_getLogger = logging.getLogger
    logger._log = _log

    def getLogger(name=None):
        logger = origin_getLogger(name)
        logger._log = _log
        return logger

    logging.getLogger = getLogger



def init_log():
    # 创建日志目录
    log_dir = os.path.abspath("../log")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 日志文件路径
    log_file = os.path.join(log_dir, "bot.log")
    log_lock_file = os.path.join(log_dir, "bot.lock")

    # 重置 logger
    rewrite_logging()
    hidden_debug_logger()

    for h in logger.handlers:
        logger.removeHandler(h)

    # 设置日志格式（带颜色的，用于控制台）
    console_fmt = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            "DEBUG": "fg_thin_cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        },
        style="%",
    )

    # 设置无颜色格式（用于文件）
    file_fmt = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 文件日志处理器，添加文件锁
    with FileLock(log_lock_file):
        file_handler = handlers.TimedRotatingFileHandler(
            filename=log_file, when="D", interval=1, backupCount=3, encoding="utf-8", delay=True
        )
    file_handler.setFormatter(file_fmt)
    file_handler.setLevel(logging.INFO)

    # 控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_fmt)
    console_handler.setLevel(logging.INFO)

    # 配置 Logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

    logging.info("[INIT] logger ready .....")