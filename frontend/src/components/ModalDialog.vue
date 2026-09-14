<script setup lang="ts">
import { onBeforeUnmount, onMounted } from "vue";

const props = defineProps<{ title?: string; wide?: boolean }>();
const emit = defineEmits<{ close: [] }>();

function onKey(event: KeyboardEvent) {
  if (event.key === "Escape") emit("close");
}

onMounted(() => document.addEventListener("keydown", onKey));
onBeforeUnmount(() => document.removeEventListener("keydown", onKey));
</script>

<template>
  <Teleport to="body">
    <div class="veil" role="dialog" aria-modal="true" @click.self="emit('close')">
      <div class="sheet frame-gold" :class="{ wide: props.wide }">
        <header class="sheet-head">
          <h2>{{ title }}</h2>
          <button class="close" type="button" aria-label="Fechar" @click="emit('close')">✕</button>
        </header>
        <div class="sheet-body">
          <slot />
        </div>
        <footer v-if="$slots.footer" class="sheet-foot">
          <slot name="footer" />
        </footer>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.veil {
  position: fixed;
  inset: 0;
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 18px;
  background: rgba(12, 7, 30, 0.72);
  backdrop-filter: blur(4px);
  animation: fade 0.18s ease;
}

.sheet {
  width: 100%;
  max-width: 460px;
  max-height: 86vh;
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-lg);
  background: linear-gradient(170deg, var(--scroll-50), var(--scroll-200));
  color: var(--ink-900);
  animation: pop 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.sheet.wide {
  max-width: 760px;
}

.sheet-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 3px solid var(--gold-400);
}

.sheet-head h2 {
  margin: 0;
  color: var(--gold-700);
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.6);
}

.close {
  border: none;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: linear-gradient(180deg, color-mix(in srgb, var(--school-fire) 80%, #fff), var(--school-fire));
  color: #fff;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 0 0 2px var(--school-fire-deep), 0 2px 0 var(--school-fire-deep);
}

.sheet-body {
  padding: 18px 20px;
  overflow-y: auto;
}

.sheet-foot {
  padding: 14px 20px;
  border-top: 2px solid var(--scroll-300);
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

@keyframes fade {
  from {
    opacity: 0;
  }
}

@keyframes pop {
  from {
    transform: scale(0.92) translateY(10px);
    opacity: 0;
  }
}
</style>
