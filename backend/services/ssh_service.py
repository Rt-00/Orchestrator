import asyncio
import paramiko
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time


from models import ExecutionRequest, HostConfig
from settings import settings
from storage import executions, results


class SSHExecutionService:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=settings.THREAD_POOL_SIZE)

    def execute_on_host(self, host: HostConfig, script: str, timeout: int) -> dict:
        """Execute script on a single host with retry logic"""
        start_time = datetime.now()
        output = ""
        error = ""
        success = False

        for attempt in range(settings.SSH_RETRY_COUNT):
            try:
                # Exponential backoff between retries
                if attempt > 0:
                    time.sleep(2**attempt)

                # Create and config SSH client
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                # Connection parameters
                connect_kwargs = {
                    "hostname": host.hostname,
                    "port": host.port,
                    "password": host.password,
                    "username": host.username,
                    "timeout": settings.SSH_CONNECTION_TIMEOUT,
                    "banner_timeout": settings.SSH_BANNER_TIMEOUT,
                    "auth_timeout": settings.SSH_AUTH_TIMEOUT,
                    "look_for_keys": False,
                    "allow_agent": False,
                }

                ssh.connect(**connect_kwargs)

                stdin, stdout, stderr = ssh.exec_command(script, timeout=timeout)

                # Get results
                output = stdout.read().decode("utf-8", errors="ignore")
                error = stderr.read().decode("utf-8", errors="ignore")
                exit_status = stdout.channel.recv_exit_status()

                success = exit_status == 0
                ssh.close()
                break  # Success, exit retry loop

            except paramiko.AuthenticationException:
                error = "Authentication failed"
                break  # No retry on auth failure

            except paramiko.SSHException as e:
                error = f"SSH error (attempt {attempt + 1}/{settings.SSH_RETRY_COUNT}): {str(e)}"

                if attempt == settings.SSH_RETRY_COUNT - 1:
                    success = False

                continue

            except Exception as e:
                error = f"Error (attempt {attempt + 1}/{settings.SSH_RETRY_COUNT}): {str(e)}"

                if attempt == settings.SSH_RETRY_COUNT - 1:
                    success = False
                continue

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        return {
            "hostname": host.hostname,
            "success": success,
            "output": output,
            "error": error,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
        }

    async def execute_on_multiple_hosts(
        self, execution_id: str, request: ExecutionRequest
    ):
        """Execute script on multiple hosts with concurrency control"""
        start_time = datetime.now()

        # Initialize execution status
        executions[execution_id] = {
            "execution_id": execution_id,
            "status": "Running",
            "total_hosts": len(request.hosts),
            "completed_hosts": 0,
            "successful_hosts": 0,
            "failed_hosts": 0,
            "start_time": start_time.isoformat(),
            "end_time": None,
        }

        # Semaphore for concurrency control
        semaphore = asyncio.Semaphore(request.max_concurrent)

        async def execute_with_semaphore(host: HostConfig):
            async with semaphore:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.executor,
                    self.execute_on_host,
                    host,
                    request.script,
                    request.timeout_seconds,
                )

                # Store result
                results[execution_id].append(result)

                # Update status
                executions[execution_id]["completed_hosts"] += 1

                if result["success"]:
                    executions[execution_id]["successful_hosts"] += 1
                else:
                    executions[execution_id]["failed_hosts"] += 1

                return result

        tasks = [execute_with_semaphore(host) for host in request.hosts]
        await asyncio.gather(*tasks, return_exceptions=True)

        # Mark as completed
        executions[execution_id]["status"] = "Completed"
        executions[execution_id]["end_time"] = datetime.utcnow().isoformat()


# Singleton instance
ssh_service = SSHExecutionService()
