document.addEventListener("DOMContentLoaded", () => {
    const socket = io.connect('wss://familyrpg.servebeer.com', {
        transports: ['websocket']
    });

    const mediaForm = document.getElementById('media-form');
    const effectSelects = document.querySelectorAll('.status-effect-select');
    const audioPlayer = document.getElementById('audio-player');
    const musicSelect = document.getElementById('music-select');
    const currentTrackElement = document.getElementById('current-track');
    const playerList = document.querySelector('.characters-container .character-list');
    const addMonsterForm = document.getElementById('add-monster-form');
    const monsterList = document.getElementById('monster-list');

    if (addMonsterForm) {
        addMonsterForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const monsterId = document.getElementById('monster-select').value;
            const quantity = parseInt(document.getElementById('monster-quantity').value);

            if (monsterId && quantity > 0) {
                for (let i = 0; i < quantity; i++) {
                    socket.emit('add_monster', { monster_id: monsterId, session_id: sessionId });
                }
            }
        });
    }

    if (monsterList) {
        document.querySelectorAll('.enemy-card').forEach((monsterCard) => {
            const monsterId = monsterCard.getAttribute('data-monster-id');
            const hpElement = monsterCard.querySelector(`input[name="monster_hp"]`);
            const manaElement = monsterCard.querySelector(`input[name="monster_mana"]`);
            const energiaElement = monsterCard.querySelector(`input[name="monster_energia"]`);

            hpElement?.addEventListener('input', () => updateMonsterStats(monsterId, 'hp', hpElement.value));
            manaElement?.addEventListener('input', () => updateMonsterStats(monsterId, 'mana', manaElement.value));
            energiaElement?.addEventListener('input', () => updateMonsterStats(monsterId, 'energia', energiaElement.value));

            const removeButton = monsterCard.querySelector('.remove-monster-button');
            removeButton?.addEventListener('click', () => removeMonster(monsterId));
        });
    }

    if (playerList) {
        document.querySelectorAll('.character-form').forEach((form) => {
            form.addEventListener('submit', (event) => {
                event.preventDefault();
                const charId = form.getAttribute('data-char-id');
                const hp = form.querySelector('.hp-input').value;
                const mana = form.querySelector('.mana-input').value;
                const energy = form.querySelector('.energy-input').value;

                socket.emit('update_character_status', {
                    character_id: charId,
                    new_health: hp,
                    new_mana: mana,
                    new_energy: energy
                });
            });
        });
    }

    mediaForm?.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(mediaForm);
        const fileInput = document.getElementById('media-input');

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
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Media uploaded successfully!', data.media_url);
                } else {
                    throw new Error('Error uploading media: ' + data.error);
                }
            })
            .catch(error => console.error('Error:', error.message));
    });

    socket.emit('request_master_sync', { session_id: sessionId });

    socket.on('master_sync', (data) => {
        updatePlayersList(data.characters);
        updateMonstersList(data.monsters);
    });

    socket.on('monster_added', (data) => {
        const existingMonster = document.querySelector(`.enemy-card[data-monster-id="${data._id}"]`);
        if (existingMonster) {
            console.log(`Monster with ID ${data._id} already exists. Skipping duplicate render.`);
            return;
        }

        const monsterElement = createMonsterElement(data);
        monsterList.appendChild(monsterElement);
    });

    function createMonsterElement(monster) {
        const monsterElement = document.createElement('li');
        monsterElement.dataset.monsterId = monster._id;
        monsterElement.innerHTML = `
            <div class="enemy-card">
                <img src="${monster.img_url}" alt="${monster.name}" class="monster-image">
                <h4>${monster.name}</h4>
                <p>HP: <span class="monster-hp">${monster.current_hp}</span> / ${monster.hp}</p>
                <button class="remove-monster-button" onclick="removeMonster('${monster._id}')">Remover</button>
            </div>
        `;

        monsterElement.querySelector('.remove-monster-button').addEventListener('click', () => {
            socket.emit('remove_monster', { monster_id: monster._id, session_id: sessionId });
        });

        return monsterElement;
    }

    function removeMonster(monsterId) {
        fetch('/remove_monster', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ monster_id: monsterId })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.querySelector(`.enemy-card[data-monster-id="${monsterId}"]`)?.remove();
                    console.log(`Monster ${monsterId} removed successfully`);
                } else {
                    console.error('Failed to remove monster');
                }
            })
            .catch(error => console.error('Error:', error));
    }

    socket.on('monster_removed', (data) => {
        document.querySelector(`li[data-monster-id="${data._id}"]`)?.remove();
    });

    function updatePlayerList(players) {
        const playersContainer = document.querySelector('.characters-container');
        playersContainer.innerHTML = '';

        players.forEach(player => {
            const playerCard = `
                <div class="character-card" data-player-id="${player._id || ''}">
                    <p><strong>${player.name || 'Unnamed Player'}</strong></p>
                    <form method="POST" class="character-form" data-char-id="${player._id || ''}">
                        <label>HP: <input type="number" name="hp" value="${player.current_hp || 0}" class="hp-input"> / ${player.hp || 0}</label><br>
                        <label>Mana: <input type="number" name="mana" value="${player.current_mana || 0}" class="mana-input"> / ${player.mana || 0}</label><br>
                        <label>Energia: <input type="number" name="energia" value="${player.current_energy || 0}" class="energy-input"> / ${player.energia || 0}</label><br>
                        <button type="submit">Atualizar</button>
                    </form>
                </div>`;
            playersContainer.insertAdjacentHTML('beforeend', playerCard);
        });
    }

    function updateMonsterStats(monsterId, stat, value) {
        fetch('/update_monster_stats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                monster_id: monsterId,
                session_id: sessionId,
                [stat]: value
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log(`Monster ${stat} updated successfully`);
                } else {
                    console.error('Failed to update monster stats:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    function updateMonstersList(monsters) {
        monsters.forEach(monster => {
            const existingMonster = document.querySelector(`.enemy-card[data-monster-id="${monster._id}"]`);
            if (!existingMonster) {
                addMonsterToDOM(monster);
            } else {
                console.log(`Monster with ID ${monster._id} already exists in DOM. Skipping duplicate render.`);
            }
        });
    }

    function addMonsterToDOM(monster) {
        const boardCenter = document.querySelector('.board-center');
        if (boardCenter) {
            const monsterElement = document.createElement('div');
            monsterElement.classList.add('enemy-card');
            monsterElement.dataset.monsterId = monster._id;
            monsterElement.innerHTML = `
                <h4>${monster.name}</h4>
                <img src="${monster.img_url}" alt="${monster.name}" class="monster-image">
                <div class="health-bar">
                    <div class="health-fill" style="width: ${(monster.current_hp / monster.hp) * 100}%"></div>
                    <div class="health-text">HP: ${monster.current_hp} / ${monster.hp}</div>
                </div>
                <p>${monster.resumo}</p>
                <button class="remove-monster-button" data-monster-id="${monster._id}">Remover</button>
            `;
            boardCenter.appendChild(monsterElement);
        } else {
            console.error('Elemento board-center não encontrado no DOM.');
        }
    }

    socket.on('connect', () => {
        console.log('Connected to the server, requesting session sync...');
        socket.emit('request_session_sync', { session_id: sessionId });
    });

    socket.on('session_sync', (data) => {
        if (data && data.characters && data.characters.length > 0) {
            updatePlayerList(data.characters);
        } else {
            console.warn('No characters found in session sync data.');
        }
    });

    socket.on('mana_energy_updated_master', (data) => {
        const playerElement = document.querySelector(`.character-form[data-char-id="${data.character_id}"]`);
        if (playerElement) {
            const manaField = playerElement.querySelector('.mana-input');
            const energyField = playerElement.querySelector('.energy-input');

            if (manaField) manaField.value = data.current_mana;
            if (energyField) energyField.value = data.current_energy;
        }
    });

    socket.on('new_player', (data) => addOrUpdatePlayer(data));

    socket.on('player_left', (data) => {
        const playerElement = document.querySelector(`div[data-player-id="${data._id}"]`);
        playerElement?.remove();
    });

    function addOrUpdatePlayer(char) {
        const existingPlayer = playerList.querySelector(`.character-form[data-char-id="${char._id}"]`);

        if (existingPlayer) {
            updatePlayerElement(existingPlayer, char);
        } else {
            createPlayerElement(char);
        }
    }

    function updatePlayerElement(element, char) {
        const hpInput = element.querySelector('.hp-input');
        hpInput.value = char.hp;
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
            </div>`;
        playerList.insertAdjacentHTML('beforeend', newPlayerHTML);

        const newForm = playerList.querySelector(`.character-form[data-char-id="${char._id}"]`);
        newForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const charId = newForm.getAttribute('data-char-id');
            const hp = newForm.querySelector('.hp-input').value;
            const mana = newForm.querySelector('.mana-input').value;
            const energy = newForm.querySelector('.energy-input').value;

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
        playerElement?.remove();
    }

    socket.on('mana_energy_updated', (data) => {
        const characterForm = document.querySelector(`.character-form[data-char-id="${data.character_id}"]`);
        if (characterForm) {
            const manaInput = characterForm.querySelector('.mana-input');
            const energyInput = characterForm.querySelector('.energy-input');

            if (manaInput) manaInput.value = data.current_mana;
            if (energyInput) energyInput.value = data.current_energy;
        }
    });

    socket.on('health_updated', (data) => {
        const characterForm = document.querySelector(`.character-form[data-char-id="${data.character_id}"]`);
        if (characterForm) {
            const healthInput = characterForm.querySelector('.hp-input');
            healthInput.value = data.new_health;
        }
    });

    socket.on('status_updated', (data) => {
        const statusList = document.querySelector(`.character-form[data-char-id="${data.character_id}"] .status-effects ul`);
        statusList.innerHTML = '';
        data.status_effects.forEach(effect => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<img src="${effect.icon_url}" alt="${effect.name}"> ${effect.name}: ${effect.description}`;
            statusList.appendChild(listItem);
        });
    });

    socket.on('play_music', (data) => {
        if (audioPlayer.src !== data.track_url) {
            audioPlayer.src = data.track_url;
            audioPlayer.play();
            currentTrackElement.textContent = `Reproduzindo: ${data.track_url.split('/').pop().split('.').slice(0, -1).join('.')}`;
            saveMusicState();
        }
    });

    socket.on('stop_music', () => {
        audioPlayer.pause();
        audioPlayer.src = '';
        currentTrackElement.textContent = 'Nenhuma música em reprodução';
        localStorage.removeItem('musicPlayerState');
    });

    effectSelects.forEach(select => {
        select.addEventListener('change', function () {
            const selectedOption = this.options[this.selectedIndex];
            const description = selectedOption.getAttribute('data-description');
            const descriptionElement = this.parentNode.querySelector('.effect-description');
            descriptionElement.textContent = description || '';
        });
    });

    document.getElementById('play-button').addEventListener('click', () => {
        const selectedTrack = musicSelect.value;

        if (selectedTrack && audioPlayer.src !== selectedTrack) {
            audioPlayer.src = selectedTrack;
            audioPlayer.play();

            const selectedOption = document.querySelector(`#music-select option[value="${selectedTrack}"]`);
            currentTrackElement.textContent = `Reproduzindo: ${selectedOption.textContent}`;

            fetch('/play_music', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ track_url: selectedTrack }),
            });

            saveMusicState();
        }
    });

    document.getElementById('stop-button').addEventListener('click', () => {
        audioPlayer.pause();
        audioPlayer.src = '';
        currentTrackElement.textContent = 'Nenhuma música em reprodução';
        localStorage.removeItem('musicPlayerState');

        fetch('/stop_music', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
    });

    window.addEventListener('beforeunload', saveMusicState);
    window.addEventListener('unload', saveMusicState);

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
});
