<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import GlyphPanel from "@/components/GlyphPanel.vue";
import RuneButton from "@/components/RuneButton.vue";
import NoticeBar from "@/components/NoticeBar.vue";
import SchoolBadge from "@/components/SchoolBadge.vue";
import CharacterPortrait from "@/components/CharacterPortrait.vue";
import { api, ApiError } from "@/services/api";
import { useSystemsStore } from "@/stores/systems";
import type { Character, GameSystem, SystemOptions } from "@/types";

const props = defineProps<{ id?: string }>();
const router = useRouter();
const systems = useSystemsStore();

const BASE_POINTS = 10;
const ATTR_MIN = 3;
const ATTR_MAX = 18;
const MAX_SKILLS = 3;
const MAX_ABILITIES = 5;

const isEdit = computed(() => Boolean(props.id));

const systemId = ref<string>("medieval");
const options = ref<SystemOptions>({ classes: [], races: [], abilities: [] });
const loading = ref(true);
const saving = ref(false);
const error = ref<string | null>(null);

const name = ref("");
const classId = ref("");
const raceId = ref("");
const origem = ref("");
const attributes = ref<Record<string, number>>({});
const chosenSkills = ref<string[]>([]);
const chosenAbilities = ref<string[]>([]);
const imageFile = ref<File | null>(null);
const imagePreview = ref<string | null>(null);
const existingImage = ref<string | null>(null);

const system = computed<GameSystem | undefined>(() => systems.get(systemId.value));
const selectedClass = computed(() => options.value.classes.find((c) => c._id === classId.value));
const selectedRace = computed(() => options.value.races.find((r) => r._id === raceId.value));

const spentPoints = computed(() =>
  Object.values(attributes.value).reduce((total, value) => total + (value - 10), 0),
);
const remainingPoints = computed(() => BASE_POINTS - spentPoints.value);

/** Atributos com o bônus racial já aplicado (o que o servidor vai gravar). */
const effectiveAttributes = computed<Record<string, number>>(() => {
  const result: Record<string, number> = {};
  for (const attr of system.value?.attributes ?? []) {
    const base = attributes.value[attr.key] ?? 10;
    result[attr.key] = base + (selectedRace.value?.attribute_bonuses?.[attr.key] ?? 0);
  }
  return result;
});

/** Prévia dos recursos derivados, espelhando a fórmula de character_model.py. */
const resourcePreview = computed(() =>
  (system.value?.resources ?? []).map((resource) => {
    const base = selectedClass.value?.resource_bases?.[resource.key] ?? 0;
    const raceBonus = selectedRace.value?.resource_bonuses?.[resource.key] ?? 0;
    const governed = resource.governing_attribute
      ? effectiveAttributes.value[resource.governing_attribute] ?? 0
      : 0;
    return { ...resource, value: Math.max(base + raceBonus + governed, 1) };
  }),
);

const availableSkills = computed(() => Object.entries(selectedClass.value?.pericias ?? {}));

/** Cada recurso do sistema tem a cor da sua escola (fogo, gelo, myth, ...). */
function resourceDef(key: string) {
  return system.value?.resources.find((resource) => resource.key === key);
}

const resourceTone = (key: string) => resourceDef(key)?.color ?? "gold";
const resourceLabel = (key: string) => resourceDef(key)?.label ?? key;

// O servidor já resolve qual arquivo de arte existe para cada raça.
const racePortrait = computed(() => selectedRace.value?.img_url ?? null);

function adjust(key: string, delta: number) {
  const current = attributes.value[key] ?? 10;
  const next = current + delta;
  if (next < ATTR_MIN || next > ATTR_MAX) return;
  if (delta > 0 && remainingPoints.value <= 0) return;
  attributes.value[key] = next;
}

function toggleIn(list: string[], value: string, max: number) {
  const index = list.indexOf(value);
  if (index >= 0) {
    list.splice(index, 1);
  } else if (list.length < max) {
    list.push(value);
  }
}

const toggleSkill = (skill: string) => toggleIn(chosenSkills.value, skill, MAX_SKILLS);
const toggleAbility = (ability: string) => toggleIn(chosenAbilities.value, ability, MAX_ABILITIES);

function onImage(event: Event) {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0] ?? null;
  imageFile.value = file;
  imagePreview.value = file ? URL.createObjectURL(file) : null;
}

function resetAttributes() {
  const fresh: Record<string, number> = {};
  for (const attr of system.value?.attributes ?? []) fresh[attr.key] = 10;
  attributes.value = fresh;
}

