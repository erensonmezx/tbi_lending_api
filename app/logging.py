import logging
import os
import uuid
from typing import Optional
from fastapi import Request

CORRELATION_HEADER = "x-correlation-id"

def setup_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s correlation_id=%(correlation_id)s %(message)s",
    )

def get_or_create_correlation_id(request: Request) -> str:
    cid: Optional[str] = request.headers.get(CORRELATION_HEADER)
    return cid or str(uuid.uuid4())
