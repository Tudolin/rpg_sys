import { io, type Socket } from "socket.io-client";
import type { Character, Monster, SessionSnapshot } from "@/types";

/** Eventos que o servidor envia para o cliente. */
interface ServerToClient {
  session_sync: (snapshot: SessionSnapshot) => void;
  resources_updated: (data: {
    character_id: string;
    resources: Character["resources"];
  }) => void;
  monster_added: (monster: Monster) => void;
  monster_stats_updated: (data: {
    monster_id: string;
    current_hp: number;
    hp: number;
    current_mana: number;
    current_energia: number;
  }) => void;
  monster_removed: (data: { monster_id: string }) => void;
  play_music: (data: { track_url: string }) => void;
  stop_music: () => void;
  new_media: (data: { media_url: string; display_time: number | null }) => void;
  session_error: (data: { message: string }) => void;
}

/** Eventos que o cliente envia para o servidor. */
interface ClientToServer {
  join_session_room: (data: { session_id: string }) => void;
  request_session_sync: (data: { session_id: string }) => void;
  update_character_status: (data: {
    character_id: string;
    resources: Record<string, number>;
  }) => void;
  update_monster_stats: (data: {
    session_id: string;
    monster_id: string;
    hp?: number;
    mana?: number;
    energia?: number;
  }) => void;
  remove_monster: (data: { session_id: string; monster_id: string }) => void;
}

export type GameSocket = Socket<ServerToClient, ClientToServer>;

let socket: GameSocket | null = null;

/**
 * Conexão única e reaproveitada. Sem URL fixa: o socket.io-client aponta
 * para a mesma origem que serviu a página, então funciona em localhost,
 * no Debian self-hosted e atrás de qualquer proxy reverso.
 */
export function getSocket(): GameSocket {
  if (!socket) {
    socket = io({
      transports: ["websocket", "polling"],
      reconnection: true,
      reconnectionDelay: 800,
      reconnectionDelayMax: 5000,
    });
  }
  return socket;
}

export function disconnectSocket(): void {
  socket?.disconnect();
  socket = null;
}
