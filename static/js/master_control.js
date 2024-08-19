document.addEventListener("DOMContentLoaded", function() {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    const effectSelects = document.querySelectorAll('.status-effect-select');
    const audioPlayer = document.getElementById('audio-player');
    const forms = document.querySelectorAll(`.character-form[data-session-id="${sessionId}"]`);

    // Atualiza a descrição dos efeitos selecionados
    effectSelects.forEach(select => {
        select.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const description = selectedOption.getAttribute('data-description');
            const descriptionElement = this.parentNode.querySelector('.effect-description');
            
            descriptionElement.textContent = description ? description : '';
        });
    });

    // Carrega as faixas de música
    fetch('/music_tracks')
        .then(response => response.json())
        .then(tracks => {
            const musicSelect = document.getElementById('music-select');
            musicSelect.innerHTML = '';
            tracks.forEach(track => {
                const option = document.createElement('option');
                option.value = track.url;
                option.textContent = track.name;
                musicSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Erro ao carregar músicas:', error));

    // Listener para o botão de tocar música
    document.getElementById('play-button').addEventListener('click', function () {
        const selectedTrack = document.getElementById('music-select').value;
        
        if (selectedTrack && audioPlayer.src !== selectedTrack) { // Apenas altere se a faixa for diferente da atual
            audioPlayer.src = selectedTrack;
            audioPlayer.play();
    
            // Atualiza o nome da faixa em reprodução
            const selectedOption = document.querySelector(`#music-select option[value="${selectedTrack}"]`);
            document.getElementById('current-track').textContent = `Reproduzindo: ${selectedOption.textContent}`;
    
            // Envia o evento de tocar música para os outros clientes
            fetch('/play_music', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ track_url: selectedTrack }),
            });
        }
    });

    // Listener para o botão de parar música
    document.getElementById('stop-button').addEventListener('click', function () {
        audioPlayer.pause();
        audioPlayer.src = '';

        // Atualiza o nome da faixa em reprodução
        document.getElementById('current-track').textContent = 'Nenhuma música em reprodução';

        fetch('/stop_music', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
    });

    // Reproduz música enviada pelos sockets
    socket.on('play_music', function(data) {
        if (audioPlayer.src !== data.track_url) { // Evita reiniciar a música se a faixa já estiver tocando
            audioPlayer.src = data.track_url;
            audioPlayer.play();
    
            // Atualiza o nome da faixa em reprodução
            document.getElementById('current-track').textContent = `Reproduzindo: ${data.track_url.split('/').pop().split('.').slice(0, -1).join('.')}`;
        }
    });

    // Para a música pelos sockets
    socket.on('stop_music', function() {
        audioPlayer.pause();
        audioPlayer.src = '';

        // Atualiza o nome da faixa em reprodução
        document.getElementById('current-track').textContent = 'Nenhuma música em reprodução';
    });

    // Itera sobre cada formulário e lida com submissão
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
        const playerList = document.querySelector('.characters-container');
        const existingPlayer = playerList.querySelector(`.character-form[data-char-id="${data._id}"]`);
        if (existingPlayer) return;

        const newPlayerHTML = `
            <div class="character-card">
                <form method="POST" class="character-form" data-char-id="${data._id}">
                    <input type="hidden" name="char_id" value="${data._id}">
                    <p><strong>${data.name}</strong></p>
                    <label>HP: <input type="number" name="hp" value="${data.hp}" class="hp-input"></label><br>
                    <label>Status: <input type="text" name="status" value="" class="status-input"></label><br>
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
            const status = newForm.querySelector('.status-input').value;

            socket.emit('update_health', {
                character_id: charId,
                new_health: hp,
                status: status
            });
        });
    });

    // Recebe notificação quando um jogador sai da sessão
    socket.on('player_left', function(data) {
        const characterForm = document.querySelector(`.character-form[data-char-id="${data._id}"]`);
        if (characterForm) {
            characterForm.remove(); // Remove o formulário do personagem desconectado
        }
    });
});
