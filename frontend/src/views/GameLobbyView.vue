<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import GlyphPanel from "@/components/GlyphPanel.vue";
import RuneButton from "@/components/RuneButton.vue";
import ResourceOrb from "@/components/ResourceOrb.vue";
import CharacterPortrait from "@/components/CharacterPortrait.vue";
import SchoolBadge from "@/components/SchoolBadge.vue";
import MonsterCard from "@/components/MonsterCard.vue";
import ModalDialog from "@/components/ModalDialog.vue";
import NoticeBar from "@/components/NoticeBar.vue";
import { api, ApiError } from "@/services/api";
import { useSystemsStore } from "@/stores/systems";
import { useTableStore } from "@/stores/table";
import type { Ability, Character, GameSystem } from "@/types";

const props = defineProps<{ id: string }>();
const systems = useSystemsStore();
const table = useTableStore();

const bootstrapping = ref(true);
const error = ref<string | null>(null);
const myCharacterId = ref<string | null>(null);
const system = ref<GameSystem | null>(null);
const inspecting = ref<Character | null>(null);
const busyAbility = ref<string | null>(null);

const diceResult = ref<number | null>(null);
const rolling = ref(false);

const audio = ref<HTMLAudioElement | null>(null);
const volume = ref(0.5);

/** Meu personagem vem do snapshot ao vivo, então HP/mana sempre atualizados. */
const me = computed<Character | null>(() =>
  myCharacterId.value ? table.characterById(myCharacterId.value) : null,
);

const allies = computed(() =>
  table.characters.filter((character) => character._id !== myCharacterId.value),
);

async function bootstrap() {
  bootstrapping.value = true;
  try {
    await systems.ensureLoaded();
    const data = await api.get<{ system_id: string; character_id: string | null }>(
      `/sessions/${props.id}/table`,
    );
    system.value = systems.get(data.system_id) ?? null;
    myCharacterId.value = data.character_id;
    table.joinTable(props.id);
  } catch (err) {
    error.value = err instanceof ApiError ? err.message : "Não foi possível abrir a mesa.";
  } finally {
    bootstrapping.value = false;
  }
}

function canAfford(ability: Ability) {
  if (!me.value) return false;
  return Object.entries(ability.cost ?? {}).every(
    ([key, amount]) => (me.value?.resources[key]?.current ?? 0) >= amount,
  );
}

async function useAbility(ability: Ability) {
  if (!me.value || !canAfford(ability) || busyAbility.value) return;
  busyAbility.value = ability.id;
  try {
    await api.post(`/characters/${me.value._id}/use-ability`, { ability_id: ability.id });
  } catch (err) {
    error.value = err instanceof ApiError ? err.message : "Falha ao usar a habilidade.";
  } finally {
    busyAbility.value = null;
  }
}

function rollDice() {
  if (rolling.value) return;
  rolling.value = true;
  diceResult.value = null;
  window.setTimeout(() => {
    diceResult.value = Math.floor(Math.random() * 20) + 1;
    rolling.value = false;
  }, 900);
}

function resourceTone(key: string) {
  return system.value?.resources.find((resource) => resource.key === key)?.color ?? "gold";
}

// Trilha sonora controlada pelo Mestre via socket.
watch(
  () => table.currentTrack,
  (track) => {
    const element = audio.value;
    if (!element) return;
    if (!track) {
      element.pause();
      element.removeAttribute("src");
      return;
    }
    if (element.src.endsWith(track)) return;
    element.src = track;
    element.volume = volume.value;
    element.play().catch(() => {
      /* precisa de interação do usuário — o controle de volume serve para isso */
    });
  },
);

watch(volume, (value) => {
  if (audio.value) audio.value.volume = value;
});

onMounted(bootstrap);
onBeforeUnmount(() => table.leaveTable());
</script>

