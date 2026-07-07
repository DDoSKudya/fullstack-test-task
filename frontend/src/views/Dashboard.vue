<script setup lang="ts">
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";
import { toast } from "vue-sonner";
import {
  useAlertsQuery,
  useDeleteMutation,
  useFilesQuery,
  useUploadMutation,
} from "@/composables/useDashboard";
import { useConfirm } from "@/composables/useConfirm";
import AlertTimeline from "@/components/AlertTimeline.vue";
import AppButton from "@/components/AppButton.vue";
import AppDrawer from "@/components/AppDrawer.vue";
import AppHeader from "@/components/AppHeader.vue";
import AppSpinner from "@/components/AppSpinner.vue";
import FileTable from "@/components/FileTable.vue";
import FileUploadZone from "@/components/FileUploadZone.vue";
import StatsCards from "@/components/StatsCards.vue";

const { t } = useI18n();
const { confirm } = useConfirm();
const uploadOpen = ref(false);
const uploadTitle = ref("");
const uploadFile = ref<File | null>(null);
const deletingId = ref<string | null>(null);

const filesQuery = useFilesQuery();
const alertsQuery = useAlertsQuery();
const uploadMutation = useUploadMutation();
const deleteMutation = useDeleteMutation();

const files = computed(() => filesQuery.data.value ?? []);
const alerts = computed(() => alertsQuery.data.value ?? []);
const loading = computed(() => filesQuery.isPending.value || alertsQuery.isPending.value);

function openUpload() {
  uploadTitle.value = "";
  uploadFile.value = null;
  uploadOpen.value = true;
}

function closeUpload() {
  uploadOpen.value = false;
}

async function submitUpload() {
  if (!uploadFile.value || !uploadTitle.value.trim()) {
    return;
  }
  try {
    await uploadMutation.mutateAsync({
      title: uploadTitle.value.trim(),
      file: uploadFile.value,
    });
    toast.success(t("upload.success"));
    closeUpload();
  } catch {
    toast.error(t("upload.error"));
  }
}

async function onDelete(fileId: string) {
  const accepted = await confirm({
    title: t("actions.deleteTitle"),
    message: t("actions.deleteConfirm"),
    confirmLabel: t("actions.delete"),
    cancelLabel: t("upload.cancel"),
    danger: true,
  });
  if (!accepted) {
    return;
  }

  deletingId.value = fileId;
  try {
    await deleteMutation.mutateAsync(fileId);
    toast.success(t("actions.deleteSuccess"));
  } catch {
    toast.error(t("actions.deleteError"));
  } finally {
    deletingId.value = null;
  }
}
</script>

<template>
  <div class="app">
    <AppHeader @upload="openUpload" />

    <main class="app-main">
      <div
        v-if="loading"
        class="centered"
      >
        <AppSpinner
          large
          :aria-label="t('common.loading')"
        />
      </div>

      <template v-else>
        <div class="dashboard-content">
          <StatsCards
            :files="files"
            :alerts="alerts"
          />

          <div class="split-layout">
            <FileTable
              :files="files"
              :deleting-id="deletingId"
              @delete="onDelete"
            />
            <AlertTimeline :alerts="alerts" />
          </div>
        </div>
      </template>
    </main>

    <AppDrawer
      v-model="uploadOpen"
      :title="t('upload.title')"
      @close="closeUpload"
    >
      <FileUploadZone
        v-model:title="uploadTitle"
        v-model:file="uploadFile"
      />
      <template #footer>
        <AppButton
          type="submit"
          :disabled="!uploadFile || !uploadTitle.trim() || uploadMutation.isPending.value"
          @click="submitUpload"
        >
          {{ t("upload.submit") }}
        </AppButton>
      </template>
    </AppDrawer>
  </div>
</template>
