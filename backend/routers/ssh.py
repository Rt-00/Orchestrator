from fastapi import APIRouter, HTTPException

from models import ExecutionStatus
from storage import (
    delete_execution_data,
    get_execution,
    get_results,
    list_all_executions,
)

router = APIRouter(tags=["SSH"])


@router.get("/status/{execution_id}", response_model=ExecutionStatus)
async def get_execution_status(execution_id: str):
    """Get the status of an execution"""
    execution = get_execution(execution_id)

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found.")

    return execution


@router.get("/results/{execution_id}")
async def get_execution_results(execution_id: str):
    """Get the results of an execution"""
    execution_results = get_results(execution_id)

    if not execution_results:
        raise HTTPException(status_code=404, detail="Results not found")

    return execution_results


@router.get("/executions")
async def list_executions():
    """List all executions"""
    return list_all_executions()


@router.delete("/executions/{execution_id}")
async def delete_execution(execution_id: str):
    """Delete an execution and its results"""
    delete_execution_data(execution_id)
    return {"message": "Execution deleted"}
