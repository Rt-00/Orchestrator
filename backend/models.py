from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from settings import settings


class HostConfig(BaseModel):
    hostname: str
    port: int = 22
    username: str
    password: str


class ExecutionRequest(BaseModel):
    hosts: List[HostConfig]
    script: str

    timeout_seconds: int = Field(
        default=settings.SSH_DEFAULT_TIMEOUT, ge=1, le=settings.SSH_MAX_TIMEOUT
    )

    max_concurrent: int = Field(
        default=settings.MAX_CONCURRENT_DEFAULT, ge=1, le=settings.MAX_CONCURRENT_LIMIT
    )


class ExecutionStatus(BaseModel):
    execution_id: str
    status: str
    total_hosts: int
    completed_hosts: int
    successful_hosts: int
    failed_hosts: int
    start_time: datetime
    end_time: Optional[datetime]
