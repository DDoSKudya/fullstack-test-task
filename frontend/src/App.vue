<script setup lang="ts">
import { provide } from "vue";
import { Toaster } from "vue-sonner";
import ConfirmDialog from "@/components/ConfirmDialog.vue";
import Dashboard from "@/views/Dashboard.vue";
import { confirmKey, createConfirm } from "@/composables/useConfirm";

provide(confirmKey, createConfirm());
</script>

<template>
  <Dashboard />
  <ConfirmDialog />
  <Toaster
    rich-colors
    position="top-right"
  />
</template>
