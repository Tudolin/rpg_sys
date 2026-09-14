import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { api } from "@/services/api";
import type { GameSystem } from "@/types";

/** Catálogo de sistemas de RPG — carregado uma vez e reaproveitado. */
export const useSystemsStore = defineStore("systems", () => {
  const systems = ref<GameSystem[]>([]);
  const loaded = ref(false);
  let inflight: Promise<GameSystem[]> | null = null;

  const byId = computed(() => {
    const map = new Map<string, GameSystem>();
    systems.value.forEach((system) => map.set(system.id, system));
    return map;
  });

  async function ensureLoaded() {
    if (loaded.value) return systems.value;
    if (!inflight) {
      inflight = api
        .get<{ systems: GameSystem[] }>("/systems")
        .then((data) => {
          systems.value = data.systems;
          loaded.value = true;
          return systems.value;
        })
        .finally(() => {
          inflight = null;
        });
    }
    return inflight;
  }

  function get(id: string | null | undefined): GameSystem | undefined {
    if (!id) return undefined;
    return byId.value.get(id);
  }

  return { systems, loaded, byId, ensureLoaded, get };
});
