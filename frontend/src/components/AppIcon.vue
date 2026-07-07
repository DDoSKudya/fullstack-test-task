<script setup lang="ts">
withDefaults(
  defineProps<{
    iconClass?: string;
  }>(),
  {
    iconClass: "h-8 w-8",
  },
);
</script>

<template>
  <img
    src="/icons/app-icon.svg"
    alt=""
    aria-hidden="true"
    :class="iconClass"
    width="32"
    height="32"
  >
</template>
