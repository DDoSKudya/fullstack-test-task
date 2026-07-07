<script setup lang="ts">
import { ArrowDownTrayIcon, TrashIcon } from "@heroicons/vue/24/outline";
import { useI18n } from "vue-i18n";
import { downloadUrl } from "@/api/client";
import AppButton from "./AppButton.vue";

defineProps<{
  fileId: string;
  deleting?: boolean;
}>();

const emit = defineEmits<{
  delete: [];
}>();

const { t } = useI18n();
</script>

<template>
  <div class="flex items-center gap-1">
    <a
      :href="downloadUrl(fileId)"
      class="btn btn--ghost btn--icon"
      :aria-label="t('actions.download')"
    >
      <ArrowDownTrayIcon class="icon-md" />
    </a>
    <AppButton
      variant="ghost"
      icon
      :disabled="deleting"
      :aria-label="t('actions.delete')"
      @click="emit('delete')"
    >
      <TrashIcon class="icon-md" />
    </AppButton>
  </div>
</template>
