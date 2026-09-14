import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/LoginView.vue"),
      meta: { public: true },
    },
    {
      path: "/registrar",
      name: "register",
      component: () => import("@/views/RegisterView.vue"),
      meta: { public: true },
    },
    { path: "/", name: "characters", component: () => import("@/views/CharactersView.vue") },
    {
      path: "/personagens/novo",
      name: "character-new",
      component: () => import("@/views/CharacterFormView.vue"),
    },
    {
      path: "/personagens/:id/editar",
      name: "character-edit",
      component: () => import("@/views/CharacterFormView.vue"),
      props: true,
    },
    { path: "/mesas", name: "sessions", component: () => import("@/views/SessionsView.vue") },
    {
      path: "/mesas/:id/entrar",
      name: "join",
      component: () => import("@/views/JoinSessionView.vue"),
      props: true,
    },
    {
      path: "/mesas/:id/jogar",
      name: "lobby",
      component: () => import("@/views/GameLobbyView.vue"),
      props: true,
    },
    {
      path: "/mesas/:id/mestre",
      name: "master",
      component: () => import("@/views/MasterControlView.vue"),
      props: true,
    },
    { path: "/:pathMatch(.*)*", redirect: { name: "characters" } },
  ],
  scrollBehavior: () => ({ top: 0 }),
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();

  if (!auth.ready) {
    try {
      await auth.fetchMe();
    } catch {
      auth.ready = true;
    }
  }

  if (!to.meta.public && !auth.user) {
    return { name: "login", query: to.name === "characters" ? {} : { next: to.fullPath } };
  }

  if (to.meta.public && auth.user) {
    return { name: "characters" };
  }

  return true;
});

export default router;
