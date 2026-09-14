/**
 * Shared realtime connection helper for game_lobby.html and master_control.html.
 *
 * The previous version hardcoded `io.connect('wss://familyrpg.servebeer.com', ...)`
 * in both page scripts, which only ever worked on that one domain. Calling
 * `io()` with no URL connects back to whatever origin served the page, so
 * this works unmodified on localhost, a self-hosted Debian box, or behind
 * any reverse proxy.
 */
function createSessionSocket() {
  const socket = io({
    transports: ["websocket", "polling"],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
  });

  const sessionId = window.GAME && window.GAME.sessionId;

  function joinRoom() {
    if (sessionId) {
      socket.emit("join_session_room", { session_id: sessionId });
    }
  }

  socket.on("connect", joinRoom);

  // A phone that was backgrounded (or a laptop that slept) may keep its
  // socket "connected" while missing events that fired while it was away.
  // Ask for a fresh snapshot whenever the tab becomes visible again.
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden && sessionId) {
      socket.emit("request_session_sync", { session_id: sessionId });
    }
  });

  socket.on("session_error", (data) => {
    console.error("Session error:", data && data.message);
  });

  return socket;
}

/** Updates one resource orb (HP/Mana/Energy/Sanity/... — whatever the active
 * game system defines) in place, given its current/max values. */
function updateResourceOrb(characterId, resourceKey, current, max) {
  const orb = document.querySelector(
    `.resource-orb[data-character-id="${characterId}"][data-resource-key="${resourceKey}"]`
  );
  if (!orb) return;

  const fill = orb.querySelector(".resource-fill");
  const text = orb.querySelector(".resource-text");
  const safeMax = Number(max) || Number(orb.dataset.max) || 1;
  const pct = Math.max(0, Math.min(100, (Number(current) / safeMax) * 100));

  if (fill) fill.style.height = pct + "%";
  if (text) text.textContent = `${current} / ${safeMax}`;
  orb.dataset.max = safeMax;
}

function applyResourceUpdate(characterId, resources) {
  Object.entries(resources || {}).forEach(([key, value]) => {
    updateResourceOrb(characterId, key, value.current, value.max);
  });
}
