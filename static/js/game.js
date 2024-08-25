document.addEventListener("DOMContentLoaded", function () {
    const profileButton = document.getElementById("profile-button");
    const profilePopup = document.getElementById("profile-popup");
    const otherPlayerPopup = document.getElementById("other-player-popup");
    const closeButtons = document.querySelectorAll(".close-button");
    const rollDiceButton = document.getElementById("roll-dice-button");
    const diceResult = document.getElementById("dice-result");
    const socket = io.connect('wss://familyrpg.servebeer.com', {
        transports: ['websocket']
    });

    window.addEventListener('beforeunload', function (e) {
        const confirmationMessage = 'Você tem certeza que deseja sair do lobby? Isso pode causar a perda de progresso.';
        e.returnValue = confirmationMessage; // Standard for most browsers
        return confirmationMessage; // For some other browsers
    });

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
    
                const habilidades = data.habilidades ? Object.entries(data.habilidades) : [];
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
                    <p><strong>Raca:</strong> ${data.race_name}</p>
                    <div class="attributes">
                        <p><strong>Atributos:</strong></p>
                        <ul>
                            <li>Forca: ${data.forca}</li>
                            <li>Destreza: ${data.destreza}</li>
                            <li>Constituicão: ${data.constituicao}</li>
                            <li>Inteligência: ${data.inteligencia}</li>
                            <li>Sabedoria: ${data.sabedoria}</li>
                            <li>Carisma: ${data.carisma}</li>
                        </ul>
                    </div>
                    <div class="skills">
                        <p><strong>Habilidades:</strong></p>
                        <ul>
                            ${habilidades.map(([nome, descricao]) => `<li>${nome}: ${descricao}</li>`).join('')}
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

    // Função para adicionar evento de clique ao perfil de um jogador
    function attachPlayerClickEvent(playerElement) {
        playerElement.addEventListener("click", function () {
            const playerId = this.getAttribute("data-player-id");
            fetch(`/get_player_details/${playerId}`)
                .then(response => response.json())
                .then(data => {
                    const detailsContainer = document.getElementById("other-player-details");
    
                    const habilidades = data.habilidades ? Object.entries(data.habilidades) : [];
                    const pericias = data.pericias ? Object.entries(data.pericias) : [];
    
                    // Verificação para garantir que img_url não seja undefined ou vazio
                    const imgUrl = data.img_url ? data.img_url : '/static/images/default.png';
    
                    detailsContainer.innerHTML = `
                        <div class="profile-header">
                        <div class="profile-image">
                            <img src="${data.img_url}" alt="${data.name}" class="character-portrait-popup">
                        </div>
                        <h2>${data.name}</h2>
                    </div>
                        <p><strong>Classe:</strong> ${data.class_name}</p>
                        <p><strong>Raca:</strong> ${data.race_name}</p>
                        <div class="attributes">
                            <p><strong>Atributos:</strong></p>
                            <ul>
                                <li>Forca: ${data.forca}</li>
                                <li>Destreza: ${data.destreza}</li>
                                <li>Constituicão: ${data.constituicao}</li>
                                <li>Inteligência: ${data.inteligencia}</li>
                                <li>Sabedoria: ${data.sabedoria}</li>
                                <li>Carisma: ${data.carisma}</li>
                            </ul>
                        </div>
                        <div class="skills">
                            <p><strong>Habilidades:</strong></p>
                            <ul>
                                ${habilidades.map(([nome, descricao]) => `<li>${nome}: ${descricao}</li>`).join('')}
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

    socket.on('session_sync', function(data) {
        const playerList = document.querySelector('.other-players ul');
        playerList.innerHTML = ''; // Limpa a lista existente
    
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
                        <p>Raca: ${char.race_name}</p>
                        <p>HP: ${char.hp}</p>
                    </div>
                </li>
            `;
            playerList.insertAdjacentHTML('beforeend', newPlayerHTML);
            // Re-anexar eventos de clique
            attachPlayerClickEvent(playerList.querySelector(`.other-player[data-player-id="${char._id}"]`));
        });
    });
    

    socket.on('new_player', function (data) {
        console.log('New player joined:', data);  // Log de depuração
        console.log('New media received:', data);
        const img = document.createElement('img');
        img.src = data.media_url;
        img.alt = 'New media';
        document.getElementById('media-container').appendChild(img);
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
                    <p>Raca: ${data.race_name}</p>
                    <p>HP: ${data.hp}</p>
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
        player.src = data.track_url; // Set the source of the music to be played
        player.play(); // Start playing the music
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