async function loadOptions(id: string) {
  options.value = await api.get<SystemOptions>(`/systems/${id}/options`);
  if (!options.value.classes.some((c) => c._id === classId.value)) {
    classId.value = options.value.classes[0]?._id ?? "";
  }
  if (!options.value.races.some((r) => r._id === raceId.value)) {
    raceId.value = options.value.races[0]?._id ?? "";
  }
}

async function pickSystem(id: string) {
  if (isEdit.value || systemId.value === id) return;
  systemId.value = id;
  chosenSkills.value = [];
  chosenAbilities.value = [];
  await loadOptions(id);
  resetAttributes();
}

async function load() {
  loading.value = true;
  try {
    await systems.ensureLoaded();

    if (isEdit.value) {
      const data = await api.get<{ character: Character }>(`/characters/${props.id}`);
      const character = data.character;
      systemId.value = character.system_id;
      name.value = character.name;
      classId.value = character.class_id ?? "";
      raceId.value = character.race_id ?? "";
      origem.value = character.origem ?? "";
      attributes.value = { ...character.attributes };
      chosenSkills.value = Object.keys(character.pericias ?? {});
      chosenAbilities.value = (character.habilidades ?? []).map((a) => a.name);
      existingImage.value = character.img_url;
      await loadOptions(systemId.value);
    } else {
      systemId.value = systems.systems[0]?.id ?? "medieval";
      await loadOptions(systemId.value);
      resetAttributes();
    }
  } catch {
    error.value = "Não foi possível carregar os dados do personagem.";
  } finally {
    loading.value = false;
  }
}

watch(classId, () => {
  // Perícias vêm da classe: ao trocar de classe, mantém só as ainda válidas.
  const valid = new Set(Object.keys(selectedClass.value?.pericias ?? {}));
  chosenSkills.value = chosenSkills.value.filter((skill) => valid.has(skill));
});

async function submit() {
  error.value = null;
  if (!name.value.trim()) {
    error.value = "Dê um nome ao personagem.";
    return;
  }
  if (!classId.value) {
    error.value = `Escolha ${system.value?.class_label ?? "uma classe"}.`;
    return;
  }

  const form = new FormData();
  form.set("system_id", systemId.value);
  form.set("name", name.value.trim());
  form.set("class_id", classId.value);
  if (system.value?.uses_race && raceId.value) form.set("race_id", raceId.value);
  form.set("origem", origem.value);
  form.set("attributes", JSON.stringify(attributes.value));
  form.set("pericias", JSON.stringify(chosenSkills.value));
  form.set("habilidades", JSON.stringify(chosenAbilities.value));
  if (imageFile.value) form.set("image", imageFile.value);

  saving.value = true;
  try {
    if (isEdit.value) {
      await api.postForm(`/characters/${props.id}`, form);
    } else {
      await api.postForm("/characters", form);
    }
    router.push({ name: "characters" });
  } catch (err) {
    error.value = err instanceof ApiError ? err.message : "Não foi possível salvar.";
  } finally {
    saving.value = false;
  }
}

onMounted(load);
</script>

