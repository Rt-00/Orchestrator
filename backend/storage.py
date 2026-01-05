from collections import defaultdict
from typing import Dict, List


# In-memory storage
executions: Dict[str, dict] = {}
results: Dict[str, List[dict]] = defaultdict(list)


def get_execution(execution_id: str) -> dict:
    """Get execution status by ID"""
    return executions.get(execution_id)


def get_results(execution_id: str) -> List[dict]:
    """Get execution results by ID"""
    return results.get(execution_id, [])


def list_all_executions() -> List[dict]:
    """List all executions"""
    return list(executions.values())


def delete_execution_data(execution_id: str):
    """Delete execution and its results"""
    if execution_id in executions:
        del executions[execution_id]
    if execution_id in results:
        del results[execution_id]
