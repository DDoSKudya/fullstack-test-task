import type { AlertItem, FileItem } from "@/types";

const API_BASE = import.meta.env.VITE_API_URL || "/api/v1";

export class ApiError extends Error {
  constructor(
    readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function parseError(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: unknown };
    if (typeof body.detail === "string") {
      return body.detail;
    }
  } catch {
    return response.statusText;
  }
  return response.statusText;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, init);
  if (!response.ok) {
    throw new ApiError(response.status, await parseError(response));
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return response.json() as Promise<T>;
}

export function fetchFiles(): Promise<FileItem[]> {
  return request("/files");
}

export function fetchAlerts(): Promise<AlertItem[]> {
  return request("/alerts");
}

export function uploadFile(title: string, file: File): Promise<FileItem> {
  const form = new FormData();
  form.append("title", title);
  form.append("file", file);
  return request("/files", { method: "POST", body: form });
}

export function deleteFile(fileId: string): Promise<void> {
  return request(`/files/${fileId}`, { method: "DELETE" });
}

export async function downloadFile(fileId: string, filename: string): Promise<void> {
  const response = await fetch(`${API_BASE}/files/${fileId}/download`);
  if (!response.ok) {
    throw new ApiError(response.status, await parseError(response));
  }

  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