<template>
  <main class="page lobby">
    <header class="lobby-head">
      <div>
        <h1>
          <span class="icon">{{ system?.icon }}</span>
          Mesa em andamento
        </h1>
        <p class="muted-on-dark">{{ system?.name }}</p>
      </div>
      <div class="row">
        <SchoolBadge :tone="table.connected ? 'life' : 'fire'">
          {{ table.connected ? "● ao vivo" : "○ reconectando" }}
        </SchoolBadge>
        <label class="volume">
          🔊
          <input v-model.number="volume" type="range" min="0" max="1" step="0.01" />
        </label>
      </div>
    </header>

    <NoticeBar v-if="error" kind="error">{{ error }}</NoticeBar>
    <NoticeBar v-if="table.errorMessage" kind="error">{{ table.errorMessage }}</NoticeBar>
    <p v-if="bootstrapping" class="text-center muted-on-dark">Conjurando a mesa…</p>

    <div v-else class="layout">
      <!-- Party -->
      <GlyphPanel title="Party" icon="🛡️" tone="life" dark thin class="party">
        <p v-if="!allies.length" class="muted-on-dark" style="margin: 0">
          Ninguém mais entrou ainda.
        </p>
        <ul v-else class="party-list">
          <li v-for="ally in allies" :key="ally._id">
            <button type="button" class="ally" @click="inspecting = ally">
              <CharacterPortrait :src="ally.img_url" size="sm" />
              <span class="ally-info">
                <strong>{{ ally.name }}</strong>
                <small>{{ ally.class_name }}</small>
                <span class="ally-orbs">
                  <ResourceOrb
                    v-for="resource in system?.resources ?? []"
                    :key="resource.key"
                    size="sm"
                    :tone="resource.color"
                    :label="resource.label"
                    :current="ally.resources[resource.key]?.current ?? 0"
                    :max="ally.resources[resource.key]?.max ?? 0"
                  />
                </span>
              </span>
            </button>
          </li>
        </ul>
      </GlyphPanel>

      <!-- Campo de batalha -->
      <section class="board">
        <h2 class="board-title">Campo de Batalha</h2>
        <div v-if="table.monsters.length" class="monsters">
          <MonsterCard v-for="monster in table.monsters" :key="monster._id" :monster="monster" />
        </div>
        <GlyphPanel v-else dark tone="storm" thin>
          <p class="text-center" style="margin: 0">
            Nenhuma criatura invocada. Aproveite a calmaria…
          </p>
        </GlyphPanel>

        <div class="dice-zone">
          <RuneButton tone="myth" size="lg" :disabled="rolling" @click="rollDice">
            🎲 Rolar d20
          </RuneButton>
          <Transition name="pop">
            <div v-if="diceResult !== null" class="dice-result" :class="{ crit: diceResult === 20, fail: diceResult === 1 }">
              {{ diceResult }}
            </div>
          </Transition>
          <div v-if="rolling" class="dice-rolling">🎲</div>
        </div>
      </section>

      <!-- Ficha do jogador -->
      <GlyphPanel v-if="me" :title="me.name" :icon="system?.icon" :tone="system?.tone" class="sheet">
        <div class="sheet-top">
          <CharacterPortrait :src="me.img_url" size="lg" :tone="system?.tone" />
          <div class="row row-center" style="margin-top: 10px">
            <SchoolBadge tone="balance">{{ me.class_name }}</SchoolBadge>
            <SchoolBadge v-if="me.race_name" tone="life">{{ me.race_name }}</SchoolBadge>
          </div>
        </div>

        <div class="my-orbs">
          <ResourceOrb
            v-for="resource in system?.resources ?? []"
            :key="resource.key"
            size="lg"
            :tone="resource.color"
            :label="resource.label"
            :current="me.resources[resource.key]?.current ?? 0"
            :max="me.resources[resource.key]?.max ?? 0"
          />
        </div>

        <RuneButton tone="ice" size="sm" block @click="inspecting = me">
          📖 Ver ficha completa
        </RuneButton>
      </GlyphPanel>
    </div>

    <!-- Barra de habilidades -->
    <footer v-if="me" class="spellbar">
      <div class="spells">
        <button
          v-for="ability in me.habilidades"
          :key="ability.id"
          type="button"
          class="spell"
          :class="{ locked: !canAfford(ability) }"
          :disabled="!canAfford(ability) || busyAbility === ability.id"
          :title="ability.description"
          @click="useAbility(ability)"
        >
          <img
            :src="`/static/images/skills/${ability.icon ?? 'default_icon.png'}`"
            :alt="ability.name"
            @error="($event.target as HTMLImageElement).src = '/static/icons/buff icon.png'"
          />
          <span class="spell-name">{{ ability.name }}</span>
          <span class="spell-cost">
            <SchoolBadge
              v-for="(amount, key) in ability.cost"
              :key="key"
              :tone="resourceTone(String(key))"
            >
              {{ amount }}
            </SchoolBadge>
          </span>
        </button>
        <p v-if="!me.habilidades.length" class="muted-on-dark" style="margin: 0">
          Este personagem ainda não tem habilidades registradas.
        </p>
      </div>
    </footer>

    <!-- Mídia enviada pelo Mestre -->
    <Teleport to="body">
      <div v-if="table.mediaOverlay" class="media-veil" @click="table.dismissMedia()">
        <div class="media-frame frame-gold">
          <video
            v-if="/\.(mp4|webm)$/i.test(table.mediaOverlay.url)"
            :src="table.mediaOverlay.url"
            autoplay
            controls
          />
          <img v-else :src="table.mediaOverlay.url" alt="" />
        </div>
      </div>
    </Teleport>

    <audio ref="audio" />

    <ModalDialog v-if="inspecting" :title="inspecting.name" wide @close="inspecting = null">
      <div class="row" style="align-items: flex-start; gap: 18px">
        <CharacterPortrait :src="inspecting.img_url" size="md" :tone="system?.tone" />
        <div class="grow">
          <div class="row">
            <SchoolBadge tone="balance">{{ inspecting.class_name }}</SchoolBadge>
            <SchoolBadge v-if="inspecting.race_name" tone="life">
              {{ inspecting.race_name }}
            </SchoolBadge>
          </div>
          <dl class="sheet-attrs">
            <div v-for="attr in system?.attributes ?? []" :key="attr.key">
              <dt>{{ attr.label }}</dt>
              <dd>{{ inspecting.attributes[attr.key] ?? 0 }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <h3>{{ system?.ability_label }}</h3>
      <ul class="sheet-list">
        <li v-for="ability in inspecting.habilidades" :key="ability.id">
          <strong>{{ ability.name }}</strong> — {{ ability.description }}
        </li>
        <li v-if="!inspecting.habilidades.length" class="muted">Nenhuma.</li>
      </ul>

      <h3>{{ system?.skill_label }}</h3>
      <div class="row">
        <SchoolBadge
          v-for="(value, skill) in inspecting.pericias"
          :key="skill"
          tone="life"
        >
          {{ skill }} +{{ value }}
        </SchoolBadge>
        <span v-if="!Object.keys(inspecting.pericias).length" class="muted">Nenhuma.</span>
      </div>
    </ModalDialog>
  </main>
</template>

<style scoped>
.lobby {
  /* Espaço para a barra de habilidades fixa no rodapé não cobrir a ficha. */
  padding-bottom: 190px;
}

.lobby-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 14px;
}

