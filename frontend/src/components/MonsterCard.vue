<script setup lang="ts">
import { computed } from "vue";
import type { Monster } from "@/types";

const props = defineProps<{ monster: Monster }>();

const pct = computed(() => {
  const max = props.monster.hp || 1;
  return Math.max(0, Math.min(100, (props.monster.current_hp / max) * 100));
});

const defeated = computed(() => props.monster.current_hp <= 0);
</script>

<template>
  <article class="monster frame-gold-thin tone-fire" :class="{ defeated }">
    <div class="art">
      <img
        :src="`/static/images/monsters/${monster.img_url}`"
        :alt="monster.name"
        loading="lazy"
        @error="($event.target as HTMLImageElement).src = '/static/images/monsters/default.png'"
      />
    </div>
    <h3>{{ monster.name }}</h3>

    <div class="bar">
      <div class="fill" :style="{ width: `${pct}%` }" />
      <span class="bar-text">{{ monster.current_hp }} / {{ monster.hp }}</span>
    </div>

    <p v-if="monster.resumo" class="lore">{{ monster.resumo }}</p>

    <div v-if="$slots.actions" class="actions">
      <slot name="actions" />
    </div>
  </article>
</template>

<style scoped>
.monster {
  width: 190px;
  padding: 14px;
  border-radius: var(--radius-md);
  background: linear-gradient(170deg, #2a1533 0%, #1a0e26 100%);
  color: var(--ink-onDark);
  text-align: center;
  transition: transform 0.18s ease, filter 0.25s ease;
}

.monster:hover {
  transform: translateY(-4px);
}

.monster.defeated {
  filter: grayscale(0.85) brightness(0.6);
}

.art {
  width: 84px;
  height: 84px;
  margin: 0 auto 8px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--void-900);
  box-shadow:
    0 0 0 3px var(--school-fire-deep),
    0 0 0 5px var(--gold-400),
    0 0 16px rgba(239, 91, 69, 0.5);
}

.art img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

h3 {
  margin: 0 0 8px;
  font-size: 1rem;
  color: var(--gold-200);
}

.bar {
  position: relative;
  height: 20px;
  border-radius: var(--radius-pill);
  background: rgba(0, 0, 0, 0.55);
  overflow: hidden;
  box-shadow: 0 0 0 2px var(--gold-600), inset 0 2px 5px rgba(0, 0, 0, 0.6);
}

.fill {
  height: 100%;
  background: linear-gradient(180deg, #ff8a72, var(--school-fire) 55%, var(--school-fire-deep));
  transition: width 0.4s cubic-bezier(0.33, 1, 0.68, 1);
}

.bar-text {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.72rem;
  font-weight: 800;
  color: #fff;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
}

.lore {
  margin: 8px 0 0;
  font-size: 0.74rem;
  line-height: 1.35;
  color: var(--ink-onDark-muted);
}

.actions {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
