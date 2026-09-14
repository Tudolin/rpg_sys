document.addEventListener("DOMContentLoaded", function () {
    const GAME = window.GAME || {};
    const system = GAME.system || { resources: [], attributes: [] };
    const characterId = GAME.characterId;
    const sessionId = GAME.sessionId;
    const staticBaseUrl = GAME.staticBaseUrl || "/static/images/monsters/";

    const profileButton = document.getElementById("profile-button");
    const skillIcons = document.querySelectorAll(".skill-icon");
    const profilePopup = document.getElementById("profile-popup");
    const otherPlayerPopup = document.getElementById("other-player-popup");
    const closeButtons = document.querySelectorAll(".close-button");
    const rollDiceButton = document.getElementById("roll-dice-button");
    const diceResult = document.getElementById("dice-result");
    const volumeControl = document.getElementById("volume-control");
    const player = document.getElementById("game-music-player");

    const socket = createSessionSocket();

    window.addEventListener("beforeunload", function (e) {
        const confirmationMessage = "Você tem certeza que deseja sair do lobby? Isso pode causar a perda de progresso.";
        e.returnValue = confirmationMessage;
        return confirmationMessage;
    });

    if (volumeControl && player) {
        volumeControl.addEventListener("input", function () {
            player.volume = this.value;
        });
        player.volume = volumeControl.value;
    }

    function resourceLabel(key) {
        const def = system.resources.find((r) => r.key === key);
        return def ? def.label : key;
    }

    function formatCost(cost) {
        return Object.entries(cost || {})
            .filter(([, amount]) => amount)
            .map(([key, amount]) => `${resourceLabel(key)}: ${amount}`)
            .join(", ") || "Sem custo";
    }

    socket.on("new_media", function (data) {
        const mediaPopup = document.getElementById("media-popup");
        const mediaContainer = document.getElementById("media-container");
        if (!mediaContainer) return;

        mediaContainer.innerHTML = "";
        if (data.media_url.match(/\.(jpeg|jpg|gif|png|webp)$/i)) {
            const img = document.createElement("img");
            img.src = data.media_url;
            img.style.width = "100%";
            mediaContainer.appendChild(img);
        } else if (data.media_url.match(/\.(mp4|webm)$/i)) {
            const video = document.createElement("video");
            video.src = data.media_url;
            video.controls = true;
            video.autoplay = true;
            video.style.width = "100%";
            mediaContainer.appendChild(video);
        }
        mediaPopup.style.display = "flex";
    });

    if (rollDiceButton) {
        rollDiceButton.addEventListener("click", function () {
            diceResult.textContent = "🎲";
            diceResult.classList.add("rolling");
            setTimeout(() => {
                const result = Math.floor(Math.random() * 20) + 1;
                diceResult.textContent = `🎲 ${result}`;
                diceResult.classList.remove("rolling");
            }, 1500);
        });
    }

    function renderCharacterSheet(container, data) {
        const habilidades = data.habilidades || [];
        const attributes = Object.entries(data.attributes || {});
        const resources = Object.entries(data.resources || {});
        const imgUrl = data.img_url || "/static/images/default.png";

        container.innerHTML = `
            <span class="close-button">&times;</span>
            <div class="profile-header">
                <div class="profile-image">
                    <img src="${imgUrl}" alt="${data.name}" class="character-portrait-popup">
                </div>
                <h2>${data.name}</h2>
            </div>
            <p><strong>${system.class_label}:</strong> ${data.class_name}</p>
            ${data.race_name ? `<p><strong>${system.race_label}:</strong> ${data.race_name}</p>` : ""}
            <div class="attributes">
                <p><strong>Atributos:</strong></p>
                <ul>
                    ${attributes.map(([key, value]) => {
                        const def = system.attributes.find((a) => a.key === key);
                        return `<li>${def ? def.label : key}: ${value}</li>`;
                    }).join("")}
                    ${resources.map(([key, value]) => `<li>${resourceLabel(key)}: ${value.current} / ${value.max}</li>`).join("")}
                </ul>
            </div>
            <div class="skills">
                <p><strong>${system.ability_label}:</strong></p>
                <ul>
                    ${habilidades.map((h) => `
                        <li>
                            <strong>${h.name}</strong>: ${h.description}<br>
                            <small><em>${formatCost(h.cost)}</em></small>
                        </li>
                    `).join("")}
                </ul>
                <p><strong>${system.skill_label}:</strong></p>
                <ul>
                    ${Object.entries(data.pericias || {}).map(([nome, valor]) => `<li>${nome}: +${valor}</li>`).join("")}
                </ul>
            </div>
        `;
    }

    if (profileButton) {
        profileButton.addEventListener("click", function () {
            fetch("/get_current_player_details")
                .then((response) => response.json())
                .then((data) => {
                    renderCharacterSheet(document.querySelector("#profile-popup .popup-content"), data);
                    profilePopup.style.display = "flex";
                    document.querySelector("#profile-popup .close-button").addEventListener("click", function () {
                        profilePopup.style.display = "none";
                    });
                })
                .catch((error) => console.error("Error:", error));
        });
    }

    closeButtons.forEach((button) => {
        button.addEventListener("click", function () {
            if (profilePopup) profilePopup.style.display = "none";
            if (otherPlayerPopup) otherPlayerPopup.style.display = "none";
        });
    });

    skillIcons.forEach((icon) => {
        icon.addEventListener("click", function () {
            const skillId = this.getAttribute("data-skill-id");
            let cost = {};
            try {
                cost = JSON.parse(this.getAttribute("data-skill-cost") || "{}");
            } catch (e) {
                console.error("Invalid skill cost data", e);
            }

            fetch("/use_skill", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ skill_id: skillId, cost: cost, char_id: characterId }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        applyResourceUpdate(characterId, data.resources);
                    } else {
                        alert(data.message || "Não foi possível usar a habilidade.");
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    });

    function attachPlayerClickEvent(playerElement) {
        playerElement.addEventListener("click", function () {
            const playerId = this.getAttribute("data-player-id");
            fetch(`/get_player_details/${playerId}`)
                .then((response) => response.json())
                .then((data) => {
                    renderCharacterSheet(document.querySelector("#other-player-popup .popup-content"), data);
                    otherPlayerPopup.style.display = "flex";
                    document.querySelector("#other-player-popup .close-button").addEventListener("click", function () {
                        otherPlayerPopup.style.display = "none";
                    });
                })
                .catch((error) => console.error("Error:", error));
        });
    }

    document.querySelectorAll(".other-player").forEach(attachPlayerClickEvent);

    function resourceOrbsHTML(charId, resources) {
        return system.resources.map((res) => {
            const value = (resources && resources[res.key]) || { current: 0, max: 1 };
            const pct = value.max > 0 ? Math.max(0, Math.min(100, (value.current / value.max) * 100)) : 0;
            return `
                <div class="resource-orb resource-${res.color}" data-character-id="${charId}" data-resource-key="${res.key}" data-max="${value.max}">
                    <div class="resource-fill" style="height: ${pct}%"></div>
                    <div class="resource-text">${value.current} / ${value.max}</div>
                </div>
            `;
        }).join("");
    }

    function renderOtherPlayers(characters) {
        const playerList = document.querySelector(".other-players ul");
        if (!playerList) return;
        playerList.innerHTML = "";

        (characters || []).forEach((char) => {
            const li = document.createElement("li");
            li.className = "other-player";
            li.dataset.playerId = char._id;
            li.innerHTML = `
                <div class="character-frame-small">
                    <img src="${char.img_url}" alt="${char.name}" class="character-portrait-small">
                </div>
                <div class="player-stats">
                    <p>${char.name}</p>
                    <p>${char.class_name}${char.race_name ? " · " + char.race_name : ""}</p>
                    <div class="resource-orbs resource-orbs-compact">${resourceOrbsHTML(char._id, char.resources)}</div>
                </div>
            `;
            playerList.appendChild(li);
            attachPlayerClickEvent(li);
        });
    }

    function updateMonsterInDOM(monster) {
        if (document.querySelector(`.enemy-card[data-monster-id="${monster._id}"]`)) return;

        const boardCenter = document.querySelector(".board-center");
        if (!boardCenter) return;

        const monsterElement = document.createElement("div");
        monsterElement.classList.add("enemy-card");
        monsterElement.dataset.monsterId = monster._id;
        monsterElement.setAttribute("data-max-hp", monster.hp);

        const imageUrl = staticBaseUrl + monster.img_url;
        monsterElement.innerHTML = `
            <h4>${monster.name}</h4>
            <img src="${imageUrl}" alt="${monster.name}" class="monster-image">
            <div class="monster-health-bar">
                <div class="monster-health-fill" style="width: ${(monster.current_hp / monster.hp) * 100}%;"></div>
                <div class="monster-health-text">HP: ${monster.current_hp} / ${monster.hp}</div>
            </div>
            <p>${monster.resumo}</p>
        `;
        boardCenter.appendChild(monsterElement);
    }

    function renderMonsters(monsters) {
        const boardCenter = document.querySelector(".board-center");
        if (!boardCenter) return;
        boardCenter.innerHTML = "";
        (monsters || []).forEach(updateMonsterInDOM);
    }

    socket.on("session_sync", function (data) {
        renderOtherPlayers((data.characters || []).filter((c) => c._id !== characterId));
        renderMonsters(data.monsters);
    });

    socket.on("resources_updated", function (data) {
        applyResourceUpdate(data.character_id, data.resources);
    });

    socket.on("monster_added", function (data) {
        if (document.querySelector(`.enemy-card[data-monster-id="${data._id}"]`)) return;
        updateMonsterInDOM(data);
        if (data.spawn_som) {
            const audio = new Audio(`/static/spawn/${data.spawn_som}`);
            audio.play().catch((error) => console.error("Failed to play monster spawn sound:", error));
        }
    });

    socket.on("monster_stats_updated", function (data) {
        const monsterElement = document.querySelector(`.enemy-card[data-monster-id="${data.monster_id}"]`);
        if (!monsterElement) return;
        const healthFill = monsterElement.querySelector(".monster-health-fill");
        const healthText = monsterElement.querySelector(".monster-health-text");
        const maxHp = parseInt(monsterElement.getAttribute("data-max-hp"), 10) || data.hp;
        if (healthFill && healthText && maxHp) {
            const percentage = (data.current_hp / maxHp) * 100;
            healthFill.style.width = `${percentage}%`;
            healthText.textContent = `HP: ${data.current_hp} / ${maxHp}`;
        }
    });

    socket.on("monster_removed", function (data) {
        const monsterElement = document.querySelector(`.enemy-card[data-monster-id="${data.monster_id}"]`);
        if (monsterElement) monsterElement.remove();
    });

    if (player) {
        socket.on("play_music", function (data) {
            if (player.src !== data.track_url) {
                player.pause();
                player.src = data.track_url;
                player.play().catch((error) => console.error("Failed to play the music:", error));
            }
        });

        socket.on("stop_music", function () {
            player.pause();
            player.src = "";
        });
    }

    window.onclick = function (event) {
        if (event.target === profilePopup) profilePopup.style.display = "none";
        if (event.target === otherPlayerPopup) otherPlayerPopup.style.display = "none";
    };
});
