<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import type { FileItem } from "@/types";
import AnimatedValue from "./AnimatedValue.vue";

const props = defineProps<{
  file: FileItem;
}>();

const { t } = useI18n();

const display = computed(() => {
  const { processing_status: proc, scan_status: scan } = props.file;

  if (proc === "processing" || proc === "uploaded") {
    return {
      label: t(`files.${proc}` as "files.processing"),
      className: "badge--processing",
      spinning: proc === "processing",
    };
  }

  if (proc === "failed") {
    return {
      label: t("files.failed"),
      className: "badge--failed",
      spinning: false,
    };
  }

  if (scan === "clean" || scan === "suspicious") {
    return {
      label: t(`files.${scan}`),
      className: scan === "suspicious" ? "badge--suspicious" : "badge--clean",
      spinning: false,
    };
  }

  return {
    label: t("files.processed"),
    className: "badge--processed",
    spinning: false,
  };
});
</script>

<template>
  <span
    class="badge"
    :class="display.className"
  >
    <span
      v-if="display.spinning"
      class="spinner"
    />
    <AnimatedValue :value="display.label" />
  </span>
</template>
