<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import AppNav from "@/components/AppNav.vue";
import ArcaneBackdrop from "@/components/ArcaneBackdrop.vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const route = useRoute();

const showNav = computed(() => Boolean(auth.user) && route.name !== "login" && route.name !== "register");
</script>

<template>
  <ArcaneBackdrop />
  <AppNav v-if="showNav" />
  <RouterView v-slot="{ Component }">
    <Transition name="page" mode="out-in">
      <component :is="Component" />
    </Transition>
  </RouterView>
</template>

<style>
.page-enter-active,
.page-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