<template>
  <main class="page">
    <h1 class="text-center">{{ isEdit ? "Editar Personagem" : "Forjar Personagem" }}</h1>

    <NoticeBar v-if="error" kind="error">{{ error }}</NoticeBar>
    <p v-if="loading" class="text-center muted-on-dark">Preparando o ritual…</p>

    <form v-else @submit.prevent="submit">
      <GlyphPanel v-if="!isEdit" title="Sistema de Jogo" icon="🌌" tone="storm">
        <div class="systems">
          <button
            v-for="option in systems.systems"
            :key="option.id"
            type="button"
            class="system-card"
            :class="[`tone-${option.tone}`, { active: option.id === systemId }]"
            @click="pickSystem(option.id)"
          >
            <span class="system-icon">{{ option.icon }}</span>
            <strong>{{ option.name }}</strong>
            <small>{{ option.tagline }}</small>
          </button>
        </div>
      </GlyphPanel>

      <GlyphPanel :title="system?.name ?? 'Identidade'" :icon="system?.icon" :tone="system?.tone">
        <div class="split">
          <div class="stack grow">
            <div>
              <label for="name">Nome do Personagem</label>
              <input id="name" v-model="name" required />
            </div>

            <div v-if="system?.uses_race">
              <label for="race">{{ system.race_label }}</label>
              <select id="race" v-model="raceId">
                <option v-for="race in options.races" :key="race._id" :value="race._id">
                  {{ race.name }}
                </option>
              </select>
              <p v-if="selectedRace?.resumo" class="muted lore">{{ selectedRace.resumo }}</p>
            </div>

            <div>
              <label for="class">{{ system?.class_label }}</label>
              <select id="class" v-model="classId">
                <option v-for="option in options.classes" :key="option._id" :value="option._id">
                  {{ option.name }}
                </option>
              </select>
            </div>
          </div>

          <div v-if="system?.uses_race && racePortrait" class="race-art">
            <img
              :src="racePortrait"
              :alt="selectedRace?.name"
              @error="($event.target as HTMLImageElement).src = '/static/images/races/default.png'"
            />
            <SchoolBadge :tone="system?.tone">{{ selectedRace?.name }}</SchoolBadge>
          </div>
        </div>
      </GlyphPanel>

      <GlyphPanel title="Atributos" icon="⚖️" tone="myth">
        <template v-if="isEdit">
          <p class="muted">
            Atributos são definidos na criação e permanecem fixos — eles já incluem os bônus de
            origem.
          </p>
          <div class="attr-readonly">
            <div v-for="attr in system?.attributes ?? []" :key="attr.key">
              <span>{{ attr.label }}</span>
              <strong>{{ attributes[attr.key] ?? 0 }}</strong>
            </div>
          </div>
        </template>

        <template v-else>
          <p class="points" :class="{ spent: remainingPoints === 0 }">
            Pontos restantes: <strong>{{ remainingPoints }}</strong>
          </p>
          <div class="attr-grid">
            <div v-for="attr in system?.attributes ?? []" :key="attr.key" class="attr-row">
              <label :for="`attr-${attr.key}`">{{ attr.label }}</label>
              <div class="stepper">
                <button
                  type="button"
                  :disabled="(attributes[attr.key] ?? 10) <= ATTR_MIN"
                  @click="adjust(attr.key, -1)"
                >
                  −
                </button>
                <output :id="`attr-${attr.key}`">{{ attributes[attr.key] ?? 10 }}</output>
                <button
                  type="button"
                  :disabled="remainingPoints <= 0 || (attributes[attr.key] ?? 10) >= ATTR_MAX"
                  @click="adjust(attr.key, 1)"
                >
                  +
                </button>
              </div>
              <span v-if="selectedRace?.attribute_bonuses?.[attr.key]" class="bonus">
                {{ selectedRace.attribute_bonuses[attr.key] > 0 ? "+" : ""
                }}{{ selectedRace.attribute_bonuses[attr.key] }} de origem
              </span>
            </div>
          </div>

          <div class="preview">
            <h3>Recursos estimados</h3>
            <div class="row">
              <SchoolBadge
                v-for="resource in resourcePreview"
                :key="resource.key"
                :tone="resource.color"
              >
                {{ resource.label }}: {{ resource.value }}
              </SchoolBadge>
            </div>
          </div>
        </template>
      </GlyphPanel>

      <GlyphPanel
        :title="`${system?.skill_label ?? 'Perícias'} (até ${MAX_SKILLS})`"
        icon="🎯"
        tone="life"
      >
        <p v-if="!availableSkills.length" class="muted">
          Escolha {{ system?.class_label?.toLowerCase() }} para ver as perícias disponíveis.
        </p>
        <div class="chips">
          <button
            v-for="[skill, governing] in availableSkills"
            :key="skill"
            type="button"
            class="chip"
            :class="{ on: chosenSkills.includes(skill) }"
            :disabled="!chosenSkills.includes(skill) && chosenSkills.length >= MAX_SKILLS"
            @click="toggleSkill(skill)"
          >
            <strong>{{ skill }}</strong>
            <small>{{ governing }}</small>
          </button>
        </div>
      </GlyphPanel>

      <GlyphPanel
        :title="`${system?.ability_label ?? 'Habilidades'} (até ${MAX_ABILITIES})`"
        icon="✨"
        tone="ice"
      >
        <div class="ability-list">
          <button
            v-for="ability in options.abilities"
            :key="ability.id"
            type="button"
            class="ability"
            :class="{ on: chosenAbilities.includes(ability.name) }"
            :disabled="
              !chosenAbilities.includes(ability.name) && chosenAbilities.length >= MAX_ABILITIES
            "
            @click="toggleAbility(ability.name)"
          >
            <span class="ability-head">
              <strong>{{ ability.name }}</strong>
              <SchoolBadge
                v-for="(amount, key) in ability.cost"
                :key="key"
                :tone="resourceTone(String(key))"
              >
                {{ resourceLabel(String(key)) }} {{ amount }}
              </SchoolBadge>
            </span>
            <small>{{ ability.description }}</small>
          </button>
        </div>
      </GlyphPanel>

      <GlyphPanel :title="system?.history_label ?? 'História'" icon="📖" tone="balance">
        <label for="origem">Conte de onde vem este personagem</label>
        <textarea id="origem" v-model="origem" rows="4" />

        <label for="image" style="margin-top: 10px">Retrato</label>
        <div class="row">
          <CharacterPortrait :src="imagePreview ?? existingImage" size="md" />
          <input id="image" type="file" accept="image/*" class="grow" @change="onImage" />
        </div>
      </GlyphPanel>

      <div class="row row-center">
        <RuneButton tone="ice" size="lg" @click="$router.push({ name: 'characters' })">
          Voltar
        </RuneButton>
        <RuneButton :tone="system?.tone ?? 'gold'" size="lg" type="submit" :disabled="saving">
          {{ saving ? "Selando…" : isEdit ? "💾 Salvar" : "✨ Criar Personagem" }}
        </RuneButton>
      </div>
    </form>
  </main>
