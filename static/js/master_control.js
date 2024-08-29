document.addEventListener("DOMContentLoaded", function() {
    const socket = io.connect('wss://familyrpg.servebeer.com', {
        transports: ['websocket']
    });

    const mediaForm = document.getElementById('media-form');
    
    const effectSelects = document.querySelectorAll('.status-effect-select');
    const audioPlayer = document.getElementById('audio-player');
    const forms = document.querySelectorAll(`.character-form[data-session-id="${sessionId}"]`);
    const musicSelect = document.getElementById('music-select');
    const currentTrackElement = document.getElementById('current-track');
    const playerList = document.querySelector('.characters-container .character-list');
    const addMonsterForm = document.getElementById('add-monster-form');
    const monsterSelect = document.getElementById('monster-select');
    const monsterQuantityInput = document.getElementById('monster-quantity');
    const monsterList = document.getElementById('monster-list');

    if (addMonsterForm) {
        addMonsterForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const monsterId = monsterSelect.value;
            const quantity = parseInt(monsterQuantityInput.value);

            console.log(`Attempting to add ${quantity} of monster with ID: ${monsterId}`);

            if (monsterId && quantity > 0) {
                for (let i = 0; i < quantity; i++) {
                    socket.emit('add_monster', { monster_id: monsterId, session_id: sessionId });
                }
            }
        });
    }

    socket.emit('request_master_sync', { session_id: sessionId });

    socket.on('master_sync', function(data) {
        updatePlayersList(data.characters);
        updateMonstersList(data.monsters);
    });

    socket.on('monster_added', function(monster) {
        addMonsterToDOM(monster);
    });

    socket.on('monster_added', function(data) {
        const monsterList = document.getElementById('monster-list');
        const monsterElement = document.createElement('li');
        monsterElement.dataset.monsterId = data._id;
        monsterElement.innerHTML = `
            <div class="enemy-card">
                <img src="${data.img_url}" alt="${data.name}" class="monster-image">
                <h4>${data.name}</h4>
                <p>HP: <span class="monster-hp">${data.current_hp}</span> / ${data.hp}</p>
                <button class="remove-monster-button" onclick="removeMonster('${data._id}')">Remover</button>
            </div>
        `;
        monsterList.appendChild(monsterElement);

        const form = monsterElement.querySelector('.monster-form');
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const monsterId = form.getAttribute('data-monster-id');
            const newHp = form.querySelector('.monster-hp-input').value;

            console.log(`Updating HP of monster with ID: ${monsterId} to ${newHp}`);

            socket.emit('update_monster_hp', {
                monster_id: monsterId,
                new_hp: newHp,
                session_id: sessionId
            });
        });

        monsterElement.querySelector('.remove-monster-button').addEventListener('click', function() {
            const monsterId = this.getAttribute('data-monster-id');
            console.log(`Attempting to remove monster with ID: ${monsterId}`);
            socket.emit('remove_monster', { monster_id: monsterId, session_id: sessionId });
        });
    });

    function removeMonster(monsterId) {
        fetch('/remove_monster', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                monster_id: monsterId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const monsterElement = document.querySelector(`li[data-monster-id="${monsterId}"]`);
                if (monsterElement) {
                    monsterElement.remove();
                }
            }
        })
        .catch(error => console.error('Erro:', error));
    }

    socket.on('monster_hp_updated', function(data) {
        console.log('Received monster_hp_updated event with data:', data);
        const monsterElement = document.querySelector(`li[data-monster-id="${data._id}"]`);
        if (monsterElement) {
            const hpInput = monsterElement.querySelector('.monster-hp-input');
            hpInput.value = data.current_hp;
        }
    });

    socket.on('connect', function() {
        console.log('Connected to the server, requesting session sync...');
        socket.emit('request_session_sync', { session_id: sessionId });
    });
    

    socket.on('session_sync', function(data) {
        console.log('Received session sync:', data);
        if (data && data.characters && data.characters.length > 0) {
            updatePlayerList(data.characters);
        } else {
            console.warn('No characters found in session sync data.');
        }
    });

    socket.on('mana_energy_updated_master', function(data) {
        const playerElement = document.querySelector(`.character-form[data-char-id="${data.character_id}"]`);
        if (playerElement) {
            const manaField = playerElement.querySelector('.mana-input');
            const energyField = playerElement.querySelector('.energy-input');
            
            if (manaField) manaField.value = data.current_mana;
            if (energyField) energyField.value = data.current_energy;
        }
    });
    

    socket.on('new_player', function(data) {
        addOrUpdatePlayer(data);
    });

    socket.on('player_left', function(data) {
        const playerElement = document.querySelector(`div[data-player-id="${data._id}"]`);
        if (playerElement) {
            playerElement.remove();
        }
    });

    function updatePlayersList(players) {
        const playersContainer = document.querySelector('.characters-container');
        playersContainer.innerHTML = '';
        players.forEach(player => {
            const playerCard = `
            <div class="character-card" data-player-id="${player._id}">
                <p><strong>${player.name}</strong></p>
                <form method="POST" class="character-form" data-char-id="${player._id}">
                    <input type="hidden" name="char_id" value="${player._id}">
                    <label>HP: <input type="number" name="hp" value="${player.current_hp}" class="hp-input"> / ${player.hp}</label><br>
                    <label>Mana: <input type="number" name="mana" value="${player.current_mana}" class="mana-input"> / ${player.mana}</label><br>
                    <label>Energia: <input type="number" name="energia" value="${player.current_energy}" class="energy-input"> / ${player.energia}</label><br>
                    <button type="submit">Atualizar</button>
                </form>
            </div>`;
            playersContainer.insertAdjacentHTML('beforeend', playerCard);
        });
    }

    function updateMonstersList(monsters) {
        const monsterList = document.getElementById('monster-list');
        monsterList.innerHTML = '';
        monsters.forEach(monster => {
            addMonsterToDOM(monster);
        });
    }

    function addMonsterToDOM(monster) {
        const monsterCard = `
        <li class="enemy-card" data-monster-id="${monster._id}">
            <h4>${monster.name}</h4>
            <img src="${monster.img_url}" alt="${monster.name}" class="monster-image">
            <p>HP: ${monster.current_hp} / ${monster.hp}</p>
            <p>Mana: ${monster.current_mana} / ${monster.mana}</p>
            <p>Energia: ${monster.current_energia} / ${monster.energia}</p>
            <p>${monster.resumo}</p>
            <button class="remove-monster-button" data-monster-id="${monster._id}">Remover</button>
        </li>`;
        
    }

    document.getElementById('monster-list').addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-monster-button')) {
            const monsterId = e.target.getAttribute('data-monster-id');
            socket.emit('remove_monster', { monster_id: monsterId, session_id: sessionId });
        }
    });
    
    socket.on('monster_removed', function(data) {
        const monsterElement = document.querySelector(`li[data-monster-id="${data._id}"]`);
        if (monsterElement) {
            monsterElement.remove();
        }
    });
    

    function addOrUpdatePlayer(char) {
        let existingPlayer = playerList.querySelector(`.character-form[data-char-id="${char._id}"]`);
    
        if (existingPlayer) {
            updatePlayerElement(existingPlayer, char);
        } else {
            createPlayerElement(char);
        }
    }

    function updatePlayerElement(element, char) {
        const hpInput = element.querySelector('.hp-input');
        hpInput.value = char.hp;
        // Update other elements as necessary
    }

    function createPlayerElement(char) {
        const newPlayerHTML = `
            <div class="character-card">
                <form method="POST" class="character-form" data-char-id="${char._id}">
                    <input type="hidden" name="char_id" value="${char._id}">
                    <p><strong>${char.name}</strong></p>
                    <label>HP: <input type="number" name="hp" value="${char.current_hp}" class="hp-input"></label><br>
                    <label>Mana: <input type="number" name="mana" value="${char.current_mana}" class="mana-input"></label><br>
                    <label>Energia: <input type="number" name="energia" value="${char.current_energy}" class="energy-input"></label><br>
                    <button type="submit">Atualizar</button>
                </form>
            </div>
        `;
        playerList.insertAdjacentHTML('beforeend', newPlayerHTML);

        const newForm = playerList.querySelector(`.character-form[data-char-id="${char._id}"]`);
    newForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const charId = newForm.getAttribute('data-char-id');
        const hp = newForm.querySelector('.hp-input').value;
        const mana = newForm.querySelector('.mana-input').value;
        const energy = newForm.querySelector('.energy-input').value;

        // Emite o evento de atualização de saúde, mana e energia via socket
        socket.emit('update_character_status', {
            character_id: charId,
            new_health: hp,
            new_mana: mana,
            new_energy: energy
        });
    });
    }

    function removePlayerFromList(charId) {
        const playerElement = playerList.querySelector(`.character-form[data-char-id="${charId}"]`);
        if (playerElement) {
            playerElement.remove();
        }
    }

    if (mediaForm) {
        mediaForm.addEventListener('submit', function(event) {
            event.preventDefault();  // Prevent the default form submission
            
            const formData = new FormData(this);  // 'this' refers to the form itself
            const fileInput = document.getElementById('media-input');
            
            // Check if a file is selected
            if (fileInput.files.length === 0) {
                console.error('No file selected!');
                return;
            }
            
            formData.append('media', fileInput.files[0]);
            const displayTime = document.getElementById('display-time').value;
            formData.append('display_time', displayTime);
        
            fetch('/upload_media', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    console.log('Media uploaded successfully!', data.media_url);
                    // Additional actions can be performed here with data.media_url
                } else {
                    throw new Error('Error uploading media: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error.message);
            });
        });
    }

