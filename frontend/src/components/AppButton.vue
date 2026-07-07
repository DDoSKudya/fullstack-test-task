<script setup lang="ts">
import { computed } from "vue";

type ButtonVariant = "primary" | "ghost" | "danger";

const props = withDefaults(
  defineProps<{
    type?: "button" | "submit";
    variant?: ButtonVariant;
    disabled?: boolean;
    icon?: boolean;
  }>(),
  {
    type: "button",
    variant: "primary",
    disabled: false,
    icon: false,
  },
);

const variantClass = computed(() => {
  const map: Record<ButtonVariant, string> = {
    primary: "btn--primary",
    ghost: "btn--ghost",
    danger: "btn--danger",
  };
  return map[props.variant];
});
</script>

<template>
  <button
    :type="type"
    class="btn"
    :class="[variantClass, icon && 'btn--icon']"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>
