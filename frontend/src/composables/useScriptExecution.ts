import { ref, computed } from "vue";
import { sshApi } from "../services/sshApi";
import type {
  Host,
  ExecutionStatus,
  ExecutionResult,
} from "../types/ssh.types";

export function useScriptExecution() {
  const currentExecutionId = ref<string | null>(null);
  const executionStatus = ref<ExecutionStatus | null>(null);
  const executionResults = ref<ExecutionResult[]>([]);
  const isExecuting = ref(false);

  const progressPercentage = computed(() => {
    if (!executionStatus.value) return 0;
    return Math.round(
      (executionStatus.value.completed_hosts /
        executionStatus.value.total_hosts) *
        100
    );
  });

  const executeScript = async (
    hosts: Host[],
    script: string,
    timeoutSeconds: number,
    maxConcurrent: number
  ) => {
    try {
      isExecuting.value = true;
      executionStatus.value = null;
      executionResults.value = [];

      const response = await sshApi.executeScript({
        hosts,
        script,
        timeout_seconds: timeoutSeconds,
        max_concurrent: maxConcurrent,
      });

      currentExecutionId.value = response.execution_id;
      pollStatus();
    } catch (error) {
      console.error("Error executing script:", error);
      alert("Error executing script. Check console for details.");
      isExecuting.value = false;
      throw error;
    }
  };

  const pollStatus = async () => {
    if (!currentExecutionId.value) return;

    const interval = setInterval(async () => {
      try {
        const status = await sshApi.getExecutionStatus(
          currentExecutionId.value!
        );
        executionStatus.value = status;

        if (status.status === "Completed") {
          clearInterval(interval);
          isExecuting.value = false;
          await fetchResults();
        }
      } catch (error) {
        clearInterval(interval);
        isExecuting.value = false;
        console.error("Error polling status:", error);
      }
    }, 1000);
  };

  const fetchResults = async () => {
    if (!currentExecutionId.value) return;

    try {
      const results = await sshApi.getExecutionResults(
        currentExecutionId.value
      );
      executionResults.value = results;
    } catch (error) {
      console.error("Error fetching results:", error);
    }
  };

  return {
    currentExecutionId,
    executionStatus,
    executionResults,
    isExecuting,
    progressPercentage,
    executeScript,
    fetchResults,
  };
}
