import { ref } from "vue";

import type { ConfirmOptions, ConfirmState } from "@/types/ui";

const visible = ref(false);
const options = ref<ConfirmState>({
  title: "Confirm",
  message: "",
  confirmLabel: "Confirm",
  cancelLabel: "Cancel",
  danger: false,
});

let pending: ((value: boolean) => void) | null = null;

export function useConfirm() {
  function confirm(config: ConfirmOptions): Promise<boolean> {
    options.value = {
      title: config.title ?? "Confirm",
      message: config.message ?? "",
      confirmLabel: config.confirmLabel ?? "Confirm",
      cancelLabel: config.cancelLabel ?? "Cancel",
      danger: config.danger ?? false,
    };
    visible.value = true;

    return new Promise((resolve) => {
      pending = resolve;
    });
  }

  function resolveConfirm(): void {
    visible.value = false;
    pending?.(true);
    pending = null;
  }

  function resolveCancel(): void {
    visible.value = false;
    pending?.(false);
    pending = null;
  }

  return {
    visible,
    options,
    confirm,
    resolveConfirm,
    resolveCancel,
  };
}
