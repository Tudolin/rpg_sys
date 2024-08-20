document.addEventListener("DOMContentLoaded", function () {
    const profileButton = document.getElementById("profile-button");
    const profilePopup = document.getElementById("profile-popup");
    const otherPlayerPopup = document.getElementById("other-player-popup");
    const closeButtons = document.querySelectorAll(".close-button");

    window.addEventListener('beforeunload', function (e) {
        const confirmationMessage = 'Você tem certeza que deseja sair do lobby? Isso pode causar a perda de progresso.';
        
        (e || window.event).returnValue = confirmationMessage; // Standard for most browsers
        return confirmationMessage; // For some other browsers
    });
    
    profileButton.addEventListener("click", function () {
        fetch('/get_current_player_details')
            .then(response => response.json())
            .then(data => {
                const detailsContainer = document.querySelector("#profile-popup .popup-content");

                const habilidades = data.habilidades ? Object.entries(data.habilidades) : [];
                const pericias = data.pericias ? Object.entries(data.pericias) : [];

                detailsContainer.innerHTML = `
                    <span class="close-button">&times;</span>
                    <div class="profile-header">
                        <div class="profile-image">
                            <img src="${data.img_url}" alt="${data.name}" class="character-portrait-popup">
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

                    detailsContainer.innerHTML = `
                        <div class="profile-header">
                            <div class="profile-image">
                                <img src="${data.img_url}" alt="${data.name}" class="character-portrait-popup">
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

    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', function () {
        socket.emit('join', { data: 'Player joined!' });
    });

    socket.on('new_player', function (data) {
        console.log('New player joined:', data);  // Log de depuração
        const playerList = document.querySelector('.other-players ul');
        const existingPlayer = document.querySelector(`.other-player[data-player-id="${data._id}"]`);
        if (existingPlayer) return;
    
        const newPlayerHTML = `
            <li class="other-player" data-player-id="${data._id}">
                <div class="character-frame-small">
                    <img src="${data.img_url}" alt="${data.name}" class="character-portrait-small">
                </div>
                <div class="player-stats">
                    <p>${data.name}</p>
                    <p>Classe: ${data.class_name}</p>
                    <p>Raça: ${data.race_name}</p>
                    <p>HP: ${data.hp}</p>
                </div>
            </li>
        `;
        playerList.insertAdjacentHTML('beforeend', newPlayerHTML);

        // Adiciona o evento de clique ao novo jogador adicionado
        const newPlayerElement = playerList.querySelector(`.other-player[data-player-id="${data._id}"]`);
        attachPlayerClickEvent(newPlayerElement);
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