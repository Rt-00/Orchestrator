import axios from "axios";
import type {
  ExecutionPayload,
  ExecutionStatus,
  ExecutionResult,
} from "@/types/ssh.types";

const API_URL = "http://localhost:8000";

export const sshApi = {
  async executeScript(payload: ExecutionPayload) {
    const response = await axios.post(`${API_URL}/api/ssh/execute`, payload);
    return response.data;
  },

  async getExecutionStatus(executionId: string): Promise<ExecutionStatus> {
    const response = await axios.get(
      `${API_URL}/api/ssh/status/${executionId}`
    );
    return response.data;
  },

  async getExecutionResults(executionId: string): Promise<ExecutionResult[]> {
    const response = await axios.get(
      `${API_URL}/api/ssh/results/${executionId}`
    );
    return response.data;
  },
};