</template>

<style scoped>
.systems {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 12px;
}

.system-card {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 14px;
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
  box-shadow: 0 0 0 3px var(--tone-deep), 0 0 0 6px var(--tone), 0 0 20px var(--tone), var(--lift-1);
}

.system-icon {
  font-size: 1.9rem;
}

.system-card small {
  color: var(--ink-500);
  line-height: 1.3;
}

.split {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.race-art {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: 200px;
}

.race-art img {
  width: 100%;
  border-radius: var(--radius-md);
  box-shadow: 0 0 0 3px var(--gold-600), 0 0 0 6px var(--gold-300), var(--lift-1);
}

.lore {
  margin-top: 6px;
  line-height: 1.4;
}

.points {
  font-weight: 700;
  color: var(--ink-700);
}

.points.spent strong {
  color: var(--school-fire-deep);
}

.attr-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 12px;
}

.attr-row label {
  margin-bottom: 4px;
}

.stepper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stepper button {
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  border: none;
  border-radius: 50%;
  font-size: 1.2rem;
  font-weight: 800;
  cursor: pointer;
  color: #fff;
  background: linear-gradient(180deg, var(--gold-300), var(--gold-500));
  box-shadow: 0 0 0 2px var(--gold-700), 0 3px 0 var(--gold-700);
}

.stepper button:disabled {
  filter: grayscale(0.7);
  cursor: not-allowed;
}

.stepper output {
  flex: 1;
  text-align: center;
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--ink-900);
  background: #fffdf8;
  border-radius: var(--radius-sm);
  padding: 5px 0;
  box-shadow: inset 0 0 0 2px var(--scroll-300);
}

.bonus {
  display: block;
  margin-top: 4px;
  font-size: 0.72rem;
  color: var(--school-life-deep);
  font-weight: 700;
}

.attr-readonly {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
}

.attr-readonly div {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  background: rgba(58, 36, 16, 0.07);
}

.preview {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 2px dashed var(--scroll-300);
}

.preview h3 {
  color: var(--ink-700);
  margin-bottom: 8px;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chip {
  display: flex;
  flex-direction: column;
  padding: 9px 14px;
  border: none;
  border-radius: var(--radius-pill);
  background: #fffdf8;
  box-shadow: inset 0 0 0 2px var(--scroll-300);
  cursor: pointer;
  font-family: var(--font-ui);
  color: var(--ink-900);
}

.chip small {
  color: var(--ink-500);
  font-size: 0.72rem;
}

.chip.on {
  background: linear-gradient(180deg, var(--school-life), var(--school-life-deep));
  color: #fff;
  box-shadow: 0 0 0 2px var(--school-life-deep), 0 3px 0 var(--school-life-deep);
}

.chip.on small {
  color: rgba(255, 255, 255, 0.85);
}

.chip:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.ability-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 10px;
  max-height: 340px;
  overflow-y: auto;
  padding-right: 4px;
}

.ability {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 11px 14px;
  border: none;
  border-radius: var(--radius-md);
  background: #fffdf8;
  box-shadow: inset 0 0 0 2px var(--scroll-300);
  cursor: pointer;
  text-align: left;
  font-family: var(--font-ui);
  color: var(--ink-900);
}

.ability-head {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.ability small {
  color: var(--ink-500);
  line-height: 1.35;
}

.ability.on {
  background: linear-gradient(170deg, #e8f7fd, #cfeefb);
  box-shadow: 0 0 0 3px var(--school-ice-deep), 0 3px 0 var(--school-ice-deep);
}

.ability:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

@media (max-width: 720px) {
  .race-art {
    width: 100%;
  }
}
</style>
