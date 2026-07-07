<script setup lang="ts">
import { Toaster } from "vue-sonner";
import ConfirmDialog from "@/components/ConfirmDialog.vue";
import Dashboard from "@/views/Dashboard.vue";
</script>

<template>
  <Dashboard />
  <ConfirmDialog />
  <Toaster
    rich-colors
    position="top-right"
  />
</template>
