<template>
  <div
    class="spinner"
    :class="{ 'spinner--lg': large }"
    role="status"
    :aria-label="ariaLabel"
  />
</template>

<script setup lang="ts">
defineProps<{
  ariaLabel?: string;
  large?: boolean;
}>();
</script>
