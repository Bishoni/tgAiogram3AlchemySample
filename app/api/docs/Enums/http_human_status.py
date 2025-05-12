from enum import Enum


class HttpHumanStatusCode(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
