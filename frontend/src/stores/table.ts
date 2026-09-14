import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { getSocket } from "@/services/socket";
import type { Character, Monster, SessionSnapshot } from "@/types";

/**
 * Estado ao vivo de uma mesa (sessão de jogo).
 *
 * Toda mutação chega pelo Socket.IO e é aplicada aqui; as telas apenas
 * renderizam este estado. Isso substitui a manipulação manual de DOM da
 * versão antiga, que era a origem da maior parte dos bugs de sincronismo
 * (listeners duplicados, cards renderizados duas vezes, etc).
 */
export const useTableStore = defineStore("table", () => {
  const sessionId = ref<string | null>(null);
  const characters = ref<Character[]>([]);
  const monsters = ref<Monster[]>([]);
  const connected = ref(false);
  const errorMessage = ref<string | null>(null);

  const mediaOverlay = ref<{ url: string; displayTime: number | null } | null>(null);
  const currentTrack = ref<string | null>(null);

  let bound = false;
  let mediaTimer: number | undefined;

  function characterById(id: string) {
    return characters.value.find((c) => c._id === id) ?? null;
  }

  const monsterCount = computed(() => monsters.value.length);

  function applySnapshot(snapshot: SessionSnapshot) {
    characters.value = snapshot.characters ?? [];
    monsters.value = snapshot.monsters ?? [];
  }

  function bindSocket() {
    if (bound) return;
    const socket = getSocket();

    socket.on("connect", () => {
      connected.value = true;
      if (sessionId.value) {
        socket.emit("join_session_room", { session_id: sessionId.value });
      }
    });

    socket.on("disconnect", () => {
      connected.value = false;
    });

    socket.on("session_sync", applySnapshot);

    socket.on("resources_updated", ({ character_id, resources }) => {
      const character = characterById(character_id);
      if (character) character.resources = resources;
    });

    socket.on("monster_added", (monster) => {
      if (monsters.value.some((m) => m._id === monster._id)) return;
      monsters.value.push(monster);
      if (monster.spawn_som) {
        const audio = new Audio(`/static/spawn/${monster.spawn_som}`);
        audio.play().catch(() => {
          /* navegadores bloqueiam áudio sem interação — tudo bem */
        });
      }
    });

    socket.on("monster_stats_updated", (data) => {
      const monster = monsters.value.find((m) => m._id === data.monster_id);
      if (!monster) return;
      monster.current_hp = data.current_hp;
      monster.current_mana = data.current_mana;
      monster.current_energia = data.current_energia;
    });

    socket.on("monster_removed", ({ monster_id }) => {
      monsters.value = monsters.value.filter((m) => m._id !== monster_id);
    });

    socket.on("new_media", ({ media_url, display_time }) => {
      window.clearTimeout(mediaTimer);
      mediaOverlay.value = { url: media_url, displayTime: display_time };
      if (display_time && display_time > 0) {
        mediaTimer = window.setTimeout(() => {
          mediaOverlay.value = null;
        }, display_time * 1000);
      }
    });

    socket.on("play_music", ({ track_url }) => {
      currentTrack.value = track_url;
    });

    socket.on("stop_music", () => {
      currentTrack.value = null;
    });

    socket.on("session_error", ({ message }) => {
      errorMessage.value = message;
    });

    // Celular que voltou do background pode ter perdido eventos: pede um
    // retrato completo assim que a aba fica visível de novo.
    document.addEventListener("visibilitychange", () => {
      if (!document.hidden && sessionId.value) {
        socket.emit("request_session_sync", { session_id: sessionId.value });
      }
    });

    bound = true;
  }

  function joinTable(id: string) {
    bindSocket();
    sessionId.value = id;
    errorMessage.value = null;
    const socket = getSocket();
    if (socket.connected) {
      socket.emit("join_session_room", { session_id: id });
    }
  }

  function leaveTable() {
    sessionId.value = null;
    characters.value = [];
    monsters.value = [];
    mediaOverlay.value = null;
    window.clearTimeout(mediaTimer);
  }

  function updateCharacterResources(characterId: string, resources: Record<string, number>) {
    getSocket().emit("update_character_status", {
      character_id: characterId,
      resources,
    });
  }

  function updateMonsterStats(
    monsterId: string,
    stats: { hp?: number; mana?: number; energia?: number },
  ) {
    if (!sessionId.value) return;
    getSocket().emit("update_monster_stats", {
      session_id: sessionId.value,
      monster_id: monsterId,
      ...stats,
    });
  }

  function removeMonster(monsterId: string) {
    if (!sessionId.value) return;
    getSocket().emit("remove_monster", {
      session_id: sessionId.value,
      monster_id: monsterId,
    });
  }

  function dismissMedia() {
    window.clearTimeout(mediaTimer);
    mediaOverlay.value = null;
  }

  return {
    sessionId,
    characters,
    monsters,
    connected,
    errorMessage,
    mediaOverlay,
    currentTrack,
    monsterCount,
    characterById,
    joinTable,
    leaveTable,
    updateCharacterResources,
    updateMonsterStats,
    removeMonster,
    dismissMedia,
  };
});
