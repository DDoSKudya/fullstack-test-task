import { QueryClient, VueQueryPlugin } from "@tanstack/vue-query";
import { createApp, h } from "vue";
import { beforeEach, describe, expect, it, vi } from "vitest";

const fetchFiles = vi.fn().mockResolvedValue([]);
const fetchAlerts = vi.fn().mockResolvedValue([]);
const uploadFileApi = vi.fn().mockResolvedValue({ id: "1" });
const deleteFileApi = vi.fn().mockResolvedValue(undefined);

vi.mock("@/api/client", () => ({
  fetchFiles: (...args: unknown[]) => fetchFiles(...args),
  fetchAlerts: (...args: unknown[]) => fetchAlerts(...args),
  uploadFile: (...args: unknown[]) => uploadFileApi(...args),
  deleteFile: (...args: unknown[]) => deleteFileApi(...args),
}));

import {
  useAlertsQuery,
  useDeleteMutation,
  useFilesQuery,
  useUploadMutation,
} from "./useDashboard";

function mountQuery<T>(composable: () => T): { result: T; queryClient: QueryClient } {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });
  let result!: T;
  const app = createApp({
    setup() {
      result = composable();
      return () => h("div");
    },
  });
  app.use(VueQueryPlugin, { queryClient });
  app.mount(document.createElement("div"));
  return { result, queryClient };
}

describe("useDashboard", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("useFilesQuery loads files", async () => {
    const { result: query } = mountQuery(() => useFilesQuery());

    await vi.waitFor(() => expect(query.isSuccess.value).toBe(true));
    expect(fetchFiles).toHaveBeenCalledOnce();
    expect(query.data.value).toEqual([]);
  });

  it("useAlertsQuery loads alerts", async () => {
    const { result: query } = mountQuery(() => useAlertsQuery());

    await vi.waitFor(() => expect(query.isSuccess.value).toBe(true));
    expect(fetchAlerts).toHaveBeenCalledOnce();
  });

  it("useUploadMutation invalidates caches on success", async () => {
    const { result: mutation, queryClient } = mountQuery(() => useUploadMutation());
    const invalidate = vi.spyOn(queryClient, "invalidateQueries");
    const file = new File(["x"], "test.txt", { type: "text/plain" });

    await mutation.mutateAsync({ title: "doc", file });

    expect(uploadFileApi).toHaveBeenCalledWith("doc", file);
    expect(invalidate).toHaveBeenCalledWith({ queryKey: ["files"] });
    expect(invalidate).toHaveBeenCalledWith({ queryKey: ["alerts"] });
  });

  it("useDeleteMutation invalidates caches on success", async () => {
    const { result: mutation, queryClient } = mountQuery(() => useDeleteMutation());
    const invalidate = vi.spyOn(queryClient, "invalidateQueries");

    await mutation.mutateAsync("file-id");

    expect(deleteFileApi).toHaveBeenCalledWith("file-id");
    expect(invalidate).toHaveBeenCalledWith({ queryKey: ["files"] });
    expect(invalidate).toHaveBeenCalledWith({ queryKey: ["alerts"] });
  });
});
