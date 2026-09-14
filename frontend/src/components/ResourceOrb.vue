<script setup lang="ts">
import { computed } from "vue";
import type { SchoolTone } from "@/types";

const props = withDefaults(
  defineProps<{
    label: string;
    current: number;
    max: number;
    tone?: SchoolTone;
    size?: "sm" | "md" | "lg";
  }>(),
  { tone: "gold", size: "md" },
);

const pct = computed(() => {
  if (!props.max || props.max <= 0) return 0;
  return Math.max(0, Math.min(100, (props.current / props.max) * 100));
});

const low = computed(() => pct.value <= 25);
</script>

<template>
  <div class="orb-wrap" :class="[`tone-${tone}`, `size-${size}`]" :title="`${label}: ${current} / ${max}`">
    <div class="orb" :class="{ low }">
      <div class="liquid" :style="{ height: `${pct}%` }">
        <span class="wave" />
      </div>
      <span class="shine" />
      <span class="value">{{ current }}<i>/{{ max }}</i></span>
    </div>
    <span class="orb-label">{{ label }}</span>
  </div>
</template>

<style scoped>
.orb-wrap {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.orb {
  position: relative;
  width: var(--orb-size);
  height: var(--orb-size);
  border-radius: 50%;
  overflow: hidden;
  background: radial-gradient(circle at 50% 120%, #1a1136, #0b0720 70%);
  box-shadow:
    0 0 0 3px var(--gold-600),
    0 0 0 6px var(--gold-300),
    0 0 0 8px var(--gold-700),
    0 0 18px color-mix(in srgb, var(--tone) 60%, transparent),
    inset 0 -6px 14px rgba(0, 0, 0, 0.55);
}

.liquid {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, color-mix(in srgb, var(--tone) 85%, #fff) 0%, var(--tone) 40%, var(--tone-deep) 100%);
  transition: height 0.45s cubic-bezier(0.33, 1, 0.68, 1);
}

/* Crista ondulada no topo do líquido — sutil, só para dar vida. */
.wave {
  position: absolute;
  top: -5px;
  left: -25%;
  width: 150%;
  height: 10px;
  background: var(--tone);
  border-radius: 45%;
  animation: bob 3.2s ease-in-out infinite;
  opacity: 0.85;
}

/* Sem líquido não há crista para desenhar. */
.liquid[style*="height: 0%"] .wave {
  display: none;
}

.shine {
  position: absolute;
  top: 8%;
  left: 14%;
  width: 40%;
  height: 28%;
  border-radius: 50%;
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0));
  pointer-events: none;
}

.value {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: var(--orb-font);
  color: #fff;
  text-shadow: 0 2px 3px rgba(0, 0, 0, 0.75);
}

.value i {
  font-style: normal;
  opacity: 0.8;
  font-size: 0.8em;
  margin-left: 2px;
}

.orb.low {
  animation: pulse-warning 1.4s ease-in-out infinite;
}

.orb-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--ink-onDark-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.size-sm {
  --orb-size: 46px;
  --orb-font: 0.62rem;
}

.size-md {
  --orb-size: 78px;
  --orb-font: 0.85rem;
}

.size-lg {
  --orb-size: 104px;
  --orb-font: 1rem;
}

@keyframes bob {
  0%,
  100% {
    transform: translateX(-4%) rotate(-1deg);
  }
  50% {
    transform: translateX(4%) rotate(1deg);
  }
}

@keyframes pulse-warning {
  0%,
  100% {
    box-shadow:
      0 0 0 3px var(--gold-600),
      0 0 0 6px var(--gold-300),
      0 0 0 8px var(--gold-700),
      0 0 14px color-mix(in srgb, var(--school-fire) 55%, transparent),
      inset 0 -6px 14px rgba(0, 0, 0, 0.55);
  }
  50% {
    box-shadow:
      0 0 0 3px var(--gold-600),
      0 0 0 6px var(--gold-300),
      0 0 0 8px var(--gold-700),
      0 0 26px color-mix(in srgb, var(--school-fire) 90%, transparent),
      inset 0 -6px 14px rgba(0, 0, 0, 0.55);
  }
}
</style>
