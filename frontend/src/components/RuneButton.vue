<script setup lang="ts">
import type { SchoolTone } from "@/types";

withDefaults(
  defineProps<{
    tone?: SchoolTone;
    size?: "sm" | "md" | "lg";
    block?: boolean;
    disabled?: boolean;
    type?: "button" | "submit";
  }>(),
  { tone: "gold", size: "md", block: false, disabled: false, type: "button" },
);
</script>

<template>
  <button
    class="rune"
    :class="[`tone-${tone}`, `size-${size}`, { block }]"
    :type="type"
    :disabled="disabled"
  >
    <span class="label"><slot /></span>
  </button>
</template>

<style scoped>
.rune {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: var(--radius-pill);
  /* Mantém o brilho diagonal (::after) contido no botão. */
  overflow: hidden;
  font-family: var(--font-ui);
  font-weight: 800;
  letter-spacing: 0.02em;
  color: #fff;
  cursor: pointer;
  text-shadow: 0 2px 2px rgba(0, 0, 0, 0.35);
  background: linear-gradient(180deg, color-mix(in srgb, var(--tone) 78%, #fff), var(--tone));
  box-shadow:
    inset 0 2px 0 rgba(255, 255, 255, 0.55),
    inset 0 -3px 0 rgba(0, 0, 0, 0.18),
    0 0 0 2px var(--tone-deep),
    0 5px 0 var(--tone-deep),
    0 9px 16px rgba(10, 6, 25, 0.45);
  transition: transform 0.1s ease, box-shadow 0.1s ease, filter 0.15s ease;
}

.rune:hover:not(:disabled) {
  filter: brightness(1.06);
  transform: translateY(-2px);
  box-shadow:
    inset 0 2px 0 rgba(255, 255, 255, 0.55),
    inset 0 -3px 0 rgba(0, 0, 0, 0.18),
    0 0 0 2px var(--tone-deep),
    0 7px 0 var(--tone-deep),
    0 12px 20px rgba(10, 6, 25, 0.5);
}

.rune:active:not(:disabled) {
  transform: translateY(3px);
  box-shadow:
    inset 0 2px 6px rgba(0, 0, 0, 0.3),
    0 0 0 2px var(--tone-deep),
    0 2px 0 var(--tone-deep),
    0 4px 8px rgba(10, 6, 25, 0.4);
}

.rune:disabled {
  cursor: not-allowed;
  filter: grayscale(0.55) brightness(0.85);
  opacity: 0.75;
}

.rune:focus-visible {
  outline: 3px solid var(--gold-200);
  outline-offset: 3px;
}

/* Brilho diagonal que atravessa o botão no hover. */
.rune::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(115deg, transparent 35%, rgba(255, 255, 255, 0.35) 50%, transparent 65%);
  transform: translateX(-120%);
  transition: transform 0.55s ease;
  pointer-events: none;
}

.rune:hover:not(:disabled)::after {
  transform: translateX(120%);
}

.label {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.size-sm {
  padding: 7px 15px;
  font-size: 0.85rem;
}

.size-md {
  padding: 11px 22px;
  font-size: 1rem;
}

.size-lg {
  padding: 15px 32px;
  font-size: 1.15rem;
}

.block {
  display: flex;
  width: 100%;
}
</style>
