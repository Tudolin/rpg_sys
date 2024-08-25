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

    socket.on('connect', function() {
        socket.emit('request_session_sync', { session_id: sessionId });
    });

    socket.on('session_sync', function(data) {
        updatePlayerList(data.characters);
    });

    socket.on('new_player', function(data) {
        addOrUpdatePlayer(data);
    });

    socket.on('player_left', function(data) {
        removePlayerFromList(data._id);
    });

    function updatePlayerList(characters) {
        playerList.innerHTML = ''; // Clear the current list
        
        characters.forEach(char => {
            addOrUpdatePlayer(char);
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

            socket.emit('update_health', {
                character_id: charId,
                new_health: hp
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
    
            // Adiciona o novo formulário à lista de listeners para submissões
            const newForm = playerList.querySelector(`.character-form[data-char-id="${char._id}"]`);
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