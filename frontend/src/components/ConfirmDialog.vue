<script setup lang="ts">
import { useConfirm } from "@/composables/useConfirm";

const { visible, options, resolveConfirm, resolveCancel } = useConfirm();
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="visible"
        class="modal-backdrop"
        @click.self="resolveCancel"
      >
        <section
          class="modal"
          role="alertdialog"
          aria-modal="true"
          @click.stop
        >
          <header class="modal__head">
            <h2 class="modal__title">
              {{ options.title }}
            </h2>
          </header>
          <div class="modal__body">
            {{ options.message }}
          </div>
          <footer class="modal__foot">
            <button
              type="button"
              class="btn btn--ghost"
              @click="resolveCancel"
            >
              {{ options.cancelLabel }}
            </button>
            <button
              type="button"
              class="btn"
              :class="options.danger ? 'btn--danger' : 'btn--primary'"
              @click="resolveConfirm"
            >
              {{ options.confirmLabel }}
            </button>
          </footer>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>
