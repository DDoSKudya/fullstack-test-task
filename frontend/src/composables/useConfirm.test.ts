import { describe, expect, it } from "vitest";
import { createConfirm, useConfirm, confirmKey } from "./useConfirm";
import { createApp, h } from "vue";

describe("createConfirm", () => {
  it("resolves true on confirm", async () => {
    const api = createConfirm();
    const promise = api.confirm({ title: "Delete?", message: "Sure?", danger: true });

    expect(api.visible.value).toBe(true);
    expect(api.options.value.title).toBe("Delete?");
    expect(api.options.value.danger).toBe(true);

    api.resolveConfirm();
    await expect(promise).resolves.toBe(true);
    expect(api.visible.value).toBe(false);
  });

  it("resolves false on cancel", async () => {
    const api = createConfirm();
    const promise = api.confirm({ message: "Cancel me" });

    api.resolveCancel();
    await expect(promise).resolves.toBe(false);
  });

  it("uses defaults for optional fields", async () => {
    const api = createConfirm();
    const promise = api.confirm({});

    expect(api.options.value.title).toBe("Confirm");
    expect(api.options.value.confirmLabel).toBe("Confirm");

    api.resolveConfirm();
    await expect(promise).resolves.toBe(true);
  });
});

describe("useConfirm", () => {
  it("returns injected confirm api", () => {
    const confirm = createConfirm();
    let injected: ReturnType<typeof useConfirm> | undefined;

    const app = createApp({
      setup() {
        injected = useConfirm();
        return () => h("div");
      },
    });
    app.provide(confirmKey, confirm);
    app.mount(document.createElement("div"));

    expect(injected).toBe(confirm);
    app.unmount();
  });

  it("throws when confirmKey is missing", () => {
    const app = createApp({
      setup() {
        expect(() => useConfirm()).toThrow("useConfirm() requires confirmKey to be provided");
        return () => h("div");
      },
    });
    app.mount(document.createElement("div"));
    app.unmount();
  });
});
