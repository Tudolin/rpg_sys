<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import GlyphPanel from "@/components/GlyphPanel.vue";
import RuneButton from "@/components/RuneButton.vue";
import SchoolBadge from "@/components/SchoolBadge.vue";
import NoticeBar from "@/components/NoticeBar.vue";
import ModalDialog from "@/components/ModalDialog.vue";
import { api, ApiError } from "@/services/api";
import { useSystemsStore } from "@/stores/systems";
import type { GameSessionSummary } from "@/types";

const router = useRouter();
const systems = useSystemsStore();

const sessions = ref<GameSessionSummary[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

const newName = ref("");
const newSystem = ref("medieval");
const creating = ref(false);
const pendingDelete = ref<GameSessionSummary | null>(null);

async function load() {
  loading.value = true;
  try {
    await systems.ensureLoaded();
    newSystem.value = systems.systems[0]?.id ?? "medieval";
    const data = await api.get<{ sessions: GameSessionSummary[] }>("/sessions");
    sessions.value = data.sessions;
  } catch {
    error.value = "Não foi possível carregar as mesas.";
  } finally {
    loading.value = false;
  }
}

async function createSession() {
  if (!newName.value.trim()) return;
  creating.value = true;
  error.value = null;
  try {
    const data = await api.post<{ session: GameSessionSummary }>("/sessions", {
      name: newName.value.trim(),
      system_id: newSystem.value,
    });
    sessions.value.unshift(data.session);
    newName.value = "";
  } catch (err) {
    error.value = err instanceof ApiError ? err.message : "Não foi possível criar a mesa.";
  } finally {
    creating.value = false;
  }
}

async function confirmDelete() {
  const target = pendingDelete.value;
  if (!target) return;
  pendingDelete.value = null;
  await api.delete(`/sessions/${target._id}`);
  sessions.value = sessions.value.filter((s) => s._id !== target._id);
}

onMounted(load);
</script>

<template>
  <main class="page">
    <h1 class="text-center">Mesas</h1>
    <p class="text-center muted-on-dark">
      Cada mesa roda um sistema. Quem cria a mesa é o Mestre dela.
    </p>

    <NoticeBar v-if="error" kind="error">{{ error }}</NoticeBar>

    <GlyphPanel title="Abrir nova mesa" icon="🕯️" tone="storm">
      <form class="stack" @submit.prevent="createSession">
        <div>
          <label for="session-name">Nome da mesa</label>
          <input id="session-name" v-model="newName" placeholder="Ex: A Torre Esquecida" required />
        </div>

        <div>
          <label>Sistema</label>
          <div class="systems">
            <button
              v-for="system in systems.systems"
              :key="system.id"
              type="button"
              class="system-card"
              :class="[`tone-${system.tone}`, { active: system.id === newSystem }]"
              @click="newSystem = system.id"
            >
              <span class="system-icon">{{ system.icon }}</span>
              <strong>{{ system.name }}</strong>
              <small>{{ system.tagline }}</small>
            </button>
          </div>
        </div>

        <RuneButton tone="storm" size="lg" type="submit" block :disabled="creating">
          {{ creating ? "Acendendo velas…" : "🎲 Criar mesa" }}
        </RuneButton>
      </form>
    </GlyphPanel>

    <h2 class="text-center">Mesas disponíveis</h2>
    <p v-if="loading" class="text-center muted-on-dark">Procurando mesas…</p>

    <div v-else-if="sessions.length" class="list">
      <GlyphPanel
        v-for="session in sessions"
        :key="session._id"
        :tone="systems.get(session.system_id)?.tone ?? 'gold'"
        thin
      >
        <div class="session">
          <div class="session-info">
            <h3>
              <span class="icon">{{ systems.get(session.system_id)?.icon }}</span>
              {{ session.name }}
            </h3>
            <div class="row">
              <SchoolBadge :tone="systems.get(session.system_id)?.tone ?? 'gold'">
                {{ systems.get(session.system_id)?.name ?? session.system_id }}
              </SchoolBadge>
              <SchoolBadge tone="life">
                {{ session.player_count }} {{ session.player_count === 1 ? "jogador" : "jogadores" }}
              </SchoolBadge>
              <SchoolBadge v-if="session.is_master" tone="myth" icon="👑">Você é o Mestre</SchoolBadge>
            </div>
            <p class="muted">Mestre: {{ session.creator_name }}</p>
          </div>

          <div class="row session-actions">
            <RuneButton
              tone="ice"
              size="sm"
              @click="router.push({ name: 'join', params: { id: session._id } })"
            >
              🚪 Entrar
            </RuneButton>
            <RuneButton
              v-if="session.is_master"
              tone="myth"
              size="sm"
              @click="router.push({ name: 'master', params: { id: session._id } })"
            >
              👑 Mestrar
            </RuneButton>
            <RuneButton v-if="session.is_master" tone="fire" size="sm" @click="pendingDelete = session">
              🗑️
            </RuneButton>
          </div>
        </div>
      </GlyphPanel>
    </div>

    <GlyphPanel v-else dark tone="ice">
      <p class="text-center" style="margin: 0">Nenhuma mesa aberta. Crie a primeira!</p>
    </GlyphPanel>

    <ModalDialog v-if="pendingDelete" title="Excluir mesa?" @close="pendingDelete = null">
      <p>
        A mesa <strong>{{ pendingDelete.name }}</strong> e todo o seu estado serão removidos.
      </p>
      <template #footer>
        <RuneButton tone="ice" size="sm" @click="pendingDelete = null">Cancelar</RuneButton>
        <RuneButton tone="fire" size="sm" @click="confirmDelete">Excluir</RuneButton>
      </template>
    </ModalDialog>
  </main>
</template>

<style scoped>
.systems {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 10px;
}

.system-card {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 13px;
  border: none;
  border-radius: var(--radius-md);
  background: linear-gradient(170deg, #fffdf7, var(--scroll-200));
  box-shadow: 0 0 0 2px var(--scroll-300), var(--lift-1);
  cursor: pointer;
  text-align: left;
  font-family: var(--font-ui);
  color: var(--ink-900);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.system-card:hover {
  transform: translateY(-3px);
}

.system-card.active {
  box-shadow: 0 0 0 3px var(--tone-deep), 0 0 0 6px var(--tone), 0 0 18px var(--tone), var(--lift-1);
}

.system-icon {
  font-size: 1.7rem;
}

.system-card small {
  color: var(--ink-500);
  line-height: 1.3;
}

.list {
  display: grid;
  gap: 16px;
}

.session {
  display: flex;
  gap: 16px;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.session-info h3 {
  margin: 0 0 8px;
  color: var(--ink-900);
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.session-info .icon {
  font-size: 1.5rem;
}

.session-info .muted {
  margin: 8px 0 0;
}

.session-actions {
  flex-wrap: nowrap;
}
</style>
