/** Contratos compartilhados com a API Flask (ver api.py / game_systems.py). */

export type SchoolTone =
  | "fire"
  | "ice"
  | "storm"
  | "myth"
  | "life"
  | "death"
  | "balance"
  | "gold";

export interface AttributeDef {
  key: string;
  label: string;
  abbr: string;
}

export interface ResourceDef {
  key: string;
  label: string;
  color: SchoolTone;
  governing_attribute: string | null;
}

export interface CombatStatDef {
  key: string;
  label: string;
  governing_attribute: string | null;
}

export interface GameSystem {
  id: string;
  name: string;
  tagline: string;
  icon: string;
  theme: string;
  tone: SchoolTone;
  uses_class: boolean;
  class_label: string;
  uses_race: boolean;
  race_label: string | null;
  attributes: AttributeDef[];
  resources: ResourceDef[];
  combat_stats: CombatStatDef[];
  skill_label: string;
  ability_label: string;
  history_label: string;
}

export interface ResourceValue {
  max: number;
  current: number;
}

export interface Ability {
  id: string;
  name: string;
  description: string;
  cost: Record<string, number>;
  icon?: string | null;
}

export interface Character {
  _id: string;
  name: string;
  system_id: string;
  class_id: string | null;
  race_id: string | null;
  class_name: string;
  race_name: string | null;
  img_url: string;
  attributes: Record<string, number>;
  resources: Record<string, ResourceValue>;
  combat_stats: Record<string, number>;
  habilidades: Ability[];
  pericias: Record<string, number>;
  origem: string;
}

export interface Monster {
  _id: string;
  name: string;
  img_url: string;
  resumo: string;
  hp: number;
  current_hp: number;
  mana: number;
  current_mana: number;
  energia: number;
  current_energia: number;
  spawn_som?: string;
}

export interface GameSessionSummary {
  _id: string;
  name: string;
  system_id: string;
  creator_name: string;
  is_master: boolean;
  player_count: number;
}

export interface SessionSnapshot {
  session_id: string;
  characters: Character[];
  monsters: Monster[];
}

export interface ClassOption {
  _id: string;
  name: string;
  resource_bases: Record<string, number>;
  combat_bases: Record<string, number>;
  pericias: Record<string, string>;
  habilidades_classe: Record<string, string>;
}

export interface RaceOption {
  _id: string;
  name: string;
  resumo: string;
  img_url: string;
  attribute_bonuses: Record<string, number>;
  resource_bonuses: Record<string, number>;
  habilidades_inatas: Record<string, string>;
}

export interface SystemOptions {
  classes: ClassOption[];
  races: RaceOption[];
  abilities: Ability[];
}

export interface EnemyOption {
  _id: string;
  name: string;
  hp: number;
  resumo: string;
}

export interface MusicTrack {
  name: string;
  url: string;
}

export interface User {
  id: string;
  username: string;
}
