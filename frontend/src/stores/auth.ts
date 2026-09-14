import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/services/api";
import type { User } from "@/types";

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null);
  const ready = ref(false);

  async function fetchMe() {
    const data = await api.get<{ user: User | null }>("/auth/me");
    user.value = data.user;
    ready.value = true;
    return user.value;
  }

  async function login(username: string, password: string) {
    const data = await api.post<{ user: User }>("/auth/login", { username, password });
    user.value = data.user;
    return data.user;
  }

  async function register(username: string, password: string) {
    const data = await api.post<{ user: User }>("/auth/register", { username, password });
    user.value = data.user;
    return data.user;
  }

  async function logout() {
    await api.post("/auth/logout");
    user.value = null;
  }

  return { user, ready, fetchMe, login, register, logout };
});
