<script setup lang="ts">
import { useAutoAnimate } from "@formkit/auto-animate/vue";
import { useI18n } from "vue-i18n";
import { useAlertText } from "@/composables/useAlertText";
import type { AlertItem } from "@/types";
import AnimatedValue from "./AnimatedValue.vue";

defineProps<{
  alerts: AlertItem[];
}>();

const { t } = useI18n();
const { levelLabel, alertMessage, formatAlertDate } = useAlertText();
const [alertList] = useAutoAnimate();

function levelBadgeClass(level: string): string {
  if (level === "critical") {
    return "badge--level-critical";
  }
  if (level === "warning") {
    return "badge--level-warning";
  }
  return "badge--level-info";
}

function dotClass(level: string): string {
  if (level === "critical") {
    return "alert-item__dot--critical";
  }
  if (level === "warning") {
    return "alert-item__dot--warning";
  }
  return "alert-item__dot--info";
}
</script>

<template>
  <section class="surface surface--panel">
    <header class="panel-head">
      <h2 class="panel-head__title">
        <AnimatedValue :value="t('alerts.title')" />
      </h2>
      <span
        v-if="alerts.length > 0"
        class="panel-head__count"
      >
        <AnimatedValue :value="alerts.length" />
      </span>
    </header>

    <div
      v-if="alerts.length === 0"
      class="empty"
    >
      <p class="empty__title">
        <AnimatedValue :value="t('alerts.empty')" />
      </p>
    </div>

    <div
      v-else
      ref="alertList"
      class="panel-scroll"
    >
      <article
        v-for="alert in alerts"
        :key="alert.id"
        class="alert-item"
      >
        <span
          class="alert-item__dot"
          :class="dotClass(alert.level)"
        />
        <div class="min-w-0 flex-1">
          <div class="alert-item__meta">
            <span
              class="badge"
              :class="levelBadgeClass(alert.level)"
            >
              <AnimatedValue :value="levelLabel(alert.level)" />
            </span>
            <time class="alert-item__time">
              <AnimatedValue :value="formatAlertDate(alert.created_at)" />
            </time>
          </div>
          <p
            class="alert-item__message"
            :title="alertMessage(alert.message)"
          >
            <AnimatedValue :value="alertMessage(alert.message)" />
          </p>
          <p
            class="alert-item__file"
            :title="alert.file_id"
          >
            {{ alert.file_id }}
          </p>
        </div>
      </article>
    </div>
  </section>
</template>
