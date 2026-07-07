<script setup lang="ts">
import { ref } from "vue";
import { ArrowDownTrayIcon, TrashIcon } from "@heroicons/vue/24/outline";
import { useI18n } from "vue-i18n";
import { toast } from "vue-sonner";
import { downloadFile } from "@/api/client";
import { useApiErrorMessage } from "@/composables/useApiErrorMessage";
import AppButton from "./AppButton.vue";

const props = defineProps<{
  fileId: string;
  filename: string;
  deleting?: boolean;
}>();

const emit = defineEmits<{
  delete: [];
}>();

const { t } = useI18n();
const { apiError } = useApiErrorMessage();
const downloading = ref(false);

async function onDownload() {
  downloading.value = true;
  try {
    await downloadFile(props.fileId, props.filename);
  } catch (error) {
    toast.error(apiError(error, t("actions.downloadError")));
  } finally {
    downloading.value = false;
  }
}
</script>

<template>
  <div class="flex items-center gap-1">
    <AppButton
      variant="ghost"
      icon
      :disabled="downloading || deleting"
      :aria-label="t('actions.download')"
      @click="onDownload"
    >
      <ArrowDownTrayIcon class="icon-md" />
    </AppButton>
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