function removePlayer(charId) {
    fetch(`/remove_player/${charId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Player removed successfully');
            socket.emit('player_removed', { character_id: charId });
        } else {
            console.error('Failed to remove player');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Listener para o botão de remoção
document.querySelectorAll('.remove-player-button').forEach(button => {
    button.addEventListener('click', function() {
        const charId = this.getAttribute('data-char-id');
        removePlayer(charId);
    });
});

document.getElementById('add-monster-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const monsterId = document.getElementById('monster-select').value;
    const quantity = document.getElementById('monster-quantity').value;

    fetch('/add_monster_to_session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            session_id: sessionId,
            monster_id: monsterId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Monstro adicionado com sucesso');
        } else {
            console.error('Erro ao adicionar monstro:', data.message);
        }
    })
    .catch(error => console.error('Erro:', error));
});


// Recebe notificação de jogador removido e remove da lista
socket.on('player_removed', function(data) {
    const characterForm = document.querySelector(`.character-form[data-char-id="${data.character_id}"]`);
    if (characterForm) {
        characterForm.remove();
    }
});

    effectSelects.forEach(select => {
        select.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const description = selectedOption.getAttribute('data-description');
            const descriptionElement = this.parentNode.querySelector('.effect-description');
            
            descriptionElement.textContent = description ? description : '';
        });
    });

    function saveMusicState() {
        localStorage.setItem('musicPlayerState', JSON.stringify({
            trackUrl: audioPlayer.src,
            currentTime: audioPlayer.currentTime,
            playing: !audioPlayer.paused
        }));
    }

    function loadMusicState() {
        const savedState = localStorage.getItem('musicPlayerState');
        if (savedState) {
            const { trackUrl, currentTime, playing } = JSON.parse(savedState);
            if (trackUrl) {
                audioPlayer.src = trackUrl;
                audioPlayer.currentTime = currentTime;
                if (playing) {
                    audioPlayer.play();
                }
                const selectedOption = document.querySelector(`#music-select option[value="${trackUrl}"]`);
                if (selectedOption) {
                    currentTrackElement.textContent = `Reproduzindo: ${selectedOption.textContent}`;
                }
            }
        }
    }

    loadMusicState();
    // Carrega as faixas de música
    fetch('/music_tracks')
        .then(response => response.json())
        .then(tracks => {
            musicSelect.innerHTML = '';
            tracks.forEach(track => {
                const option = document.createElement('option');
                option.value = track.url;
                option.textContent = track.name;
                musicSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Erro ao carregar músicas:', error));

    document.getElementById('play-button').addEventListener('click', function () {
        const selectedTrack = musicSelect.value;
        
        if (selectedTrack && audioPlayer.src !== selectedTrack) { // Apenas altere se a faixa for diferente da atual
            audioPlayer.src = selectedTrack;
            audioPlayer.play();
    
            // Atualiza o nome da faixa em reprodução
            const selectedOption = document.querySelector(`#music-select option[value="${selectedTrack}"]`);
            currentTrackElement.textContent = `Reproduzindo: ${selectedOption.textContent}`;
    
            // Envia o evento de tocar música para os outros clientes
            fetch('/play_music', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ track_url: selectedTrack }),
            });

            // Salva o estado da música
            saveMusicState();
        }
    });

    // Listener para o botão de parar música
    document.getElementById('stop-button').addEventListener('click', function () {
        audioPlayer.pause();
        audioPlayer.src = '';
        currentTrackElement.textContent = 'Nenhuma música em reprodução';
        localStorage.removeItem('musicPlayerState'); // Remove o estado salvo

        fetch('/stop_music', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
    });

    socket.on('connect', function() {
        socket.emit('request_session_sync', { session_id: sessionId });
    });

    socket.on('session_sync', function(data) {
        console.log('Received session sync:', data);
            if (data && data.characters && data.characters.length > 0) {
                updatePlayerList(data.characters);
            } else {
                console.warn('No characters found in session sync data.');
            }
    
        data.characters.forEach(char => {
            const newPlayerHTML = `
                <div class="character-card">
                    <form method="POST" class="character-form" data-char-id="${char._id}">
                        <input type="hidden" name="char_id" value="${char._id}">
                        <p><strong>${char.name}</strong></p>
                        <label>HP: <input type="number" name="hp" value="${char.hp}" class="hp-input"></label><br>
                        <button type="submit">Atualizar</button>
                    </form>
                </div>
            `;
            playerList.insertAdjacentHTML('beforeend', newPlayerHTML);
    
            const newForm = playerList.querySelector(`.character-form[data-char-id="${char._id}"]`);
            newForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const charId = newForm.getAttribute('data-char-id');
            const hp = newForm.querySelector('.hp-input').value;
            const mana = newForm.querySelector('.mana-input').value;
            const energy = newForm.querySelector('.energy-input').value;

            // Emite o evento de atualização de saúde, mana e energia via socket
            socket.emit('update_character_status', {
                character_id: charId,
                new_health: hp,
                new_mana: mana,
                new_energy: energy
            });
        });
    });
    });

    socket.on('mana_energy_updated', function(data) {
        const characterForm = document.querySelector(`.character-form[data-char-id="${data.character_id}"]`);
        if (characterForm) {
            const manaInput = characterForm.querySelector('.mana-input');
            const energyInput = characterForm.querySelector('.energy-input');
            
            if (manaInput) manaInput.value = data.current_mana;
            if (energyInput) energyInput.value = data.current_energy;
        }
    });
    
    
    // Reproduz música enviada pelos sockets
    socket.on('play_music', function(data) {
        if (audioPlayer.src !== data.track_url) { // Evita reiniciar a música se a faixa já estiver tocando
            audioPlayer.src = data.track_url;
            audioPlayer.play();
            currentTrackElement.textContent = `Reproduzindo: ${data.track_url.split('/').pop().split('.').slice(0, -1).join('.')}`;
            saveMusicState(); // Salva o estado da música
        }
    });

    // Para a música pelos sockets
    socket.on('stop_music', function() {
        audioPlayer.pause();
        audioPlayer.src = '';
        currentTrackElement.textContent = 'Nenhuma música em reprodução';
        localStorage.removeItem('musicPlayerState'); // Remove o estado salvo
    });

    window.addEventListener('beforeunload', saveMusicState);
    window.addEventListener('unload', saveMusicState);
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const charId = form.getAttribute('data-char-id');
            const hp = form.querySelector('.hp-input').value;
            const statusEffect = form.querySelector('.status-effect-select').value;
            const effectDescription = form.querySelector('.status-effect-select option:checked').getAttribute('data-description');
            const effectIcon = form.querySelector('.status-effect-select option:checked').getAttribute('data-icon');
            
            fetch('/update_character', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    char_id: charId,
                    hp: hp,
                    status_effect: statusEffect,
                    effect_description: effectDescription,
                    effect_icon: effectIcon
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Status atualizado com sucesso');
                } else {
                    console.error('Falha ao atualizar status');
                }
            })
            .catch(error => console.error('Erro:', error));

            socket.emit('update_health', {
                character_id: charId,
                new_health: hp,
                status: statusEffect
            });
        });
    });

    // Recebe atualizações em tempo real sobre a saúde dos personagens
    socket.on('health_updated', function(data) {
        const characterForm = document.querySelector(`.character-form[data-char-id="${data.character_id}"]`);
        if (characterForm) {
            const healthInput = characterForm.querySelector('.hp-input');
            healthInput.value = data.new_health;
        }
    });

    // Recebe atualizações em tempo real sobre o status dos personagens
    socket.on('status_updated', function(data) {
        const statusList = document.querySelector(`.character-form[data-char-id="${data.character_id}"] .status-effects ul`);
        statusList.innerHTML = '';
        data.status_effects.forEach(effect => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<img src="${effect.icon_url}" alt="${effect.name}"> ${effect.name}: ${effect.description}`;
            statusList.appendChild(listItem);
        });
    });

    // Recebe notificação quando um novo jogador se junta à sessão
    socket.on('new_player', function(data) {
        const existingPlayer = playerList.querySelector(`.character-form[data-char-id="${data._id}"]`);
        if (existingPlayer) return;

        const newPlayerHTML = `
            <div class="character-card">
                <form method="POST" class="character-form" data-char-id="${data._id}">
                    <input type="hidden" name="char_id" value="${data._id}">
                    <p><strong>${data.name}</strong></p>
                    <label>HP: <input type="number" name="hp" value="${data.hp}" class="hp-input"></label><br>
                    <button type="submit">Atualizar</button>
                </form>
            </div>
        `;

        playerList.insertAdjacentHTML('beforeend', newPlayerHTML);

        // Adiciona o novo formulário à lista de listeners para submissões
        const newForm = playerList.querySelector(`.character-form[data-char-id="${data._id}"]`);
        newForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const charId = newForm.getAttribute('data-char-id');
            const hp = newForm.querySelector('.hp-input').value;

            socket.emit('update_health', {
                character_id: charId,
                new_health: hp
            });
        });
    });

    // Recebe notificação quando um jogador sai da sessão
    socket.on('player_left', function(data) {
        const playerElement = document.querySelector(`.character-form[data-char-id="${data._id}"]`);
        if (playerElement) playerElement.remove();
    });
    
});