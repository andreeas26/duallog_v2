import logging
import pathlib as pt
import pytest

from datetime import datetime


class TestDualLogger:    
    @pytest.mark.parametrize("name", ["test", "test2"])
    def test_get_logger(self, dual_logger, name):
        assert dual_logger.get_logger(name).name == name
    
    def test_dual_logger(self, dual_logger):
        assert dual_logger.main_logger.name == "root"
        assert dual_logger.main_logger.level == logging.DEBUG
        assert dual_logger.logs_dir == pt.Path("mylogs")
        assert dual_logger.min_level == logging.WARNING
        assert dual_logger.file_handler.level == logging.DEBUG
        assert dual_logger.console_handler.level == logging.WARNING
        assert dual_logger.file_handler.formatter._fmt == "%(asctime)s:[%(levelname)s]: %(name)s - %(funcName)s:%(lineno)d: %(message)s"
        assert dual_logger.console_handler.formatter._fmt == "[%(levelname)s]: %(name)s - %(funcName)s:%(lineno)d: %(message)s"
    
    @pytest.mark.parametrize("level", [logging.INFO, logging.ERROR])
    def test_set_file_handler_level(self, dual_logger, level):
        dual_logger.set_file_handler_level(level)
        assert dual_logger.file_handler.level == level
    
    @pytest.mark.parametrize("format", ["%(asctime)s - %(message)s", None])
    def test_set_file_handler_format(self, dual_logger, format):
        dual_logger.set_file_handler_format(format)
        assert dual_logger.file_handler.formatter._fmt == logging.Formatter(format)._fmt
    
    @pytest.mark.parametrize("level", [logging.INFO, logging.ERROR])
    def test_set_console_handler_level(self, dual_logger, level):
        dual_logger.set_console_handler_level(level)
        assert dual_logger.console_handler.level == level
    
    @pytest.mark.parametrize("format", ["%(asctime)s - %(message)s", None])
    def test_set_console_handler_format(self, dual_logger, format):
        dual_logger.set_console_handler_format(format)
        assert dual_logger.console_handler.formatter._fmt == logging.Formatter(format)._fmt

    def test_logging(self, dual_logger):
        logger = dual_logger.get_logger(__name__)
        logger.debug("debug message")
        logger.info("info message")
        logger.warning("warning message")
        logger.error("error message")

        latest_log_file = [*dual_logger.logs_dir.glob("*.log")]

        assert len(latest_log_file) != 0, "No log file found."
        latest_log_file = sorted(latest_log_file)[-1]

        assert datetime.now().strftime("%Y-%m-%d") in latest_log_file.name

        with open(latest_log_file, "r") as f:
            lines = [line.strip("\n") for line in f.readlines()]

            assert f"[DEBUG]: {__name__} - test_logging:" in lines[0]
            assert "debug message" in lines[0]
            assert f"[INFO]: {__name__} - test_logging:" in lines[1]
            assert "info message" in lines[1]
            assert f"[WARNING]: {__name__} - test_logging:" in lines[2]
            assert "warning message" in lines[2]
            assert f"[ERROR]: {__name__} - test_logging:" in lines[3]
            assert "error message" in lines[3]
