import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiError, deleteFile, downloadFile, fetchAlerts, fetchFiles, uploadFile } from "@/api/client";

describe("request helpers", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("fetchFiles returns parsed json", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify([{ id: "1", title: "doc" }]), { status: 200 }),
      ),
    );

    await expect(fetchFiles()).resolves.toEqual([{ id: "1", title: "doc" }]);
  });

  it("fetchAlerts returns parsed json", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify([{ id: 1, level: "info" }]), { status: 200 }),
      ),
    );

    await expect(fetchAlerts()).resolves.toEqual([{ id: 1, level: "info" }]);
  });

  it("uploadFile sends multipart payload", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ id: "1", title: "doc" }), { status: 201 }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const file = new File(["data"], "doc.txt", { type: "text/plain" });
    await expect(uploadFile("doc", file)).resolves.toEqual({ id: "1", title: "doc" });

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(init.method).toBe("POST");
    expect(init.body).toBeInstanceOf(FormData);
  });

  it("deleteFile resolves on 204", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(null, { status: 204 })));

    await expect(deleteFile("file-id")).resolves.toBeUndefined();
  });

  it("uses status text when error body is not json", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("not json", { status: 500, statusText: "Server Error" })),
    );

    await expect(fetchFiles()).rejects.toEqual(new ApiError(500, "Server Error"));
  });

  it("uses status text when detail is not a string", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: { code: "bad" } }), {
          status: 400,
          statusText: "Bad Request",
        }),
      ),
    );

    await expect(fetchFiles()).rejects.toEqual(new ApiError(400, "Bad Request"));
  });
});

describe("downloadFile", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("throws ApiError when download fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: "Stored file not found" }), { status: 404 }),
      ),
    );

    await expect(downloadFile("missing-id", "file.txt")).rejects.toEqual(
      new ApiError(404, "Stored file not found"),
    );
  });

  it("triggers browser download on success", async () => {
    const click = vi.fn();
    const link = { href: "", download: "", click } as unknown as HTMLAnchorElement;
    const createElement = vi.spyOn(document, "createElement").mockReturnValue(link);
    vi.spyOn(URL, "createObjectURL").mockReturnValue("blob:test");
    vi.spyOn(URL, "revokeObjectURL").mockImplementation(() => undefined);
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response(new Blob(["hello"]), { status: 200 })),
    );

    await downloadFile("file-id", "readme.txt");

    expect(createElement).toHaveBeenCalledWith("a");
    expect(link.download).toBe("readme.txt");
    expect(click).toHaveBeenCalledOnce();
    expect(URL.revokeObjectURL).toHaveBeenCalledWith("blob:test");
  });
});
