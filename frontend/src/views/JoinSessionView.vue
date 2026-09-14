<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import GlyphPanel from "@/components/GlyphPanel.vue";
import RuneButton from "@/components/RuneButton.vue";
import NoticeBar from "@/components/NoticeBar.vue";
import SchoolBadge from "@/components/SchoolBadge.vue";
import CharacterPortrait from "@/components/CharacterPortrait.vue";
import { api, ApiError } from "@/services/api";
import { useSystemsStore } from "@/stores/systems";
import type { Character } from "@/types";

const props = defineProps<{ id: string }>();
const router = useRouter();
const systems = useSystemsStore();

interface JoinPayload {
  session: { _id: string; name: string; system_id: string; creator_name: string };
  is_master: boolean;
  my_characters: Character[];
  my_character_id: string | null;
}

const payload = ref<JoinPayload | null>(null);
const selected = ref<string>("");
const loading = ref(true);
const joining = ref(false);
const error = ref<string | null>(null);

const system = computed(() => systems.get(payload.value?.session.system_id));

async function load() {
  loading.value = true;
  try {
    await systems.ensureLoaded();
    payload.value = await api.get<JoinPayload>(`/sessions/${props.id}`);
    selected.value = payload.value.my_character_id ?? payload.value.my_characters[0]?._id ?? "";
  } catch (err) {
    error.value = err instanceof ApiError ? err.message : "Mesa não encontrada.";
  } finally {
    loading.value = false;
  }
}

async function join() {
  if (!selected.value) return;
  joining.value = true;
  error.value = null;
  try {
    await api.post(`/sessions/${props.id}/join`, { character_id: selected.value });
    router.push({ name: "lobby", params: { id: props.id } });
  } catch (err) {
    error.value = err instanceof ApiError ? err.message : "Não foi possível entrar na mesa.";
  } finally {
    joining.value = false;
  }
}

onMounted(load);
</script>

<template>
  <main class="page page-narrow">
    <p v-if="loading" class="text-center muted-on-dark">Abrindo as portas…</p>
    <NoticeBar v-else-if="error" kind="error">{{ error }}</NoticeBar>

    <template v-if="payload">
      <h1 class="text-center">
        <span class="icon">{{ system?.icon }}</span> {{ payload.session.name }}
      </h1>
      <p class="text-center muted-on-dark">{{ system?.name }} — {{ system?.tagline }}</p>

      <div v-if="payload.is_master" class="row row-center" style="margin-bottom: 18px">
        <RuneButton
          tone="myth"
          @click="router.push({ name: 'master', params: { id: props.id } })"
        >
          👑 Abrir painel do Mestre
        </RuneButton>
      </div>

      <GlyphPanel
        v-if="payload.my_characters.length"
        title="Escolha seu personagem"
        icon="🧙"
        :tone="system?.tone"
      >
        <div class="picks">
          <button
            v-for="character in payload.my_characters"
            :key="character._id"
            type="button"
            class="pick"
            :class="{ on: selected === character._id }"
            @click="selected = character._id"
          >
            <CharacterPortrait :src="character.img_url" size="sm" :tone="system?.tone" />
            <span class="pick-info">
              <strong>{{ character.name }}</strong>
              <span class="row">
                <SchoolBadge tone="balance">{{ character.class_name }}</SchoolBadge>
                <SchoolBadge v-if="character.race_name" tone="life">
                  {{ character.race_name }}
                </SchoolBadge>
              </span>
            </span>
          </button>
        </div>

        <RuneButton
          :tone="system?.tone ?? 'gold'"
          size="lg"
          block
          style="margin-top: 16px"
          :disabled="joining || !selected"
          @click="join"
        >
          {{ joining ? "Entrando…" : "🚪 Entrar na mesa" }}
        </RuneButton>
      </GlyphPanel>

      <GlyphPanel v-else dark tone="fire" title="Sem personagens compatíveis" icon="⚠️">
        <p>
          Você ainda não tem nenhum personagem de <strong>{{ system?.name }}</strong
          >. Crie um para poder entrar nesta mesa.
        </p>
        <RuneButton tone="myth" block @click="router.push({ name: 'character-new' })">
          ✨ Criar personagem
        </RuneButton>
      </GlyphPanel>
    </template>
  </main>
</template>

<style scoped>
.icon {
  font-size: 0.9em;
}

.picks {
  display: grid;
  gap: 10px;
}

.pick {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 11px 14px;
  border: none;
  border-radius: var(--radius-md);
  background: #fffdf8;
  box-shadow: inset 0 0 0 2px var(--scroll-300);
  cursor: pointer;
  font-family: var(--font-ui);
  color: var(--ink-900);
  text-align: left;
  transition: transform 0.14s ease;
}

.pick:hover {
  transform: translateY(-2px);
}

.pick.on {
  background: linear-gradient(170deg, #fff6df, var(--scroll-200));
  box-shadow: 0 0 0 3px var(--gold-600), 0 0 0 6px var(--gold-300), var(--lift-1);
}

.pick-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.pick-info strong {
  font-size: 1.1rem;
}
</style>