.lobby-head h1 {
  margin: 0;
  font-size: clamp(1.6rem, 4vw, 2.3rem);
}

.lobby-head p {
  margin: 0;
}

.volume {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0;
  color: var(--ink-onDark-muted);
}

.volume input {
  width: 110px;
  padding: 0;
}

.layout {
  display: grid;
  grid-template-columns: 260px 1fr 300px;
  gap: 18px;
  align-items: start;
}

.party-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 8px;
}

.ally {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 8px;
  border: none;
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.05);
  color: var(--ink-onDark);
  cursor: pointer;
  text-align: left;
  font-family: var(--font-ui);
  transition: background 0.15s ease, transform 0.15s ease;
}

.ally:hover {
  background: rgba(240, 181, 55, 0.16);
  transform: translateX(2px);
}

.ally-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.ally-info small {
  color: var(--ink-onDark-muted);
}

.ally-orbs {
  display: flex;
  gap: 6px;
  margin-top: 4px;
}

.board-title {
  text-align: center;
  margin-bottom: 12px;
}

.monsters {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}

.dice-zone {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-top: 26px;
}

.dice-result {
  font-family: var(--font-display);
  font-size: 3.4rem;
  line-height: 1;
  padding: 14px 30px;
  border-radius: var(--radius-lg);
  color: var(--gold-100);
  background: linear-gradient(170deg, var(--void-600), var(--void-800));
  box-shadow:
    0 0 0 3px var(--gold-600),
    0 0 0 6px var(--gold-300),
    0 0 28px rgba(240, 181, 55, 0.5);
}

