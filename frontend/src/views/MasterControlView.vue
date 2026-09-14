<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from "vue";
import GlyphPanel from "@/components/GlyphPanel.vue";
import RuneButton from "@/components/RuneButton.vue";
import SchoolBadge from "@/components/SchoolBadge.vue";
import CharacterPortrait from "@/components/CharacterPortrait.vue";
import MonsterCard from "@/components/MonsterCard.vue";
import NoticeBar from "@/components/NoticeBar.vue";
import { api, ApiError } from "@/services/api";
import { useSystemsStore } from "@/stores/systems";
import { useTableStore } from "@/stores/table";
import type { EnemyOption, GameSystem, MusicTrack } from "@/types";

const props = defineProps<{ id: string }>();
const systems = useSystemsStore();
const table = useTableStore();

const bootstrapping = ref(true);
const error = ref<string | null>(null);
const notice = ref<string | null>(null);
const system = ref<GameSystem | null>(null);
const sessionName = ref("");

const enemies = ref<EnemyOption[]>([]);
const chosenEnemy = ref("");
const quantity = ref(1);
const spawning = ref(false);

const tracks = ref<MusicTrack[]>([]);
const chosenTrack = ref("");

const mediaInput = ref<HTMLInputElement | null>(null);
const displayTime = ref(10);
const uploading = ref(false);

/** Rascunhos editáveis por personagem/monstro (não sobrescrevem o que o Mestre digita). */
const characterDrafts = reactive<Record<string, Record<string, number>>>({});
const monsterDrafts = reactive<Record<string, { hp: number; mana: number; energia: number }>>({});

const playersOnline = computed(() => table.characters.length);

function draftFor(characterId: string) {
  if (!characterDrafts[characterId]) {
    const character = table.characterById(characterId);
    const draft: Record<string, number> = {};
    for (const resource of system.value?.resources ?? []) {
      draft[resource.key] = character?.resources[resource.key]?.current ?? 0;
    }
    characterDrafts[characterId] = draft;
  }
  return characterDrafts[characterId];
}

function monsterDraftFor(monsterId: string) {
  if (!monsterDrafts[monsterId]) {
    const monster = table.monsters.find((m) => m._id === monsterId);
    monsterDrafts[monsterId] = {
      hp: monster?.current_hp ?? 0,
      mana: monster?.current_mana ?? 0,
      energia: monster?.current_energia ?? 0,
    };
  }
  return monsterDrafts[monsterId];
}

async function bootstrap() {
  bootstrapping.value = true;
  try {
    await systems.ensureLoaded();
    const data = await api.get<{
      session: { name: string; system_id: string };
      enemies: EnemyOption[];
    }>(`/sessions/${props.id}/master`);
    sessionName.value = data.session.name;
    system.value = systems.get(data.session.system_id) ?? null;
    enemies.value = data.enemies;
    chosenEnemy.value = data.enemies[0]?._id ?? "";

    const music = await api.get<{ tracks: MusicTrack[] }>("/music");
    tracks.value = music.tracks;

    table.joinTable(props.id);
  } catch (err) {
    error.value = err instanceof ApiError ? err.message : "Não foi possível abrir o painel.";
  } finally {
    bootstrapping.value = false;
  }
}

function applyCharacter(characterId: string) {
  table.updateCharacterResources(characterId, { ...draftFor(characterId) });
  notice.value = "Status enviado para a mesa.";
}

function damage(characterId: string, resourceKey: string, delta: number) {
  const draft = draftFor(characterId);
  draft[resourceKey] = Math.max(0, (draft[resourceKey] ?? 0) + delta);
}

function applyMonster(monsterId: string) {
  table.updateMonsterStats(monsterId, { ...monsterDraftFor(monsterId) });
}

async function spawn() {
  if (!chosenEnemy.value) return;
  spawning.value = true;
  try {
    await api.post(`/sessions/${props.id}/monsters`, {
      monster_id: chosenEnemy.value,
      quantity: quantity.value,
    });
  } catch (err) {
    error.value = err instanceof ApiError ? err.message : "Falha ao invocar.";
  } finally {
    spawning.value = false;
  }
}

async function kick(characterId: string) {
  await api.post(`/sessions/${props.id}/players/${characterId}/kick`);
}

async function playTrack() {
  if (!chosenTrack.value) return;
  await api.post(`/sessions/${props.id}/music`, { track_url: chosenTrack.value });
}

