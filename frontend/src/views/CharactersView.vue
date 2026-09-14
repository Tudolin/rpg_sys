<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import GlyphPanel from "@/components/GlyphPanel.vue";
import RuneButton from "@/components/RuneButton.vue";
import CharacterPortrait from "@/components/CharacterPortrait.vue";
import SchoolBadge from "@/components/SchoolBadge.vue";
import ResourceOrb from "@/components/ResourceOrb.vue";
import NoticeBar from "@/components/NoticeBar.vue";
import ModalDialog from "@/components/ModalDialog.vue";
import { api } from "@/services/api";
import { useSystemsStore } from "@/stores/systems";
import type { Character } from "@/types";

const systems = useSystemsStore();
const characters = ref<Character[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const pendingDelete = ref<Character | null>(null);

const hasCharacters = computed(() => characters.value.length > 0);

async function load() {
  loading.value = true;
  try {
    await systems.ensureLoaded();
    const data = await api.get<{ characters: Character[] }>("/characters");
    characters.value = data.characters;
  } catch {
    error.value = "Não foi possível carregar seus personagens.";
  } finally {
    loading.value = false;
  }
}

function openPdf(characterId: string) {
  window.open(`/api/characters/${characterId}/pdf`, "_blank");
}

async function confirmDelete() {
  const target = pendingDelete.value;
  if (!target) return;
  pendingDelete.value = null;
  await api.delete(`/characters/${target._id}`);
  characters.value = characters.value.filter((c) => c._id !== target._id);
}

onMounted(load);
</script>

<template>
  <main class="page">
    <h1 class="text-center">Seus Personagens</h1>
    <p class="text-center muted-on-dark">
      Cada personagem pertence a um sistema e só entra em mesas daquele sistema.
    </p>

    <NoticeBar v-if="error" kind="error">{{ error }}</NoticeBar>

    <p v-if="loading" class="text-center muted-on-dark">Consultando o grimório…</p>

    <div v-else-if="hasCharacters" class="grid">
      <GlyphPanel
        v-for="character in characters"
        :key="character._id"
        :tone="systems.get(character.system_id)?.tone ?? 'gold'"
      >
        <div class="head">
          <CharacterPortrait
            :src="character.img_url"
            :alt="character.name"
            size="md"
            :tone="systems.get(character.system_id)?.tone ?? 'gold'"
          />
          <div class="ident">
            <h3>{{ character.name }}</h3>
            <div class="row">
              <SchoolBadge
                :tone="systems.get(character.system_id)?.tone ?? 'gold'"
                :icon="systems.get(character.system_id)?.icon"
              >
                {{ systems.get(character.system_id)?.name ?? character.system_id }}
              </SchoolBadge>
              <SchoolBadge tone="balance">{{ character.class_name }}</SchoolBadge>
              <SchoolBadge v-if="character.race_name" tone="life">
                {{ character.race_name }}
              </SchoolBadge>
            </div>
          </div>
        </div>

        <div class="orbs">
          <ResourceOrb
            v-for="resource in systems.get(character.system_id)?.resources ?? []"
            :key="resource.key"
            size="sm"
            :tone="resource.color"
            :label="resource.label"
            :current="character.resources[resource.key]?.current ?? 0"
            :max="character.resources[resource.key]?.max ?? 0"
          />
        </div>

        <dl class="attrs">
          <div v-for="attr in systems.get(character.system_id)?.attributes ?? []" :key="attr.key">
            <dt>{{ attr.abbr }}</dt>
            <dd>{{ character.attributes[attr.key] ?? 0 }}</dd>
          </div>
        </dl>

        <div class="row actions">
          <RuneButton
            tone="ice"
            size="sm"
            @click="$router.push({ name: 'character-edit', params: { id: character._id } })"
          >
            ✏️ Editar
          </RuneButton>
          <RuneButton tone="balance" size="sm" @click="openPdf(character._id)">
            📄 Ficha PDF
          </RuneButton>
          <RuneButton tone="fire" size="sm" @click="pendingDelete = character">
            🗑️ Excluir
          </RuneButton>
        </div>
      </GlyphPanel>
    </div>

    <GlyphPanel v-else dark tone="myth">
      <p class="text-center" style="margin: 0">
        Nenhum personagem ainda. Crie o primeiro herói da sua party!
      </p>
    </GlyphPanel>

    <div class="row row-center" style="margin-top: 10px">
      <RuneButton tone="myth" size="lg" @click="$router.push({ name: 'character-new' })">
        ✨ Criar Personagem
      </RuneButton>
      <RuneButton tone="storm" size="lg" @click="$router.push({ name: 'sessions' })">
        🎲 Ver Mesas
      </RuneButton>
    </div>

    <ModalDialog
      v-if="pendingDelete"
      title="Excluir personagem?"
      @close="pendingDelete = null"
    >
      <p>
        <strong>{{ pendingDelete.name }}</strong> será apagado permanentemente. Essa ação não
        pode ser desfeita.
      </p>
      <template #footer>
        <RuneButton tone="ice" size="sm" @click="pendingDelete = null">Cancelar</RuneButton>
        <RuneButton tone="fire" size="sm" @click="confirmDelete">Excluir</RuneButton>
      </template>
    </ModalDialog>
  </main>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
  gap: 22px;
  margin-bottom: 8px;
}

.head {
  display: flex;
  gap: 14px;
  align-items: center;
  margin-bottom: 14px;
}

.ident h3 {
  margin: 0 0 6px;
  color: var(--gold-700);
  font-size: 1.35rem;
}

.orbs {
  display: flex;
  gap: 12px;
  justify-content: center;
  padding: 12px;
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, var(--void-700), var(--void-800));
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.45), 0 0 0 2px var(--gold-600);
  margin-bottom: 14px;
}

.attrs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(56px, 1fr));
  gap: 6px;
  margin: 0 0 14px;
}

.attrs div {
  text-align: center;
  padding: 6px 2px;
  border-radius: var(--radius-sm);
  background: rgba(58, 36, 16, 0.08);
  box-shadow: inset 0 0 0 1px var(--scroll-300);
}

.attrs dt {
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  color: var(--ink-500);
}

.attrs dd {
  margin: 2px 0 0;
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--ink-900);
}

.actions {
  justify-content: center;
}
</style>
