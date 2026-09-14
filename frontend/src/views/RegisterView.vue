<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import GlyphPanel from "@/components/GlyphPanel.vue";
import RuneButton from "@/components/RuneButton.vue";
import NoticeBar from "@/components/NoticeBar.vue";
import { useAuthStore } from "@/stores/auth";
import { ApiError } from "@/services/api";

const auth = useAuthStore();
const router = useRouter();

const username = ref("");
const password = ref("");
const error = ref<string | null>(null);
const busy = ref(false);

async function submit() {
  error.value = null;
  if (password.value.length < 4) {
    error.value = "Use uma senha com pelo menos 4 caracteres.";
    return;
  }
  busy.value = true;
  try {
    await auth.register(username.value.trim(), password.value);
    router.push({ name: "characters" });
  } catch (err) {
    error.value = err instanceof ApiError ? err.message : "Não foi possível criar a conta.";
  } finally {
    busy.value = false;
  }
}
</script>

<template>
  <main class="page page-narrow gate">
    <h1 class="text-center">Novo Aventureiro</h1>
    <p class="text-center muted-on-dark">Crie sua conta para entrar nas mesas.</p>

    <GlyphPanel tone="life">
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
            autocomplete="new-password"
            required
          />
        </div>
        <RuneButton tone="life" size="lg" type="submit" block :disabled="busy">
          {{ busy ? "Inscrevendo…" : "📜 Criar conta" }}
        </RuneButton>
      </form>
      <p class="text-center muted" style="margin-top: 14px">
        Já tem conta?
        <RouterLink :to="{ name: 'login' }">Entrar</RouterLink>
      </p>
    </GlyphPanel>
  </main>
</template>

<style scoped>
.gate {
  padding-top: 64px;
}
</style>
