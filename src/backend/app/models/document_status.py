from enum import Enum

class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    EMBEDDED = "EMBEDDED"
    READY = "READY"
    FAILED = "FAILED"