.dice-result.crit {
  color: #fff;
  background: linear-gradient(170deg, var(--school-life), var(--school-life-deep));
  box-shadow: 0 0 0 3px var(--gold-300), 0 0 34px var(--school-life);
}

.dice-result.fail {
  background: linear-gradient(170deg, var(--school-fire), var(--school-fire-deep));
  box-shadow: 0 0 0 3px var(--gold-300), 0 0 34px var(--school-fire);
}

.dice-rolling {
  font-size: 3rem;
  animation: tumble 0.9s linear;
}

.sheet-top {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.my-orbs {
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
  margin: 18px 0;
  padding: 14px;
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, var(--void-700), var(--void-800));
  box-shadow: inset 0 3px 10px rgba(0, 0, 0, 0.5), 0 0 0 2px var(--gold-600);
}

.spellbar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 50;
  padding: 10px 16px;
  background: linear-gradient(180deg, rgba(36, 26, 82, 0.96), rgba(16, 10, 38, 0.98));
  border-top: 3px solid var(--gold-500);
  box-shadow: 0 -8px 24px rgba(10, 6, 25, 0.6);
}

.spells {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: center;
  overflow-x: auto;
  padding-bottom: 4px;
}

.spell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  min-width: 86px;
  padding: 8px 10px;
  border: none;
  border-radius: var(--radius-md);
  background: linear-gradient(170deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.04));
  color: var(--ink-onDark);
  font-family: var(--font-ui);
  cursor: pointer;
  transition: transform 0.14s ease, box-shadow 0.14s ease;
  box-shadow: 0 0 0 2px var(--gold-700);
}

.spell:hover:not(:disabled) {
  transform: translateY(-4px);
  box-shadow: 0 0 0 2px var(--gold-400), 0 0 18px rgba(240, 181, 55, 0.5);
}

.spell img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--void-900);
  box-shadow: 0 0 0 2px var(--gold-500);
}

.spell-name {
  font-size: 0.72rem;
  font-weight: 700;
  max-width: 96px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.spell-cost {
  display: flex;
  gap: 4px;
}

.spell.locked {
  filter: grayscale(0.8) brightness(0.65);
  cursor: not-allowed;
}

.media-veil {
  position: fixed;
  inset: 0;
  z-index: 300;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: rgba(10, 6, 25, 0.88);
  backdrop-filter: blur(6px);
  cursor: zoom-out;
}

.media-frame {
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--void-800);
  max-width: min(1000px, 92vw);
  max-height: 86vh;
  display: flex;
}

.media-frame img,
.media-frame video {
  max-width: 100%;
  max-height: 86vh;
  display: block;
}

.sheet-attrs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 6px;
  margin: 12px 0 0;
}

.sheet-attrs div {
  display: flex;
  justify-content: space-between;
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  background: rgba(58, 36, 16, 0.07);
}

.sheet-attrs dt {
  font-weight: 600;
  color: var(--ink-500);
}

.sheet-attrs dd {
  margin: 0;
  font-weight: 800;
}

.sheet-list {
  margin: 0 0 14px;
  padding-left: 18px;
  line-height: 1.5;
}

.pop-enter-active {
  animation: pop-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes pop-in {
  from {
    transform: scale(0.4) rotate(-12deg);
    opacity: 0;
  }
}

@keyframes tumble {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(720deg);
  }
}

@media (max-width: 1080px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .party,
  .sheet {
    max-width: 520px;
    margin-left: auto;
    margin-right: auto;
  }
}
</style>
