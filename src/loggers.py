import logging
import logging.config
import pathlib
from datetime import datetime
from typing import Union

import yaml


class DatedFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", encoding=None, delay=False, errors=None):
        dated_filename = datetime.utcnow().strftime(str(filename))
        pathlib.Path(dated_filename).parent.mkdir(parents=True, exist_ok=True)
        super().__init__(
            dated_filename,
            mode=mode,
            encoding=encoding,
            delay=delay,
            errors=errors,
        )


class ProjectPathFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        path = pathlib.Path(record.pathname)
        cwd = path.cwd()
        try:
            project_path = str(path.relative_to(cwd))
        except ValueError:  # Fix for logger inside docker image
            project_path = None
        record.projectpath = project_path
        return super().format(record=record)


def configure_logging_from_yaml_file(file_name: Union[str, pathlib.Path] = "logging.yaml") -> None:
    if not isinstance(file_name, pathlib.Path):
        file_name = pathlib.Path(file_name)
    yaml_object = yaml.safe_load(file_name.read_text())
    logging.config.dictConfig(yaml_object)


def get_logger_file_date() -> str:
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.FileHandler):
            file_date = pathlib.Path(handler.baseFilename).stem.split("_")
            return "_".join(file_date[:2])
    return ""
