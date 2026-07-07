<script setup lang="ts">
import { XMarkIcon } from "@heroicons/vue/24/outline";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const visible = defineModel<boolean>({ default: false });

withDefaults(
  defineProps<{
    title?: string;
  }>(),
  {
    title: "",
  },
);

defineEmits<{
  close: [];
}>();
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="visible"
        class="drawer-backdrop"
        @click.self="$emit('close')"
      >
        <aside
          class="drawer"
          role="dialog"
          aria-modal="true"
          @click.stop
        >
          <header class="drawer__head">
            <h2
              v-if="title"
              class="drawer__title"
            >
              {{ title }}
            </h2>
            <button
              type="button"
              class="btn btn--ghost drawer__close"
              :aria-label="t('common.close')"
              @click="$emit('close')"
            >
              <XMarkIcon class="drawer__close-icon" />
            </button>
          </header>
          <div class="drawer__body">
            <slot />
          </div>
          <footer
            v-if="$slots.footer"
            class="drawer__foot"
          >
            <slot name="footer" />
          </footer>
        </aside>
      </div>
    </Transition>
  </Teleport>
</template>
