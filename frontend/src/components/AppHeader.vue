<script setup lang="ts">
import { PlusIcon } from "@heroicons/vue/24/outline";
import { useI18n } from "vue-i18n";
import { setLocale, type AppLocale } from "@/i18n";
import AppButton from "./AppButton.vue";
import AppIcon from "./AppIcon.vue";
import AnimatedValue from "./AnimatedValue.vue";

const emit = defineEmits<{
  upload: [];
}>();

const { t, locale } = useI18n();

function switchLocale(next: AppLocale) {
  setLocale(next);
}
</script>

<template>
  <header class="app-header">
    <div class="app-brand">
      <AppIcon icon-class="h-8 w-8 shrink-0" />
      <div class="app-brand__text">
        <div
          class="app-brand__name"
          :title="t('app.title')"
        >
          <AnimatedValue :value="t('app.title')" />
        </div>
        <div
          class="app-brand__tagline hidden sm:block"
          :title="t('app.subtitle')"
        >
          <AnimatedValue :value="t('app.subtitle')" />
        </div>
      </div>
    </div>

    <div class="app-header__actions">
      <div class="locale-switch">
        <button
          type="button"
          class="locale-switch__btn"
          :class="{ 'locale-switch__btn--active': locale === 'ru' }"
          @click="switchLocale('ru')"
        >
          RU
        </button>
        <button
          type="button"
          class="locale-switch__btn"
          :class="{ 'locale-switch__btn--active': locale === 'en' }"
          @click="switchLocale('en')"
        >
          EN
        </button>
      </div>

      <AppButton @click="emit('upload')">
        <PlusIcon class="icon-md" />
        <span class="hidden sm:inline">
          <AnimatedValue :value="t('files.add')" />
        </span>
      </AppButton>
    </div>
  </header>
</template>
