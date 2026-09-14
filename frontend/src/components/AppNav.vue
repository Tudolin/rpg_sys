<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { disconnectSocket } from "@/services/socket";

const auth = useAuthStore();
const router = useRouter();
const open = ref(false);

async function handleLogout() {
  await auth.logout();
  disconnectSocket();
  open.value = false;
  router.push({ name: "login" });
}
</script>

<template>
  <nav class="nav">
    <RouterLink class="brand" :to="{ name: 'characters' }" @click="open = false">
      <img src="/static/logo.png" alt="" />
      <span class="brand-text">RPG&nbsp;Sys</span>
    </RouterLink>

    <button
      v-if="auth.user"
      class="burger"
      type="button"
      :aria-expanded="open"
      aria-label="Menu"
      @click="open = !open"
    >
      <span /><span /><span />
    </button>

    <div v-if="auth.user" class="links" :class="{ open }">
      <RouterLink :to="{ name: 'characters' }" @click="open = false">🧙 Personagens</RouterLink>
      <RouterLink :to="{ name: 'sessions' }" @click="open = false">🎲 Mesas</RouterLink>
      <span class="who">{{ auth.user.username }}</span>
      <button class="logout" type="button" @click="handleLogout">Sair</button>
    </div>
  </nav>
</template>

<style scoped>
.nav {
  position: sticky;
  top: 0;
  z-index: 60;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  padding: 10px 20px;
  background: linear-gradient(180deg, rgba(50, 38, 110, 0.97), rgba(25, 17, 58, 0.97));
  border-bottom: 3px solid var(--gold-500);
  box-shadow: 0 6px 20px rgba(10, 6, 25, 0.55);
  backdrop-filter: blur(8px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.brand img {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--void-900);
  box-shadow: 0 0 0 2px var(--gold-600), 0 0 0 4px var(--gold-300), 0 0 14px rgba(240, 181, 55, 0.5);
}

.brand-text {
  font-family: var(--font-display);
  font-size: 1.5rem;
  color: var(--gold-200);
  text-shadow: 0 2px 0 var(--gold-700), 0 0 14px rgba(240, 181, 55, 0.4);
}

.links {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.links a {
  padding: 8px 16px;
  border-radius: var(--radius-pill);
  color: var(--ink-onDark);
  font-weight: 600;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.07);
  transition: background 0.15s ease, transform 0.15s ease;
}

.links a:hover {
  background: rgba(240, 181, 55, 0.22);
  transform: translateY(-1px);
  text-decoration: none;
}

.links a.router-link-active {
  background: linear-gradient(180deg, var(--gold-300), var(--gold-500));
  color: var(--ink-900);
  box-shadow: 0 0 0 2px var(--gold-700), 0 3px 0 var(--gold-700);
}

.who {
  color: var(--ink-onDark-muted);
  font-size: 0.85rem;
  padding-left: 6px;
}

.logout {
  padding: 7px 14px;
  border: none;
  border-radius: var(--radius-pill);
  background: linear-gradient(180deg, color-mix(in srgb, var(--school-fire) 80%, #fff), var(--school-fire));
  color: #fff;
  font-family: var(--font-ui);
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 0 0 2px var(--school-fire-deep), 0 3px 0 var(--school-fire-deep);
}

.logout:hover {
  filter: brightness(1.08);
}

.burger {
  display: none;
  flex-direction: column;
  gap: 4px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.08);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.burger span {
  display: block;
  width: 22px;
  height: 3px;
  border-radius: 2px;
  background: var(--gold-200);
}

@media (max-width: 720px) {
  .burger {
    display: flex;
  }

  .links {
    display: none;
    width: 100%;
    flex-direction: column;
    align-items: stretch;
  }

  .links.open {
    display: flex;
  }

  .links a,
  .logout {
    text-align: center;
  }
}
</style>
