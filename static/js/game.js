document.addEventListener("DOMContentLoaded", function () {
    const profileButton = document.getElementById("profile-button");
    const skillIcons = document.querySelectorAll('.skill-icon');
    const profilePopup = document.getElementById("profile-popup");
    const otherPlayerPopup = document.getElementById("other-player-popup");
    const closeButtons = document.querySelectorAll(".close-button");
    const rollDiceButton = document.getElementById("roll-dice-button");
    const diceResult = document.getElementById("dice-result");
    const volumeControl = document.getElementById('volume-control');
    const player = document.getElementById('game-music-player');
    const socket = io.connect('wss://familyrpg.servebeer.com', {
        transports: ['websocket']
    });

    window.addEventListener('beforeunload', function (e) {
        const confirmationMessage = 'Você tem certeza que deseja sair do lobby? Isso pode causar a perda de progresso.';
        e.returnValue = confirmationMessage; // Standard for most browsers
        return confirmationMessage; // For some other browsers
    });

    volumeControl.addEventListener('input', function() {
        player.volume = this.value;
    });
    
    player.volume = volumeControl.value;

    socket.on('new_media', function(data) {
        const mediaPopup = document.getElementById('media-popup');
        const mediaContainer = document.getElementById('media-container');

        if (mediaContainer) {
            mediaContainer.innerHTML = ''; // Clear previous contents

            if (data.media_url.match(/\.(jpeg|jpg|gif|png)$/i)) {
                const img = document.createElement('img');
                img.src = data.media_url;
                img.style.width = '100%'; // Adjust as necessary
                mediaContainer.appendChild(img);
            } else if (data.media_url.match(/\.(mp4|webm)$/i)) {
                const video = document.createElement('video');
                video.src = data.media_url;
                video.controls = true;
                video.autoplay = true;
                video.style.width = '100%'; // Ensure it fits in the container
                mediaContainer.appendChild(video);
            }

            // Show the popup
            mediaPopup.style.display = 'block';
        } else {
            console.error('Media container not found');
        }
    });
    

    rollDiceButton.addEventListener("click", function () {
        // Define um ponto de interrogação como valor inicial durante a rolagem
        diceResult.textContent = `🎲`;
        diceResult.classList.add("rolling");

        // Após 1.5 segundos (duração da animação), mostra o resultado real
        setTimeout(() => {
            const result = Math.floor(Math.random() * 20) + 1;
            diceResult.textContent = `🎲 ${result}`;
            diceResult.classList.remove("rolling");
        }, 1500); // Duração da animação definida em @keyframes
    });

    profileButton.addEventListener("click", function () {
        fetch('/get_current_player_details')
            .then(response => response.json())
            .then(data => {
                const detailsContainer = document.querySelector("#profile-popup .popup-content");
    
                const habilidades = data.habilidades ? data.habilidades : [];
                const pericias = data.pericias ? Object.entries(data.pericias) : [];
    
                // Verificação para garantir que img_url não seja undefined ou vazio
                const imgUrl = data.img_url ? data.img_url : '/static/images/default.png';
    
                detailsContainer.innerHTML = `
                    <span class="close-button">&times;</span>
                    <div class="profile-header">
                        <div class="profile-image">
                            <img src="${imgUrl}" alt="${data.name}" class="character-portrait-popup">
                        </div>
                        <h2>${data.name}</h2>
                    </div>
                    <p><strong>Classe:</strong> ${data.class_name}</p>
                    <p><strong>Raça:</strong> ${data.race_name}</p>
                    <div class="attributes">
                        <p><strong>Atributos:</strong></p>
                        <ul>
                            <li>Força: ${data.forca}</li>
                            <li>Destreza: ${data.destreza}</li>
                            <li>Constituição: ${data.constituicao}</li>
                            <li>Inteligência: ${data.inteligencia}</li>
                            <li>Sabedoria: ${data.sabedoria}</li>
                            <li>Carisma: ${data.carisma}</li>
                            <li>Mana: ${data.current_mana} / ${data.mana}</li>
                            <li>Energia: ${data.current_energy} / ${data.energia}</li>
                        </ul>
                    </div>
                    <div class="skills">
                        <p><strong>Habilidades:</strong></p>
                        <ul>
                            ${habilidades.map(habilidade => `
                                <li>
                                    <strong>${habilidade.name}</strong>: ${habilidade.description}<br>
                                    <small><em>Custo Mana: ${habilidade.cost_mana}, Custo Energia: ${habilidade.cost_energy}</em></small>
                                </li>
                            `).join('')}
                        </ul>
                        <p><strong>Perícias:</strong></p>
                        <ul>
                            ${pericias.map(([nome, valor]) => `<li>${nome}: +${valor}</li>`).join('')}
                        </ul>
                    </div>
                `;
                profilePopup.style.display = "block";
    
                // Adiciona evento de fechamento ao novo botão close criado dinamicamente
                document.querySelector("#profile-popup .close-button").addEventListener("click", function () {
                    profilePopup.style.display = "none";
                });
            })
            .catch(error => console.error('Error:', error));
    });
    
    

    // Listener de fechamento para os botões close existentes
    closeButtons.forEach(button => {
        button.addEventListener("click", function () {
            profilePopup.style.display = "none";
            otherPlayerPopup.style.display = "none";
        });
    });

    skillIcons.forEach(icon => {
        icon.addEventListener('click', function () {
            const skillId = this.getAttribute('data-skill-id');
            const manaCost = parseInt(this.getAttribute('data-skill-cost-mana'));
            const energyCost = parseInt(this.getAttribute('data-skill-cost-energy'));
    
            // Atualiza o personagem no servidor
            fetch('/use_skill', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    skill_id: skillId,
                    mana_cost: manaCost,
                    energy_cost: energyCost,
                    char_id: characterId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateManaBar(data.current_mana);
                    updateEnergyBar(data.current_energy);
                } else {
                    alert('Não foi possível usar a habilidade.');
                }
            });
        });
    });
    
    function updateMonsterHealth(monsterId, newHp) {
        const healthBar = document.querySelector(`.health-bar[data-monster-id="${monsterId}"] .health-fill`);
        const maxHp = document.querySelector(`.health-bar[data-monster-id="${monsterId}"]`).getAttribute('data-max-hp');
        const percentage = (newHp / maxHp) * 100;
        healthBar.style.width = percentage + '%';
    
        const healthText = document.querySelector(`.health-bar[data-monster-id="${monsterId}"] .health-text`);
        healthText.textContent = `${newHp} / ${maxHp}`;
    }
    
    function updateManaBar(newMana) {
        const manaBall = document.querySelector('.mana-ball[data-character-id="' + characterId + '"] .mana-fill');
        const maxMana = document.querySelector('.mana-ball[data-character-id="' + characterId + '"]').getAttribute('data-max-mana');
        const percentage = (newMana / maxMana) * 100;
        manaBall.style.height = percentage + '%';

        const manaText = document.querySelector('.mana-ball[data-character-id="' + characterId + '"] .mana-text');
        manaText.textContent = newMana + ' / ' + maxMana;
    }
    
    function updateEnergyBar(newEnergy) {
        const energyBall = document.querySelector('.energy-ball[data-character-id="' + characterId + '"] .energy-fill');
        const maxEnergy = document.querySelector('.energy-ball[data-character-id="' + characterId + '"]').getAttribute('data-max-energy');
        const percentage = (newEnergy / maxEnergy) * 100;
        energyBall.style.height = percentage + '%';

        const energyText = document.querySelector('.energy-ball[data-character-id="' + characterId + '"] .energy-text');
        energyText.textContent = newEnergy + ' / ' + maxEnergy;
    }
    

    function attachPlayerClickEvent(playerElement) {
        playerElement.addEventListener("click", function () {
            const playerId = this.getAttribute("data-player-id");
            fetch(`/get_player_details/${playerId}`)
                .then(response => response.json())
                .then(data => {
                    const detailsContainer = document.getElementById("other-player-details");
    
                    const habilidades = data.habilidades ? data.habilidades : [];
                    const pericias = data.pericias ? Object.entries(data.pericias) : [];
    
                    // Verificação para garantir que img_url não seja undefined ou vazio
                    const imgUrl = data.img_url ? data.img_url : '/static/images/default.png';
    
                    detailsContainer.innerHTML = `
                        <div class="profile-header">
                        <div class="profile-image">
                            <img src="${imgUrl}" alt="${data.name}" class="character-portrait-popup">
                        </div>
                        <h2>${data.name}</h2>
                    </div>
                        <p><strong>Classe:</strong> ${data.class_name}</p>
                        <p><strong>Raça:</strong> ${data.race_name}</p>
                        <div class="attributes">
                            <p><strong>Atributos:</strong></p>
                            <ul>
                                <li>Força: ${data.forca}</li>
                                <li>Destreza: ${data.destreza}</li>
                                <li>Constituição: ${data.constituicao}</li>
                                <li>Inteligência: ${data.inteligencia}</li>
                                <li>Sabedoria: ${data.sabedoria}</li>
                                <li>Carisma: ${data.carisma}</li>
                                <li>Mana: ${data.current_mana} / ${data.mana}</li>
                                <li>Energia: ${data.current_energy} / ${data.energia}</li>
                            </ul>
                        </div>
                        <div class="skills">
                            <p><strong>Habilidades:</strong></p>
                            <ul>
                                ${habilidades.map(habilidade => `
                                    <li>
                                        <strong>${habilidade.name}</strong>: ${habilidade.description}<br>
                                        <small><em>Custo Mana: ${habilidade.cost_mana}, Custo Energia: ${habilidade.cost_energy}</em></small>
                                    </li>
                                `).join('')}
                            </ul>
                            <p><strong>Perícias:</strong></p>
                            <ul>
                                ${pericias.map(([nome, valor]) => `<li>${nome}: +${valor}</li>`).join('')}
                            </ul>
                        </div>
                    `;
                    otherPlayerPopup.style.display = "block";
    
                    // Adiciona evento de fechamento ao novo botão close criado dinamicamente
                    document.querySelector("#other-player-popup .close-button").addEventListener("click", function () {
                        otherPlayerPopup.style.display = "none";
                    });
                })
                .catch(error => console.error('Error:', error));
        });
    }
    
    

    // Adiciona listeners aos jogadores que já estão na lista
    document.querySelectorAll(".other-player").forEach(attachPlayerClickEvent);



    socket.on('connect', function () {
        socket.emit('join', { data: 'Player joined!' });
    });

    socket.on('mana_energy_updated', function(data) {
        if (data.character_id === characterId) {
            updateManaBar(data.current_mana);
            updateEnergyBar(data.current_energy);
        }
    });    

    socket.on('session_sync', function(data) {
        const playerList = document.querySelector('.other-players ul');
        playerList.innerHTML = ''; // Limpa a lista existente
        
        const boardCenter = document.querySelector('.board-center');
        boardCenter.innerHTML = ''; // Limpa a lista de monstros
        
        if (data.characters && Array.isArray(data.characters)) {
        data.characters.forEach(char => {
            const newPlayerHTML = `
                <li class="other-player" data-player-id="${char._id}">
                    <div class="profile-header">
                        <div class="profile-image">
                            <img src="${char.img_url}" alt="${char.name}" class="character-portrait-popup">
                        </div>
                    </div>
                    <div class="player-stats">
                        <p>${char.name}</p>
                        <p>Classe: ${char.class_name}</p>
                        <p>Raça: ${char.race_name}</p>
                        <p>HP: ${char.current_hp} / ${char.hp}</p>
                        <p>Mana: ${char.current_mana} / ${char.mana}</p>
                        <p>Energia: ${char.current_energy} / ${char.energia}</p>
                    </div>
                </li>
            `;
            playerList.insertAdjacentHTML('beforeend', newPlayerHTML);
            attachPlayerClickEvent(playerList.querySelector(`.other-player[data-player-id="${char._id}"]`));
        });
    } else {
        console.error('characters data is undefined or not an array');
    }
    
        // Adicionar monstros ao DOM
        data.monsters.forEach(monster => {
            addMonsterToDOM(monster);
        });
    });
    
    
    

    socket.on('new_player', function(data) {
        console.log('New player joined:', data);  // Log de depuração
        const playerList = document.querySelector('.other-players ul');
        const existingPlayer = document.querySelector(`.other-player[data-player-id="${data._id}"]`);
        
        // Verifica se o jogador já existe na lista para evitar duplicações
        if (existingPlayer) return;
        
        const newPlayerHTML = `
            <li class="other-player" data-player-id="${data._id}">
                <div class="profile-header">
                    <div class="profile-image">
                        <img src="${data.img_url}" alt="${data.name}" class="character-portrait-popup">
                    </div>
                </div>
                <div class="player-stats">
                    <p>${data.name}</p>
                    <p>Classe: ${data.class_name}</p>
                    <p>Raça: ${data.race_name}</p>
                    <p>HP: ${data.current_hp} / ${data.hp}</p>
                    <p>Mana: ${data.current_mana} / ${data.mana}</p>
                    <p>Energia: ${data.current_energy} / ${data.energia}</p>
                </div>
            </li>
        `;
        playerList.insertAdjacentHTML('beforeend', newPlayerHTML);
    
        // Adiciona o evento de clique ao novo jogador adicionado
        const newPlayerElement = playerList.querySelector(`.other-player[data-player-id="${data._id}"]`);
        attachPlayerClickEvent(newPlayerElement);
    });
    
    socket.on('play_music', function(data) {
        const player = document.getElementById('game-music-player');
        if (player.src !== data.track_url) {
            player.pause();  // Pause the player before changing the source
            player.src = data.track_url;
            player.play().catch(error => {
                console.error('Failed to play the music:', error);
            });
        }
    });

    socket.on('stop_music', function() {
        const player = document.getElementById('game-music-player');
        player.pause();  // Ensure the player is paused
        player.src = '';  // Clear the source to fully stop the music
    });

    socket.on('player_left', function (data) {
        const playerElement = document.querySelector(`.other-player[data-player-id="${data._id}"]`);
        if (playerElement) playerElement.remove();
    });

    socket.on('health_updated', function(data) {
        console.log('Health update received:', data);  // Log de depuração
        const healthBall = document.querySelector(`.health-ball[data-character-id="${data.character_id}"] .health-fill`);
        const maxHp = document.querySelector(`.health-ball[data-character-id="${data.character_id}"]`).getAttribute('data-max-hp');
        const percentage = (data.new_health / maxHp) * 100;
        healthBall.style.height = percentage + '%';
    
        const healthText = document.querySelector(`.health-ball[data-character-id="${data.character_id}"] .health-text`);
        healthText.textContent = data.new_health + ' / ' + maxHp;
    });

    socket.on('monster_added', function(data) {
        const boardCenter = document.querySelector('.board-center');
        
        if (boardCenter && !document.querySelector(`[data-monster-id="${data._id}"]`)) {
            const monsterElement = document.createElement('div');
            monsterElement.classList.add('enemy-card');
            monsterElement.dataset.monsterId = data._id;
            monsterElement.innerHTML = `
                <h4>${data.name}</h4>
                <img src="${data.img_url}" alt="${data.name}" class="monster-image">
                <div class="health-bar">
                    <div class="health-fill" style="width: ${(data.current_hp / data.hp) * 100}%"></div>
                    <div class="health-text">HP: ${data.current_hp} / ${data.hp}</div>
                </div>
                <p>${data.resumo}</p>
            `;
            boardCenter.appendChild(monsterElement);
        }
    });
    

    
    socket.on('monster_hp_updated', function(data) {
        const monsterElement = document.querySelector(`div[data-monster-id="${data.monster_id}"]`);
        if (monsterElement) {
            const hpElement = monsterElement.querySelector('.monster-hp');
            hpElement.textContent = `HP: ${data.new_hp}`;
        }
    });
    // Função para remover monstros da tela dos jogadores
    socket.on('monster_removed', function(data) {
        const monsterElement = document.querySelector(`div[data-monster-id="${data._id}"]`);
        if (monsterElement) {
            monsterElement.remove();
        }
    });

    function addMonsterToDOM(monster) {
        const monsterCard = `
        <div class="enemy-card" data-monster-id="${monster._id}">
            <h4>${monster.name}</h4>
            <img src="${monster.img_url}" alt="${monster.name}" class="monster-image">
            <p class="monster-hp">HP: ${monster.current_hp} / ${monster.hp}</p>
            <p>Mana: ${monster.current_mana} / ${monster.mana}</p>
            <p>Energia: ${monster.current_energia} / ${monster.energia}</p>
            <p>${monster.resumo}</p>
        </div>
        `;
        document.querySelector('.board-center').insertAdjacentHTML('beforeend', monsterCard);
    }
    

    socket.on('status_updated', function(data) {
        console.log('Status update received:', data);  // Log de depuração
        const statusField = document.querySelector(`.status-input[data-char-id="${data.character_id}"]`);
        if (statusField) {
            statusField.value = data.status;
        }
    });

    window.onclick = function (event) {
        if (event.target === profilePopup) {
            profilePopup.style.display = "none";
        } else if (event.target === otherPlayerPopup) {
            otherPlayerPopup.style.display = "none";
        }
    };

});