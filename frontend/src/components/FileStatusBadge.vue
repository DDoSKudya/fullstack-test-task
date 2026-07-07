<script setup lang="ts">
import { useI18n } from "vue-i18n";
import type { FileItem } from "@/types";
import AnimatedValue from "./AnimatedValue.vue";

defineProps<{
  file: FileItem;
}>();

const { t } = useI18n();

function processingLabel(status: string): string {
  const key = `files.${status}` as "files.processing";
  return t(key, status);
}

function scanLabel(status: string | null): string | null {
  if (!status) {
    return null;
  }
  if (status === "clean" || status === "suspicious") {
    return t(`files.${status}`);
  }
  return status;
}

function processingClass(status: string): string {
  if (status === "processed") {
    return "badge--processed";
  }
  if (status === "failed") {
    return "badge--failed";
  }
  return "badge--processing";
}

function scanClass(status: string): string {
  if (status === "suspicious") {
    return "badge--suspicious";
  }
  return "badge--clean";
}
</script>

<template>
  <div class="flex flex-wrap gap-1.5">
    <span
      class="badge"
      :class="processingClass(file.processing_status)"
    >
      <span
        v-if="file.processing_status === 'processing'"
        class="spinner"
      />
      <AnimatedValue :value="processingLabel(file.processing_status)" />
    </span>
    <span
      v-if="scanLabel(file.scan_status)"
      class="badge"
      :class="scanClass(file.scan_status!)"
    >
      <AnimatedValue :value="scanLabel(file.scan_status)!" />
    </span>
  </div>
</template>
