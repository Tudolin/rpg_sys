<script setup lang="ts">
import { computed } from "vue";
import type { SchoolTone } from "@/types";

const props = withDefaults(
  defineProps<{
    src?: string | null;
    alt?: string;
    size?: "sm" | "md" | "lg";
    tone?: SchoolTone;
  }>(),
  { size: "md", tone: "gold", alt: "" },
);

const source = computed(() => props.src || "/static/images/default.png");
</script>

<template>
  <div class="portrait" :class="[`size-${size}`, `tone-${tone}`]">
    <img :src="source" :alt="alt" loading="lazy" />
  </div>
</template>

<style scoped>
.portrait {
  position: relative;
  width: var(--portrait-size);
  height: var(--portrait-size);
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--void-700);
  box-shadow:
    0 0 0 3px var(--gold-600),
    0 0 0 6px var(--gold-300),
    0 0 0 9px var(--gold-700),
    0 0 18px color-mix(in srgb, var(--tone) 45%, transparent),
    var(--lift-1);
}

.portrait img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Reflexo de vidro sobre o retrato. */
.portrait::after {
  content: "";
  position: absolute;
  top: 6%;
  left: 12%;
  width: 45%;
  height: 26%;
  border-radius: 50%;
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.45), transparent);
  pointer-events: none;
}

.size-sm {
  --portrait-size: 52px;
}

.size-md {
  --portrait-size: 96px;
}

.size-lg {
  --portrait-size: 148px;
}
</style>
