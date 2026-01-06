import type { CSVHost, Host } from "@/types/ssh.types";

export function parseCSV(csvText: string): CSVHost[] {
  const lines = csvText.trim().split("\n");
  const result: CSVHost[] = [];

  // Remove header if exists
  const dataLines = lines[0]!.toLowerCase().includes("hostname")
    ? lines.slice(1)
    : lines;

  for (const line of dataLines) {
    if (!line.trim()) continue;

    // Handle CSV with proper comma parsing (respecting quotes)
    const values =
      line
        .match(/(".*?"|[^,]+)(?=\s*,|\s*$)/g)
        ?.map((v) => v.replace(/^"|"$/g, "").trim()) || [];

    if (values.length >= 3) {
      result.push({
        hostname: values[0] || "",
        port: values[1] || "22",
        username: values[2] || "",
        password: values[3] || "",
        private_key_path: values[4] || undefined,
      });
    }
  }

  return result;
}

export function csvToHosts(csvHosts: CSVHost[]): Host[] {
  return csvHosts.map((h) => ({
    hostname: h.hostname,
    port: parseInt(h.port) || 22,
    username: h.username,
    password: h.password,
    private_key_path: h.private_key_path,
  }));
}

export function generateCSVTemplate(): string {
  return (
    "hostname,port,username,password,private_key_path\n" +
    "192.168.1.100,22,admin,senha123,\n" +
    "server.example.com,22,root,senha456,/path/to/key\n" +
    "10.0.0.50,2222,ubuntu,senha789,"
  );
}

export function downloadCSVTemplate(): void {
  const template = generateCSVTemplate();
  const blob = new Blob([template], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "hosts_template.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}
