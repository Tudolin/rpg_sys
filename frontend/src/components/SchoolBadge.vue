<script setup lang="ts">
import type { SchoolTone } from "@/types";

withDefaults(defineProps<{ tone?: SchoolTone; icon?: string }>(), { tone: "gold" });
</script>

<template>
  <span class="badge" :class="`tone-${tone}`">
    <span v-if="icon" class="badge-icon">{{ icon }}</span>
    <slot />
  </span>
</template>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 12px;
  border-radius: var(--radius-pill);
  background: linear-gradient(180deg, color-mix(in srgb, var(--tone) 80%, #fff), var(--tone));
  color: #fff;
  font-size: 0.78rem;
  font-weight: 700;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    0 0 0 2px var(--tone-deep),
    0 2px 0 var(--tone-deep);
  white-space: nowrap;
}

.badge-icon {
  font-size: 0.9rem;
}
</style>
