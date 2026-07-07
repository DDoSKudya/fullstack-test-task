<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{
  value: number | string;
}>();

const flashing = ref(false);

watch(
  () => props.value,
  (next, prev) => {
    if (prev === undefined || next === prev) {
      return;
    }
    flashing.value = true;
    window.setTimeout(() => {
      flashing.value = false;
    }, 520);
  },
);
</script>

<template>
  <span
    class="animated-value"
    :class="{ 'animated-value--flash': flashing }"
  >
    {{ value }}
  </span>
</template>
