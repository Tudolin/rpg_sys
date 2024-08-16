document.addEventListener("DOMContentLoaded", function() {
    const characterForms = document.querySelectorAll('.character-form');
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Carrega as faixas de música
    fetch('/music_tracks')
        .then(response => response.json())
        .then(tracks => {
            const musicSelect = document.getElementById('music-select');
            musicSelect.innerHTML = ''; // Limpa as opções existentes
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
        if (selectedTrack) {
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
        fetch('/stop_music', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
    });

    characterForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const charId = form.getAttribute('data-char-id');
            const hp = form.querySelector('.hp-input').value;
            const status = form.querySelector('.status-input').value;

            // Emite um evento via Socket.IO para atualizar o personagem
            socket.emit('update_health', {
                character_id: charId,
                new_health: hp,
                status: status
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
        const characterForm = document.querySelector(`.character-form[data-char-id="${data.character_id}"]`);
        if (characterForm) {
            const statusInput = characterForm.querySelector('.status-input');
            statusInput.value = data.status;
        }
    });

    // Recebe notificação quando um novo jogador se junta à sessão
    socket.on('new_player', function(data) {
        const playerList = document.querySelector('.characters-container');

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

    // Recebe comando para tocar música
    socket.on('play_music', function (data) {
        const audioElement = document.getElementById('background-music');
        audioElement.src = data.track_url;
        audioElement.play();
    });

    // Recebe comando para parar música
    socket.on('stop_music', function () {
        const audioElement = document.getElementById('background-music');
        audioElement.pause();
        audioElement.src = '';
    });
});
