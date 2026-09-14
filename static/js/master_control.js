document.addEventListener("DOMContentLoaded", function () {
    const GAME = window.GAME || {};
    const system = GAME.system || { resources: [], attributes: [] };
    const sessionId = GAME.sessionId;
    const staticBaseUrl = GAME.staticBaseUrl || "/static/images/monsters/";

    const socket = createSessionSocket();

    const charactersContainer = document.querySelector(".characters-container");
    const monsterList = document.getElementById("monster-list");
    const addMonsterForm = document.getElementById("add-monster-form");
    const mediaForm = document.getElementById("media-form");
    const musicSelect = document.getElementById("music-select");
    const currentTrackElement = document.getElementById("current-track");
    const audioPlayer = document.getElementById("audio-player");
    const gridContainer = document.querySelector(".grid-container");

    // ---- Characters -------------------------------------------------

    function characterCardHTML(char) {
        const resourceInputs = system.resources.map((res) => {
            const value = (char.resources && char.resources[res.key]) || { current: 0, max: 0 };
            return `<label>${res.label}: <input type="number" data-resource-key="${res.key}" value="${value.current}"> / ${value.max}</label><br>`;
        }).join("");

        return `
            <div class="character-card" data-player-id="${char._id}">
                <p><strong>${char.name}</strong></p>
                <form class="character-form" data-char-id="${char._id}">
                    ${resourceInputs}
                    <button type="submit">Atualizar</button>
                </form>
                <button type="button" class="remove-player-button" data-char-id="${char._id}">Remover jogador</button>
            </div>
        `;
    }

    function renderCharacters(characters) {
        if (!charactersContainer) return;
        charactersContainer.innerHTML = (characters || []).map(characterCardHTML).join("");
    }

    if (charactersContainer) {
        charactersContainer.addEventListener("submit", function (event) {
            const form = event.target.closest(".character-form");
            if (!form) return;
            event.preventDefault();

            const charId = form.getAttribute("data-char-id");
            const resources = {};
            form.querySelectorAll("[data-resource-key]").forEach((input) => {
                resources[input.dataset.resourceKey] = Number(input.value);
            });

            socket.emit("update_character_status", { character_id: charId, resources: resources });
        });

        charactersContainer.addEventListener("click", function (event) {
            const button = event.target.closest(".remove-player-button");
            if (!button) return;

            const charId = button.getAttribute("data-char-id");
            fetch(`/remove_player/${charId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionId }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (!data.success) console.error("Failed to remove player:", data.error);
                })
                .catch((error) => console.error("Error:", error));
        });
    }

    socket.on("resources_updated", function (data) {
        const form = document.querySelector(`.character-form[data-char-id="${data.character_id}"]`);
        if (!form) return;
        Object.entries(data.resources || {}).forEach(([key, value]) => {
            const input = form.querySelector(`[data-resource-key="${key}"]`);
            if (input && document.activeElement !== input) input.value = value.current;
        });
    });

    // ---- Monsters -----------------------------------------------------

    function monsterCardHTML(monster) {
        const imageUrl = staticBaseUrl + monster.img_url;
        return `
            <li class="enemy-card" data-monster-id="${monster._id}" data-max-hp="${monster.hp}">
                <h4>${monster.name}</h4>
                <img src="${imageUrl}" alt="${monster.name}" class="monster-image">
                <form class="monster-form" data-monster-id="${monster._id}">
                    <label>HP: <input type="number" data-monster-field="hp" value="${monster.current_hp}"> / ${monster.hp}</label><br>
                    <label>Mana: <input type="number" data-monster-field="mana" value="${monster.current_mana}"></label><br>
                    <label>Energia: <input type="number" data-monster-field="energia" value="${monster.current_energia}"></label><br>
                    <button type="submit">Atualizar</button>
                </form>
                <p>${monster.resumo || ""}</p>
                <button type="button" class="remove-monster-button" data-monster-id="${monster._id}">Remover</button>
            </li>
        `;
    }

    function renderMonsters(monsters) {
        if (!monsterList) return;
        monsterList.innerHTML = (monsters || []).map(monsterCardHTML).join("");
    }

    if (monsterList) {
        monsterList.addEventListener("submit", function (event) {
            const form = event.target.closest(".monster-form");
            if (!form) return;
            event.preventDefault();

            const monsterId = form.getAttribute("data-monster-id");
            const payload = { session_id: sessionId, monster_id: monsterId };
            form.querySelectorAll("[data-monster-field]").forEach((input) => {
                payload[input.dataset.monsterField] = Number(input.value);
            });

            socket.emit("update_monster_stats", payload);
        });

        monsterList.addEventListener("click", function (event) {
            const button = event.target.closest(".remove-monster-button");
            if (!button) return;
            socket.emit("remove_monster", { monster_id: button.getAttribute("data-monster-id"), session_id: sessionId });
        });
    }

    if (addMonsterForm) {
        addMonsterForm.addEventListener("submit", function (event) {
            event.preventDefault();
            const monsterId = document.getElementById("monster-select").value;
            const quantity = parseInt(document.getElementById("monster-quantity").value, 10);
            if (!monsterId || !quantity || quantity < 1) return;

            fetch("/add_monster_to_session", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionId, monster_id: monsterId, quantity: quantity }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (!data.success) console.error("Error adding monster:", data.message);
                    // DOM updates arrive via the 'monster_added' broadcast below,
                    // so every connected view (including this one) stays in sync
                    // without rendering the new monster twice.
                })
                .catch((error) => console.error("Erro:", error));
        });
    }

    socket.on("monster_added", function (data) {
        if (document.querySelector(`.enemy-card[data-monster-id="${data._id}"]`)) return;
        if (monsterList) monsterList.insertAdjacentHTML("beforeend", monsterCardHTML(data));
    });

    socket.on("monster_stats_updated", function (data) {
        const card = document.querySelector(`.enemy-card[data-monster-id="${data.monster_id}"]`);
        if (!card) return;
        const hpInput = card.querySelector('[data-monster-field="hp"]');
        const manaInput = card.querySelector('[data-monster-field="mana"]');
        const energiaInput = card.querySelector('[data-monster-field="energia"]');
        if (hpInput && document.activeElement !== hpInput) hpInput.value = data.current_hp;
        if (manaInput && document.activeElement !== manaInput) manaInput.value = data.current_mana;
        if (energiaInput && document.activeElement !== energiaInput) energiaInput.value = data.current_energia;
    });

    socket.on("monster_removed", function (data) {
        const card = document.querySelector(`.enemy-card[data-monster-id="${data.monster_id}"]`);
        if (card) card.remove();
    });

    // ---- Full session sync ---------------------------------------------

    socket.on("session_sync", function (data) {
        renderCharacters(data.characters);
        renderMonsters(data.monsters);
    });

    // ---- Media -----------------------------------------------------

    if (mediaForm) {
        mediaForm.addEventListener("submit", function (event) {
            event.preventDefault();
            const fileInput = document.getElementById("media-input");
            if (!fileInput.files.length) {
                console.error("No file selected!");
                return;
            }

            const formData = new FormData(mediaForm);
            formData.append("session_id", sessionId);

            fetch("/upload_media", { method: "POST", body: formData })
                .then((response) => response.json())
                .then((data) => {
                    if (!data.success) console.error("Error uploading media:", data.error);
                })
                .catch((error) => console.error("Error:", error.message));
        });
    }

    // ---- Music -----------------------------------------------------

    function saveMusicState() {
        try {
            localStorage.setItem("musicPlayerState", JSON.stringify({
                trackUrl: audioPlayer.src,
                currentTime: audioPlayer.currentTime,
                playing: !audioPlayer.paused,
            }));
        } catch (e) { /* private browsing / storage disabled: non-fatal */ }
    }

    if (musicSelect) {
        fetch("/music_tracks")
            .then((response) => response.json())
            .then((tracks) => {
                musicSelect.innerHTML = '<option value="">Selecione uma música</option>';
                tracks.forEach((track) => {
                    const option = document.createElement("option");
                    option.value = track.url;
                    option.textContent = track.name;
                    musicSelect.appendChild(option);
                });
            })
            .catch((error) => console.error("Erro ao carregar músicas:", error));
    }

    const playButton = document.getElementById("play-button");
    if (playButton) {
        playButton.addEventListener("click", function () {
            const selectedTrack = musicSelect.value;
            if (!selectedTrack) return;

            fetch("/play_music", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ track_url: selectedTrack, session_id: sessionId }),
            }).catch((error) => console.error("Erro:", error));
        });
    }

    const stopButton = document.getElementById("stop-button");
    if (stopButton) {
        stopButton.addEventListener("click", function () {
            fetch("/stop_music", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionId }),
            }).catch((error) => console.error("Erro:", error));
        });
    }

    if (audioPlayer) {
        socket.on("play_music", function (data) {
            if (audioPlayer.src !== data.track_url) {
                audioPlayer.src = data.track_url;
                audioPlayer.play().catch((error) => console.error("Failed to play music:", error));
                if (currentTrackElement) {
                    currentTrackElement.textContent = `Reproduzindo: ${data.track_url.split("/").pop()}`;
                }
                saveMusicState();
            }
        });

        socket.on("stop_music", function () {
            audioPlayer.pause();
            audioPlayer.src = "";
            if (currentTrackElement) currentTrackElement.textContent = "Nenhuma música em reprodução";
            try { localStorage.removeItem("musicPlayerState"); } catch (e) { /* non-fatal */ }
        });

        window.addEventListener("beforeunload", saveMusicState);
    }

    // ---- Pawns on the tabletop row --------------------------------

    function initializeDragAndDrop() {
        if (!gridContainer) return;
        const pawns = gridContainer.querySelectorAll(".pawn");
        const cells = gridContainer.querySelectorAll("#grid-table td");

        pawns.forEach((pawn) => {
            pawn.setAttribute("draggable", true);
            pawn.addEventListener("dragstart", (e) => {
                e.dataTransfer.effectAllowed = "move";
                e.dataTransfer.setData("text/plain", pawn.id);
                pawn.classList.add("dragging");
            });
            pawn.addEventListener("dragend", () => pawn.classList.remove("dragging"));
        });

        cells.forEach((cell) => {
            cell.addEventListener("dragover", (e) => e.preventDefault());
            cell.addEventListener("drop", (e) => {
                e.preventDefault();
                const draggedId = e.dataTransfer.getData("text/plain");
                const pawn = document.getElementById(draggedId);
                if (!pawn) return;
                cell.appendChild(pawn);
                socket.emit("update_pawn_position", {
                    pawnId: draggedId,
                    x: cell.parentNode.rowIndex,
                    y: cell.cellIndex,
                });
            });
        });
    }

    initializeDragAndDrop();
});
