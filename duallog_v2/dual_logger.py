#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Duallog

This module contains a function "setup()" that sets up dual logging. 
All subsequent log messages are sent both to the console and to a logfile. 
Log messages are generated via the "logging" package.

Example:
    >>> import duallog
    >>> import logging
    >>> duallog.setup("mylogs")
    >>> logging.info("Test message")

If run, this module illustrates the usage of the duallog package.
"""


# Import required standard packages.

import logging
import pathlib as pt
import sys


from datetime import datetime
from logging import config

# Define default logfile format.
FILE_NAME_FORMAT = "{year:04d}-{month:02d}-{day:02d}-"\
    "{hour:02d}-{minute:02d}-{second:02d}.log"

# Define the default logging message formats.
FILE_MSG_FORMAT = "%(asctime)s:[%(levelname)s]: %(name)s - %(funcName)s:%(lineno)d: %(message)s"
CONSOLE_MSG_FORMAT ="[%(levelname)s]: %(name)s - %(funcName)s:%(lineno)d: %(message)s"


class DualLogger:
    """Set up dual logging to console and to logfile.
    
    
    When this function is called, it first creates the given logging output directory.
    It then creates a logfile and passes all log messages to come to it.
    
    Args:
        config_file: path to the configuration file. Defaults to None.
        logs_dir: path of the directory where to store the log files. Both a
            relative or an absolute path may be specified. If a relative path is
            specified, it is interpreted relative to the working directory.
            Defaults to "logs".
        min_level: defines the minimum level of the messages that will be shown. Defaults to WARNING.
    """

    def __init__(self, config_file:pt.Path | None=None, logs_dir:pt.Path="logs", min_level:int=logging.WARNING):

        self.logs_dir = pt.Path(logs_dir)
        self.min_level = min_level
        self.config_file = config_file

        # Create a folder for the logfiles.
        if not self.logs_dir.exists():
            self.logs_dir.mkdir(parents=True)

        # Set up dual logging.
        if config_file is None:
            self.default_setup()
        else:
            self.config_setup(config_file)

    def default_setup(self):
        # Create the root logger.
        self.main_logger = logging.getLogger()
        self.main_logger.setLevel(logging.DEBUG)

        # Construct the name of the logfile.
        t = datetime.now()
        file_name = FILE_NAME_FORMAT.format(year=t.year, month=t.month, day=t.day,
            hour=t.hour, minute=t.minute, second=t.second)
        file_name = self.logs_dir/file_name

        # Set up logging to the logfile.
        self.file_handler = logging.FileHandler(filename=file_name)
        self.file_handler.setLevel(logging.DEBUG)
        self.file_formatter = logging.Formatter(FILE_MSG_FORMAT)
        self.file_handler.setFormatter(self.file_formatter)
        self.main_logger.addHandler(self.file_handler)

        # Set up logging to the console.
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setLevel(self.min_level)
        self.console_formatter = logging.Formatter(CONSOLE_MSG_FORMAT)
        self.console_handler.setFormatter(self.console_formatter)
        self.main_logger.addHandler(self.console_handler)
    
    def config_setup(self, config_file:pt.Path):
        # Set up logging configuration. 
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        config.fileConfig(config_file, defaults={"logs_dir": self.logs_dir, "date": datetime.now().strftime("%Y-%m-%d-%H-%M-%S")})
        self.main_logger = logging.getLogger()
        self.console_handler = self.main_logger.handlers[0]
        self.console_formatter = self.console_handler.formatter
        self.file_handler = self.main_logger.handlers[1]
        self.file_formatter = self.file_handler.formatter
    
    def get_logger(self, name:str):
        return self.main_logger.getChild(name)
        
    def set_file_handler_level(self, level:int):
        self.file_handler.setLevel(level)
    
    def set_file_handler_format(self, format:str | None):
        self.file_handler.setFormatter(logging.Formatter(format))
    
    def set_console_handler_level(self, level:int):
        self.console_handler.setLevel(level)
    
    def set_console_handler_format(self, format:str | None):
        self.console_handler.setFormatter(logging.Formatter(format))


if __name__ == "__main__":
    """Illustrate the usage of the duallog package.
    """

    # Set up dual logging.
    # dual_logger = DualLogger("../mylogs")
    dual_logger = DualLogger("../example_config.ini", logs_dir="mylogs")
    logger = dual_logger.get_logger(__name__)

    # Generate some log messages.
    logger.debug("Debug messages are only sent to the logfile.")
    logger.info("Info messages are not shown on the console, too.")
    logger.warning("Warnings appear both on the console and in the logfile.")
    logger.error("Errors get the same treatment.")
    logger.critical("And critical messages, of course.")
