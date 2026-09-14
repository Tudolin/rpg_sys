<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import GlyphPanel from "@/components/GlyphPanel.vue";
import RuneButton from "@/components/RuneButton.vue";
import NoticeBar from "@/components/NoticeBar.vue";
import { useAuthStore } from "@/stores/auth";
import { ApiError } from "@/services/api";

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

const username = ref("");
const password = ref("");
const error = ref<string | null>(null);
const busy = ref(false);

async function submit() {
  error.value = null;
  busy.value = true;
  try {
    await auth.login(username.value.trim(), password.value);
    const next = typeof route.query.next === "string" ? route.query.next : undefined;
    router.push(next ?? { name: "characters" });
  } catch (err) {
    error.value = err instanceof ApiError ? err.message : "Não foi possível entrar.";
  } finally {
    busy.value = false;
  }
}
</script>

<template>
  <main class="page page-narrow gate">
    <div class="sigil">
      <img src="/static/logo.png" alt="" />
    </div>
    <h1 class="text-center">Mesa Arcana</h1>
    <p class="text-center muted-on-dark">Reúna sua party e comece a aventura.</p>

    <GlyphPanel tone="ice">
      <NoticeBar v-if="error" kind="error">{{ error }}</NoticeBar>
      <form class="stack" @submit.prevent="submit">
        <div>
          <label for="username">Usuário</label>
          <input id="username" v-model="username" autocomplete="username" required autofocus />
        </div>
        <div>
          <label for="password">Senha</label>
          <input
            id="password"
            v-model="password"
            type="password"
            autocomplete="current-password"
            required
          />
        </div>
        <RuneButton tone="ice" size="lg" type="submit" block :disabled="busy">
          {{ busy ? "Abrindo o portal…" : "⚔️ Entrar" }}
        </RuneButton>
      </form>
      <p class="text-center muted" style="margin-top: 14px">
        Ainda não tem conta?
        <RouterLink :to="{ name: 'register' }">Crie a sua</RouterLink>
      </p>
    </GlyphPanel>
  </main>
</template>

<style scoped>
.gate {
  padding-top: 52px;
}

.sigil {
  display: flex;
  justify-content: center;
  margin-bottom: 14px;
}

.sigil img {
  width: 92px;
  height: 92px;
  border-radius: 50%;
  background: var(--void-900);
  box-shadow:
    0 0 0 3px var(--gold-600),
    0 0 0 6px var(--gold-300),
    0 0 0 9px var(--gold-700),
    0 0 34px rgba(240, 181, 55, 0.55);
  animation: float 5s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}
</style>