async function stopTrack() {
  await api.post(`/sessions/${props.id}/music`, { track_url: null });
}

async function sendMedia() {
  const file = mediaInput.value?.files?.[0];
  if (!file) return;
  uploading.value = true;
  try {
    const form = new FormData();
    form.set("media", file);
    form.set("display_time", String(displayTime.value));
    await api.postForm(`/sessions/${props.id}/media`, form);
    notice.value = "Mídia enviada para os jogadores.";
    if (mediaInput.value) mediaInput.value.value = "";
  } catch (err) {
    error.value = err instanceof ApiError ? err.message : "Falha ao enviar mídia.";
  } finally {
    uploading.value = false;
  }
}

onMounted(bootstrap);
onBeforeUnmount(() => table.leaveTable());
</script>

<template>
  <main class="page">
    <header class="head">
      <div>
        <h1><span class="icon">👑</span> {{ sessionName || "Painel do Mestre" }}</h1>
        <p class="muted-on-dark">{{ system?.icon }} {{ system?.name }}</p>
      </div>
      <div class="row">
        <SchoolBadge :tone="table.connected ? 'life' : 'fire'">
          {{ table.connected ? "● ao vivo" : "○ reconectando" }}
        </SchoolBadge>
        <SchoolBadge tone="ice">{{ playersOnline }} na mesa</SchoolBadge>
        <SchoolBadge tone="fire">{{ table.monsterCount }} criaturas</SchoolBadge>
      </div>
    </header>

    <NoticeBar v-if="error" kind="error">{{ error }}</NoticeBar>
    <NoticeBar v-if="notice" kind="success">{{ notice }}</NoticeBar>
    <p v-if="bootstrapping" class="text-center muted-on-dark">Abrindo o grimório do Mestre…</p>

    <template v-else>
      <GlyphPanel title="Jogadores" icon="🛡️" tone="life">
        <p v-if="!table.characters.length" class="muted" style="margin: 0">
          Nenhum jogador entrou ainda. Compartilhe o link da mesa!
        </p>
        <div v-else class="players">
          <article v-for="character in table.characters" :key="character._id" class="player">
            <header class="player-head">
              <CharacterPortrait :src="character.img_url" size="sm" :tone="system?.tone" />
              <div>
                <strong>{{ character.name }}</strong>
                <div class="muted">{{ character.class_name }}</div>
              </div>
            </header>

            <div v-for="resource in system?.resources ?? []" :key="resource.key" class="res-row">
              <label>
                {{ resource.label }}
                <small>/ {{ character.resources[resource.key]?.max ?? 0 }}</small>
              </label>
              <div class="res-controls">
                <button type="button" @click="damage(character._id, resource.key, -5)">−5</button>
                <button type="button" @click="damage(character._id, resource.key, -1)">−1</button>
                <input
                  v-model.number="draftFor(character._id)[resource.key]"
                  type="number"
                  min="0"
                  :max="character.resources[resource.key]?.max ?? 999"
                />
                <button type="button" @click="damage(character._id, resource.key, 1)">+1</button>
                <button type="button" @click="damage(character._id, resource.key, 5)">+5</button>
              </div>
            </div>

            <div class="row" style="margin-top: 10px">
              <RuneButton tone="life" size="sm" @click="applyCharacter(character._id)">
                ✅ Aplicar
              </RuneButton>
              <RuneButton tone="fire" size="sm" @click="kick(character._id)">
                🚪 Remover
              </RuneButton>
            </div>
          </article>
        </div>
      </GlyphPanel>

      <GlyphPanel title="Invocar criaturas" icon="🐉" tone="fire">
        <form class="row" style="align-items: flex-end" @submit.prevent="spawn">
          <div class="grow">
            <label for="enemy">Criatura</label>
            <select id="enemy" v-model="chosenEnemy">
              <option v-for="enemy in enemies" :key="enemy._id" :value="enemy._id">
                {{ enemy.name }} — {{ enemy.hp }} PV
              </option>
            </select>
          </div>
          <div style="width: 120px">
            <label for="qty">Quantidade</label>
            <input id="qty" v-model.number="quantity" type="number" min="1" max="12" />
          </div>
          <RuneButton tone="fire" type="submit" :disabled="spawning">
            {{ spawning ? "Invocando…" : "🔥 Invocar" }}
          </RuneButton>
        </form>
      </GlyphPanel>

      <GlyphPanel title="Criaturas na mesa" icon="⚔️" tone="storm" dark>
        <p v-if="!table.monsters.length" class="muted-on-dark" style="margin: 0">
          Nenhuma criatura invocada.
        </p>
        <div v-else class="monsters">
          <MonsterCard v-for="monster in table.monsters" :key="monster._id" :monster="monster">
            <template #actions>
              <div class="monster-fields">
                <label>
                  PV
                  <input
                    v-model.number="monsterDraftFor(monster._id).hp"
                    type="number"
                    min="0"
                    :max="monster.hp"
                  />
                </label>
                <label>
                  Mana
                  <input v-model.number="monsterDraftFor(monster._id).mana" type="number" min="0" />
                </label>
                <label>
                  Energia
                  <input
                    v-model.number="monsterDraftFor(monster._id).energia"
                    type="number"
                    min="0"
                  />
                </label>
              </div>
              <RuneButton tone="life" size="sm" block @click="applyMonster(monster._id)">
                ✅ Aplicar
              </RuneButton>
              <RuneButton tone="fire" size="sm" block @click="table.removeMonster(monster._id)">
                🗑️ Remover
              </RuneButton>
            </template>
          </MonsterCard>
        </div>
      </GlyphPanel>

      <div class="two-up">
        <GlyphPanel title="Trilha sonora" icon="🎵" tone="ice">
          <label for="track">Faixa</label>
          <select id="track" v-model="chosenTrack">
            <option value="">Selecione…</option>
            <option v-for="track in tracks" :key="track.url" :value="track.url">
              {{ track.name }}
            </option>
          </select>
          <p class="muted">
            Tocando agora:
            <strong>{{ table.currentTrack ? table.currentTrack.split("/").pop() : "nada" }}</strong>
          </p>
          <div class="row">
            <RuneButton tone="ice" size="sm" :disabled="!chosenTrack" @click="playTrack">
              ▶️ Tocar para todos
            </RuneButton>
            <RuneButton tone="fire" size="sm" @click="stopTrack">⏹️ Parar</RuneButton>
          </div>
        </GlyphPanel>

        <GlyphPanel title="Mostrar imagem / vídeo" icon="🖼️" tone="balance">
          <label for="media">Arquivo</label>
          <input id="media" ref="mediaInput" type="file" accept="image/*,video/*" />
          <label for="display-time">Tempo na tela (segundos)</label>
          <input id="display-time" v-model.number="displayTime" type="number" min="0" max="120" />
          <RuneButton tone="balance" size="sm" block :disabled="uploading" @click="sendMedia">
            {{ uploading ? "Enviando…" : "📤 Enviar para a mesa" }}
          </RuneButton>
        </GlyphPanel>
      </div>
    </template>
  </main>
