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
    const gridContainer = document.querySelector('.grid-container');
    initializeDragAndDrop(gridContainer);
    
    if (addMonsterForm) {
        addMonsterForm.addEventListener('submit', function(event) {
            event.preventDefault();
    
            const monsterId = document.getElementById('monster-select').value;
            const quantity = parseInt(document.getElementById('monster-quantity').value);
    
            if (monsterId && quantity > 0) {
                for (let i = 0; i < quantity; i++) {
                    fetch('/add_monster_to_session', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            session_id: sessionId,
                            monster_id: monsterId,
                            quantity: 1,
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log(data.monster); // Log to verify the monster object
                            if (data.monster) {
                                addMonsterToDOM(data.monster);
                                window.location.reload();
                            } else {
                                console.error("No monster data received");
                            }
                            socket.emit('request_session_sync', { session_id: sessionId });
                        } else {
                            console.error('Error adding monster:', data.message);
                        }
                    })
                    .catch(error => console.error('Erro:', error));
                }
            }
        });
    }
    

    if (monsterList) {
        document.querySelectorAll('.enemy-card').forEach(function (monsterCard) {
            const monsterId = monsterCard.getAttribute('data-monster-id');

            const hpElement = monsterCard.querySelector(`input[name="monster_hp"]`);
            const manaElement = monsterCard.querySelector(`input[name="monster_mana"]`);
            const energiaElement = monsterCard.querySelector(`input[name="monster_energia"]`);

            if (hpElement) {
                hpElement.addEventListener('input', function () {
                    updateMonsterStats(monsterId, 'hp', hpElement.value);
                });
            }

            if (manaElement) {
                manaElement.addEventListener('input', function () {
                    updateMonsterStats(monsterId, 'mana', manaElement.value);
                });
            }

            if (energiaElement) {
                energiaElement.addEventListener('input', function () {
                    updateMonsterStats(monsterId, 'energia', energiaElement.value);
                });
            }

            const removeButton = monsterCard.querySelector('.remove-monster-button');
            if (removeButton) {
                removeButton.addEventListener('click', function () {
                    removeMonster(monsterId);
                });
            }
        });
    }

    if (playerList) {
        const forms = document.querySelectorAll('.character-form');
        forms.forEach(function (form) {
            form.addEventListener('submit', function (event) {
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

    if (mediaForm) {
        mediaForm.addEventListener('submit', function(event) {
            event.preventDefault();
        });
    }

    socket.emit('request_master_sync', { session_id: sessionId });

    socket.on('master_sync', function(data) {
        updatePlayersList(data.characters);
        updateMonstersList(data.monsters);
    });

    socket.on('monster_added', function(data) {
        // Check if the monster already exists in the DOM
        let existingMonster = document.querySelector(`.enemy-card[data-monster-id="${data._id}"]`);
        if (existingMonster) {
            console.log(`Monster with ID ${data._id} already exists. Skipping duplicate render.`);
            return;
        }
        
        const form = monsterElement.querySelector('.monster-form');
        if (form) {
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
        }
    

        monsterElement.querySelector('.remove-monster-button').addEventListener('click', function() {
            const monsterId = this.getAttribute('data-monster-id');
            console.log(`Attempting to remove monster with ID: ${monsterId}`);
            socket.emit('remove_monster', { monster_id: monsterId, session_id: sessionId });
        });
    });

    function initializeDragAndDrop() {
        const pawns = document.querySelectorAll('.pawn');
        const cells = document.querySelectorAll('#grid-table td');
    
        pawns.forEach(pawn => {
            pawn.setAttribute('draggable', true);
            pawn.addEventListener('dragstart', handleDragStart, false);
            pawn.addEventListener('dragend', handleDragEnd, false);
        });
    
        cells.forEach(cell => {
            cell.addEventListener('dragover', handleDragOver, false);
            cell.addEventListener('drop', handleDrop, false);
            cell.addEventListener('dragenter', handleDragEnter, false);
            cell.addEventListener('dragleave', handleDragLeave, false);
        });
    }
    
    function handleDragStart(e) {
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', this.id); // Pass the pawn's ID
        this.classList.add('dragging');
    }
    
    function handleDragOver(e) {
        if (e.preventDefault) {
            e.preventDefault(); // Necessary for allowing drops
        }
        e.dataTransfer.dropEffect = 'move';
        return false;
    }
    
    function handleDragEnter(e) {
        this.classList.add('over');
    }
    
    function handleDragLeave(e) {
        this.classList.remove('over');
    }
    
    function handleDrop(e) {
        if (e.stopPropagation) {
            e.stopPropagation(); // Stop the browser from redirecting
        }
    
        const draggedId = e.dataTransfer.getData('text/plain');
        const pawn = document.getElementById(draggedId);
        this.appendChild(pawn); // Append the pawn to the new cell
    
        const rowIndex = this.parentNode.rowIndex;
        const colIndex = this.cellIndex;
        
        updatePawnPositionOnServer(draggedId, rowIndex, colIndex);
    
        return false;
    }
    
    function handleDragEnd(e) {
        // Remove dragging styles
        this.classList.remove('dragging');
        const cells = document.querySelectorAll('.grid-container td');
        cells.forEach(cell => {
            cell.classList.remove('over');
        });
    }
    
    function updatePawnPositionOnServer(pawnId, x, y) {
        // Emit socket event to update the position on the server
        socket.emit('update_pawn_position', { pawnId, x, y });
    }

    function removeMonster(monsterId) {
        // Ensure sessionId is defined and valid before making the request
        if (!sessionId) {
            console.error('No session ID available');
            return;
        }
    
        // Perform a single fetch call to remove the monster
        fetch('/remove_monster', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                monster_id: monsterId,
                session_id: sessionId // Ensure session_id is passed
            })
        })
        .then(response => {
            if (!response.ok) {
                console.error(`Failed to remove monster: ${response.statusText}`);
                throw new Error('Failed to remove monster');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const monsterElement = document.querySelector(`li[data-monster-id="${monsterId}"]`);
                if (monsterElement) {
                    monsterElement.remove();
                    console.log(`Monster ${monsterId} removed successfully`);
                }
            } else {
                console.error('Failed to remove monster:', data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    // Add event listener to remove buttons
    document.querySelectorAll('.remove-monster-button').forEach(button => {
        button.addEventListener('click', function() {
            const monsterId = this.getAttribute('data-monster-id');
    
            // Check that monsterId and sessionId are valid before calling removeMonster
            if (monsterId && sessionId) {
                removeMonster(monsterId);
            } else {
                console.error('Invalid monster ID or session ID');
            }
        });
    });
    
    document.querySelectorAll('.remove-monster-button').forEach(button => {
        button.addEventListener('click', function() {
            const monsterId = this.getAttribute('data-monster-id');
            
            // Ensure `sessionId` and `monsterId` are valid before making the request
            console.log("Removing monster with ID:", monsterId);
            console.log("Session ID:", sessionId);
            
            fetch('/remove_monster', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    monster_id: monsterId,
                    session_id: sessionId // Ensure session_id is valid
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Remove the monster from the DOM if the backend confirms success
                    const monsterElement = document.querySelector(`li[data-monster-id="${monsterId}"]`);
                    if (monsterElement) {
                        monsterElement.remove();
                    }
                } else {
                    console.error('Failed to remove monster:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });    

    
    document.querySelectorAll('.enemy-card').forEach(function (monsterCard) {
        const monsterId = monsterCard.getAttribute('data-monster-id');
    
        const hpElement = monsterCard.querySelector(`input[name="monster_hp"]`);
        const manaElement = monsterCard.querySelector(`input[name="monster_mana"]`);
        const energiaElement = monsterCard.querySelector(`input[name="monster_energia"]`);
    
        if (hpElement) {
            hpElement.addEventListener('input', function () {
                updateMonsterStats(monsterId, 'hp', hpElement.value);
            });
        } else {
            console.warn(`hpElement for monster ${monsterId} not found.`);
        }
    
        if (manaElement) {
            manaElement.addEventListener('input', function () {
                updateMonsterStats(monsterId, 'mana', manaElement.value);
            });
        }
    
        if (energiaElement) {
            energiaElement.addEventListener('input', function () {
                updateMonsterStats(monsterId, 'energia', energiaElement.value);
            });
        }
    
        const removeButton = monsterCard.querySelector('.remove-monster-button');
        if (removeButton) {
            removeButton.addEventListener('click', function () {
                removeMonster(monsterId);
            });
        }
    });
    
    socket.on('monster_hp_updated', function(data) {
        const monsterElement = document.querySelector(`.enemy-card[data-monster-id="${data.monster_id}"]`);
        if (monsterElement) {
            const hpElement = monsterElement.querySelector('.monster-hp');
            hpElement.textContent = `HP: ${data.current_hp} / ${data.hp}`;
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
    
        if (data && data.monsters && data.monsters.length > 0) {
            updateMonstersList(data.monsters);
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

    socket.on('new_player_added', function(playerData) {
        const gridTable = document.getElementById('grid-table');
        const newRow = gridTable.insertRow(-1);
        const newCell = newRow.insertCell(0);
        newCell.innerHTML = `<div id="pawn-${playerData._id}" class="pawn" style="background-image:url('${playerData.img_url}');"></div>`;
        initializeDragAndDrop();
    });
    
    socket.on('player_left', function(playerId) {
        const pawnToRemove = document.getElementById(`pawn-${playerId}`);
        if (pawnToRemove) {
            pawnToRemove.parentNode.removeChild(pawnToRemove);
        }
    });

    
    socket.on('player_left', function(data) {
        const playerElement = document.querySelector(`div[data-player-id="${data._id}"]`);
        if (playerElement) {
            playerElement.remove();
        }
    });

    function updatePlayerList(players) {
        const playersContainer = document.querySelector('.characters-container');
        if (!playersContainer) {
            console.error("Unable to find the players container element");
            return;
        }
    
        playersContainer.innerHTML = ''; // Clear existing players list
    
        if (!Array.isArray(players) || players.length === 0) {
            console.log("No players data provided or empty players array");
            return;
        }
    
        players.forEach(player => {
            if (!player) {
                console.error("Undefined player data found");
                return;
            }
    
            const playerCard = `
            <div class="character-card" data-player-id="${player._id || ''}">
                <p><strong>${player.name || 'Unnamed Player'}</strong></p>
                <form method="POST" class="character-form" data-char-id="${player._id || ''}">
                    <input type="hidden" name="char_id" value="${player._id || ''}">
                    <label>HP: <input type="number" name="hp" value="${player.current_hp || 0}" class="hp-input"> / ${player.hp || 0}</label><br>
                    <label>Mana: <input type="number" name="mana" value="${player.current_mana || 0}" class="mana-input"> / ${player.mana || 0}</label><br>
                    <label>Energia: <input type="number" name="energia" value="${player.current_energia || 0}" class="energy-input"> / ${player.energia || 0}</label><br>
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
                session_id: sessionId,  // Adicione o session_id aqui
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
                    <label>Energia: <input type="number" name="energia" value="${player.current_energia}" class="energy-input"> / ${player.energia}</label><br>
                    <button type="submit">Atualizar</button>
                </form>
            </div>`;
            playersContainer.insertAdjacentHTML('beforeend', playerCard);
        });
    }

    function updateMonstersList(monsters) {
        monsters.forEach(monster => {
            let existingMonster = document.querySelector(`.enemy-card[data-monster-id="${monster._id}"]`);
            if (!existingMonster) {
                addMonsterToDOM(monster);
            } else {
                console.log(`Monster with ID ${monster._id} already exists in DOM. Skipping duplicate render.`);
            }
        });
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
    
    function addMonsterToDOM(monster) {
        const monsterList = document.getElementById('monster-list');
        
        console.log(monster);
        const monsterElement = document.createElement('li');
        monsterElement.classList.add('enemy-card');
        monsterElement.setAttribute('data-monster-id', monster._id);
    
        monsterElement.innerHTML = `
            <h4>${monster.name}</h4>
            <img src="${monster.img_url}" alt="${monster.name}" class="monster-image">
            <form method="POST" class="monster-form" data-monster-id="${monster._id}">
                <input type="hidden" name="monster_id" value="${monster._id}">
                <label>HP: <input type="number" name="monster_hp" value="${monster.current_hp}" class="hp-input"> / ${monster.hp}</label><br>
                <button type="submit">Atualizar</button>
            </form>
            <p>${monster.resumo}</p>
            <button class="remove-monster-button" data-monster-id="${monster._id}">Remover</button>
        `;
    
        // Append the new monster to the list
        monsterList.appendChild(monsterElement);
    
        // Add event listeners for the newly created monster element
        const removeButton = monsterElement.querySelector('.remove-monster-button');
        removeButton.addEventListener('click', function () {
            removeMonster(monster._id);
        });
    
        const form = monsterElement.querySelector('.monster-form');
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const newHp = form.querySelector('.hp-input').value;
            socket.emit('update_monster_hp', {
                monster_id: monster._id,
                new_hp: newHp,
                session_id: sessionId
            });
        });
    }
    

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
                    <label>Energia: <input type="number" name="energia" value="${char.current_energia}" class="energy-input"></label><br>
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

    socket.on('mana_energy_updated', function(data) {
        const characterForm = document.querySelector(`.character-form[data-char-id="${data.character_id}"]`);
        if (characterForm) {
            const manaInput = characterForm.querySelector('.mana-input');
            const energyInput = characterForm.querySelector('.energy-input');
            
            if (manaInput) manaInput.value = data.current_mana;
            if (energyInput) energyInput.value = data.current_energia;
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
    
    document.querySelectorAll('.monster-form').forEach(function (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const monsterId = form.getAttribute('data-monster-id');
            const formData = new FormData(form);

            fetch('/update_monster_stats', {
                method: 'POST',
                body: JSON.stringify({
                    monster_id: monsterId,
                    hp: formData.get('monster_hp'),
                    mana: formData.get('monster_mana'),
                    energia: formData.get('monster_energia')
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Monstro atualizado com sucesso!");
                } else {
                    alert("Erro ao atualizar o monstro.");
                }
            });
        });
    });

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