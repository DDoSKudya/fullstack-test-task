<script setup lang="ts">
import { computed, ref } from "vue";
import { CloudArrowUpIcon, DocumentIcon, XMarkIcon } from "@heroicons/vue/24/outline";
import { useI18n } from "vue-i18n";
import { formatBytes } from "@/utils/format";
import AppButton from "./AppButton.vue";

const title = defineModel<string>("title", { default: "" });
const file = defineModel<File | null>("file", { default: null });

const { t } = useI18n();
const dragOver = ref(false);
const inputRef = ref<HTMLInputElement | null>(null);

const fileSize = computed(() => (file.value ? formatBytes(file.value.size) : null));

function onFilesSelected(event: Event) {
  const target = event.target as HTMLInputElement;
  file.value = target.files?.[0] ?? null;
}

function onDrop(event: DragEvent) {
  dragOver.value = false;
  const dropped = event.dataTransfer?.files?.[0];
  if (dropped) {
    file.value = dropped;
  }
}

function clearFile() {
  file.value = null;
  if (inputRef.value) {
    inputRef.value.value = "";
  }
}
</script>

<template>
  <div class="stack">
    <label class="field-wrap">
      <span class="field-label">{{ t("upload.fileTitle") }}</span>
      <input
        v-model="title"
        type="text"
        class="field"
        :placeholder="t('upload.fileTitlePlaceholder')"
      />
    </label>

    <div
      v-if="file"
      class="upload-file"
    >
      <div class="file-cell__icon">
        <DocumentIcon class="icon-sm" />
      </div>
      <div class="upload-file__meta">
        <div
          class="upload-file__name"
          :title="file.name"
        >
          {{ file.name }}
        </div>
        <div class="upload-file__size">{{ fileSize }}</div>
      </div>
      <AppButton
        variant="ghost"
        icon
        @click="clearFile"
      >
        <XMarkIcon class="icon-sm" />
      </AppButton>
    </div>

    <div
      v-else
      class="upload-drop"
      :class="{ 'upload-drop--active': dragOver }"
      @dragover.prevent="dragOver = true"
      @dragleave.prevent="dragOver = false"
      @drop.prevent="onDrop"
      @click="inputRef?.click()"
    >
      <div class="upload-drop__icon">
        <CloudArrowUpIcon class="icon-md" />
      </div>
      <p class="upload-drop__text">{{ t("upload.drop") }}</p>
      <p class="upload-drop__hint">{{ t("upload.hint") }}</p>
      <input
        ref="inputRef"
        type="file"
        class="hidden"
        @change="onFilesSelected"
      />
    </div>
  </div>
</template>
