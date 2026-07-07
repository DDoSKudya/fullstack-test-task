import { inject, ref, type InjectionKey, type Ref } from "vue";

import type { ConfirmOptions, ConfirmState } from "@/types/ui";

export type ConfirmApi = {
  visible: Ref<boolean>;
  options: Ref<ConfirmState>;
  confirm: (config: ConfirmOptions) => Promise<boolean>;
  resolveConfirm: () => void;
  resolveCancel: () => void;
};

export const confirmKey: InjectionKey<ConfirmApi> = Symbol("confirm");

const defaultOptions: ConfirmState = {
  title: "Confirm",
  message: "",
  confirmLabel: "Confirm",
  cancelLabel: "Cancel",
  danger: false,
};

export function createConfirm(): ConfirmApi {
  const visible = ref(false);
  const options = ref<ConfirmState>({ ...defaultOptions });
  let pending: ((value: boolean) => void) | null = null;

  function confirm(config: ConfirmOptions): Promise<boolean> {
    options.value = {
      title: config.title ?? defaultOptions.title,
      message: config.message ?? defaultOptions.message,
      confirmLabel: config.confirmLabel ?? defaultOptions.confirmLabel,
      cancelLabel: config.cancelLabel ?? defaultOptions.cancelLabel,
      danger: config.danger ?? defaultOptions.danger,
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

export function useConfirm(): ConfirmApi {
  const api = inject(confirmKey);
  if (!api) {
    throw new Error("useConfirm() requires confirmKey to be provided");
  }
  return api;
}