</template>

<style scoped>
.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.head h1 {
  margin: 0;
}

.head p {
  margin: 0;
}

.players {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 14px;
}

.player {
  padding: 14px;
  border-radius: var(--radius-md);
  background: #fffdf8;
  box-shadow: inset 0 0 0 2px var(--scroll-300), var(--lift-1);
}

.player-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.player-head strong {
  font-size: 1.05rem;
}

.res-row {
  margin-bottom: 8px;
}

.res-row label {
  margin-bottom: 4px;
}

.res-row small {
  color: var(--ink-500);
  font-weight: 600;
}

.res-controls {
  display: flex;
  align-items: center;
  gap: 5px;
}

.res-controls input {
  margin: 0;
  text-align: center;
  padding: 6px;
}

.res-controls button {
  flex-shrink: 0;
  min-width: 38px;
  padding: 7px 4px;
  border: none;
  border-radius: var(--radius-sm);
  font-weight: 800;
  font-size: 0.8rem;
  cursor: pointer;
  color: #fff;
  background: linear-gradient(180deg, var(--gold-300), var(--gold-500));
  box-shadow: 0 0 0 2px var(--gold-700), 0 2px 0 var(--gold-700);
}

.res-controls button:hover {
  filter: brightness(1.07);
}

.monsters {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.monster-fields {
  display: grid;
  gap: 5px;
  margin-bottom: 6px;
}

.monster-fields label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  margin: 0;
  font-size: 0.74rem;
  color: var(--ink-onDark-muted);
}

.monster-fields input {
  width: 74px;
  margin: 0;
  padding: 4px 6px;
  font-size: 0.82rem;
}

.two-up {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 18px;
}
</style>
