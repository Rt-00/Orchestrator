export interface Host {
  hostname: string;
  port: number;
  username: string;
  password: string;
  private_key_path?: string;
}

export interface CSVHost {
  hostname: string;
  port: string;
  username: string;
  password: string;
  private_key_path?: string;
}

export interface ExecutionResult {
  hostname: string;
  success: boolean;
  output: string;
  error: string;
  start_time: string;
  end_time: string;
  duration_seconds: number;
}

export interface ExecutionStatus {
  execution_id: string;
  status: string;
  total_hosts: number;
  completed_hosts: number;
  successful_hosts: number;
  failed_hosts: number;
  start_time: string;
  end_time?: string;
}

export interface ExecutionPayload {
  hosts: Host[];
  script: string;
  timeout_seconds: number;
  max_concurrent: number;
}

export type TabType = "setup" | "status" | "results";

export interface UploadMessage {
  type: "success" | "error";
  text: string;
}
