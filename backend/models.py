from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ExecutionStatus(BaseModel):
    execution_id: str
    status: str
    total_hosts: int
    completed_hosts: int
    successful_hosts: int
    failed_hosts: int
    start_time: datetime
    end_time: Optional[datetime]
