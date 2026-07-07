<script setup lang="ts">
import { useAutoAnimate } from "@formkit/auto-animate/vue";
import { useI18n } from "vue-i18n";
import type { FileItem } from "@/types";
import { formatBytes } from "@/utils/format";
import AnimatedValue from "./AnimatedValue.vue";
import FileRowActions from "./FileRowActions.vue";
import FileStatusBadge from "./FileStatusBadge.vue";

defineProps<{
  files: FileItem[];
  deletingId?: string | null;
}>();

const emit = defineEmits<{
  delete: [fileId: string];
}>();

const { t } = useI18n();
const [tableBody] = useAutoAnimate();
</script>

<template>
  <section class="surface surface--panel">
    <header class="panel-head">
      <h2 class="panel-head__title">
        <AnimatedValue :value="t('files.title')" />
      </h2>
      <span class="panel-head__count">
        <AnimatedValue :value="files.length" />
      </span>
    </header>

    <div
      v-if="files.length === 0"
      class="empty"
    >
      <p class="empty__title">
        <AnimatedValue :value="t('files.empty')" />
      </p>
      <p class="empty__text">
        <AnimatedValue :value="t('upload.drop')" />
      </p>
    </div>

    <div
      v-else
      class="panel-scroll"
    >
      <table class="table-lite">
        <thead>
          <tr>
            <th><AnimatedValue :value="t('files.titleCol')" /></th>
            <th class="hidden md:table-cell"><AnimatedValue :value="t('files.name')" /></th>
            <th><AnimatedValue :value="t('files.size')" /></th>
            <th><AnimatedValue :value="t('files.status')" /></th>
            <th><AnimatedValue :value="t('files.actions')" /></th>
          </tr>
        </thead>
        <tbody ref="tableBody">
          <tr
            v-for="file in files"
            :key="file.id"
            :class="{ 'is-attention': file.requires_attention }"
          >
            <td>
              <div
                class="file-cell__title"
                :title="file.title"
              >
                {{ file.title }}
              </div>
              <div
                class="file-cell__sub md:hidden"
                :title="file.original_name"
              >
                {{ file.original_name }}
              </div>
            </td>
            <td
              class="hidden md:table-cell text-text-muted"
              :title="file.original_name"
            >
              {{ file.original_name }}
            </td>
            <td class="mono text-text-muted">
              {{ formatBytes(file.size) }}
            </td>
            <td>
              <FileStatusBadge :file="file" />
            </td>
            <td>
              <FileRowActions
                :file-id="file.id"
                :filename="file.original_name"
                :deleting="deletingId === file.id"
                @delete="emit('delete', file.id)"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
