<script setup lang="ts">
import type { SchoolTone } from "@/types";

withDefaults(
  defineProps<{
    title?: string;
    icon?: string;
    tone?: SchoolTone;
    thin?: boolean;
    /** Superfície escura (arcana) em vez de pergaminho. */
    dark?: boolean;
  }>(),
  { tone: "gold", thin: false, dark: false },
);
</script>

<template>
  <section class="panel" :class="[`tone-${tone}`, thin ? 'frame-gold-thin' : 'frame-gold', { dark }]">
    <header v-if="title" class="panel-head">
      <span v-if="icon" class="panel-icon">{{ icon }}</span>
      <h2>{{ title }}</h2>
    </header>
    <div class="panel-body">
      <slot />
    </div>
  </section>
</template>

<style scoped>
.panel {
  position: relative;
  border-radius: var(--radius-lg);
  background:
    radial-gradient(circle at 12% 8%, rgba(255, 255, 255, 0.7), transparent 45%),
    linear-gradient(170deg, var(--scroll-50) 0%, var(--scroll-100) 55%, var(--scroll-200) 100%);
  color: var(--ink-900);
  padding: 20px;
  margin-bottom: 24px;
}

.panel.dark {
  background:
    radial-gradient(circle at 15% 0%, rgba(145, 105, 230, 0.25), transparent 55%),
    linear-gradient(170deg, var(--void-700) 0%, var(--void-800) 100%);
  color: var(--ink-onDark);
}

/* Brilho superior sutil, reforçando o aspecto "esmaltado". */
.panel::before {
  content: "";
  position: absolute;
  inset: 3px 3px auto 3px;
  height: 38%;
  border-radius: calc(var(--radius-lg) - 4px) calc(var(--radius-lg) - 4px) 40% 40%;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.5), transparent);
  pointer-events: none;
}

.panel.dark::before {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.08), transparent);
}

.panel-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 3px solid var(--tone);
  position: relative;
}

.panel-head h2 {
  margin: 0;
  color: var(--tone-deep, var(--gold-700));
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.6);
}

.panel.dark .panel-head h2 {
  color: var(--tone);
  text-shadow: 0 2px 0 rgba(0, 0, 0, 0.4);
}

.panel-icon {
  font-size: 1.6rem;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.3));
}

.panel-body {
  position: relative;
}
</style>
