<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import type { AlertItem, FileItem } from "@/types";
import AnimatedValue from "./AnimatedValue.vue";

const props = defineProps<{
  files: FileItem[];
  alerts: AlertItem[];
}>();

const { t } = useI18n();

const attentionCount = computed(
  () => props.files.filter((file) => file.requires_attention).length,
);

const metrics = computed(() => [
  {
    key: "files",
    label: t("stats.files"),
    value: props.files.length,
    tone: "files" as const,
  },
  {
    key: "attention",
    label: t("stats.attention"),
    value: attentionCount.value,
    tone: "attention" as const,
  },
  {
    key: "alerts",
    label: t("stats.alerts"),
    value: props.alerts.length,
    tone: "alerts" as const,
  },
]);
</script>

<template>
  <div class="stat-strip surface">
    <div
      v-for="metric in metrics"
      :key="metric.key"
      class="stat-strip__item"
      :class="`stat-strip__item--${metric.tone}`"
    >
      <p
        class="stat-strip__value"
        :class="{ 'stat-strip__value--warning': metric.tone === 'attention' && metric.value > 0 }"
      >
        <AnimatedValue :value="metric.value" />
      </p>
      <p class="stat-strip__label">
        <AnimatedValue :value="metric.label" />
      </p>
    </div>
  </div>
</template>
