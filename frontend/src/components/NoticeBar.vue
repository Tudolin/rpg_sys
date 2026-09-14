<script setup lang="ts">
withDefaults(defineProps<{ kind?: "error" | "success" | "info" }>(), { kind: "info" });
</script>

<template>
  <p class="notice" :class="kind" role="status">
    <span class="mark">{{ kind === "error" ? "⚠️" : kind === "success" ? "✨" : "📜" }}</span>
    <slot />
  </p>
</template>

<style scoped>
.notice {
  display: flex;
  align-items: center;
  gap: 9px;
  margin: 0 0 14px;
  padding: 11px 15px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 0.92rem;
}

.mark {
  font-size: 1.05rem;
}

.error {
  background: rgba(239, 91, 69, 0.16);
  color: #ffd9d2;
  box-shadow: 0 0 0 2px var(--school-fire-deep);
}

.success {
  background: rgba(95, 201, 111, 0.16);
  color: #d8f6de;
  box-shadow: 0 0 0 2px var(--school-life-deep);
}

.info {
  background: rgba(79, 191, 232, 0.14);
  color: #d6f1fb;
  box-shadow: 0 0 0 2px var(--school-ice-deep);
}
</style>
