<script setup lang="ts">
/** Céu arcano: nebulosa, estrelas e faíscas flutuantes. Puramente decorativo. */
const motes = Array.from({ length: 14 }, (_, i) => ({
  id: i,
  left: `${(i * 7.3 + 4) % 96}%`,
  delay: `${(i * 1.7) % 12}s`,
  duration: `${14 + (i % 5) * 4}s`,
  size: `${4 + (i % 3) * 3}px`,
  tone: ["var(--school-ice)", "var(--gold-300)", "var(--school-storm)", "var(--school-life)"][i % 4],
}));
</script>

<template>
  <div class="backdrop" aria-hidden="true">
    <div class="nebula" />
    <div class="stars stars-far" />
    <div class="stars stars-near" />
    <span
      v-for="mote in motes"
      :key="mote.id"
      class="mote"
      :style="{
        left: mote.left,
        animationDelay: mote.delay,
        animationDuration: mote.duration,
        width: mote.size,
        height: mote.size,
        background: mote.tone,
        boxShadow: `0 0 12px ${mote.tone}`,
      }"
    />
  </div>
</template>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
  background:
    radial-gradient(120% 80% at 50% -10%, var(--void-600) 0%, transparent 55%),
    radial-gradient(90% 60% at 12% 8%, rgba(91, 63, 168, 0.55) 0%, transparent 60%),
    radial-gradient(80% 60% at 88% 20%, rgba(42, 91, 168, 0.45) 0%, transparent 62%),
    linear-gradient(180deg, var(--void-800) 0%, var(--void-900) 70%);
}

.nebula {
  position: absolute;
  inset: -20%;
  background:
    radial-gradient(closest-side, rgba(145, 105, 230, 0.32), transparent 70%) 22% 30% / 46% 46% no-repeat,
    radial-gradient(closest-side, rgba(79, 191, 232, 0.24), transparent 70%) 78% 62% / 42% 42% no-repeat,
    radial-gradient(closest-side, rgba(240, 181, 55, 0.16), transparent 70%) 52% 12% / 38% 38% no-repeat;
  filter: blur(6px);
  animation: drift 48s ease-in-out infinite alternate;
}

/* Campos de estrelas desenhados com gradientes repetidos — sem imagens. */
.stars {
  position: absolute;
  inset: 0;
  background-repeat: repeat;
}

.stars-far {
  background-image:
    radial-gradient(1px 1px at 20% 30%, rgba(255, 255, 255, 0.8), transparent),
    radial-gradient(1px 1px at 70% 15%, rgba(255, 255, 255, 0.6), transparent),
    radial-gradient(1px 1px at 45% 70%, rgba(255, 255, 255, 0.7), transparent),
    radial-gradient(1px 1px at 85% 55%, rgba(255, 255, 255, 0.5), transparent),
    radial-gradient(1px 1px at 12% 85%, rgba(255, 255, 255, 0.6), transparent);
  background-size: 260px 260px;
  opacity: 0.7;
  animation: twinkle 7s ease-in-out infinite alternate;
}

.stars-near {
  background-image:
    radial-gradient(2px 2px at 35% 22%, rgba(255, 246, 214, 0.95), transparent),
    radial-gradient(2px 2px at 78% 68%, rgba(200, 230, 255, 0.9), transparent),
    radial-gradient(1.5px 1.5px at 58% 44%, rgba(255, 255, 255, 0.85), transparent);
  background-size: 420px 420px;
  opacity: 0.75;
  animation: twinkle 4.5s ease-in-out infinite alternate-reverse;
}

.mote {
  position: absolute;
  bottom: -20px;
  border-radius: 50%;
  opacity: 0;
  animation-name: rise;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

@keyframes rise {
  0% {
    transform: translateY(0) scale(0.6);
    opacity: 0;
  }
  15% {
    opacity: 0.9;
  }
  85% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-105vh) scale(1.1);
    opacity: 0;
  }
}

@keyframes twinkle {
  from {
    opacity: 0.45;
  }
  to {
    opacity: 0.85;
  }
}

@keyframes drift {
  from {
    transform: translate3d(-2%, -1%, 0) scale(1);
  }
  to {
    transform: translate3d(3%, 2%, 0) scale(1.08);
  }
}
</style>
