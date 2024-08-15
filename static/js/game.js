document.addEventListener("DOMContentLoaded", function() {
    const profileButton = document.getElementById("profile-button");
    const profilePopup = document.getElementById("profile-popup");
    const closeButtons = document.querySelectorAll(".close-button");

    profileButton.addEventListener("click", function() {
        // Faz a requisição para obter os detalhes do jogador atual
        fetch('/get_current_player_details')
            .then(response => response.json())
            .then(data => {
                console.log("Received current player data:", data);

                const detailsContainer = document.querySelector("#profile-popup .popup-content");

                // Habilidades
                const habilidades = data.habilidades ? Object.entries(data.habilidades) : [];
                // Perícias
                const pericias = data.pericias ? Object.entries(data.pericias) : [];

                detailsContainer.innerHTML = `
                    <span class="close-button">&times;</span>
                    <h2>${data.name}</h2>
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
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    closeButtons.forEach(button => {
        button.addEventListener("click", function() {
            profilePopup.style.display = "none";
            document.getElementById("other-player-popup").style.display = "none";
        });
    });

    const otherPlayers = document.querySelectorAll(".other-player");

    otherPlayers.forEach(player => {
        player.addEventListener("click", function() {
            const playerId = this.getAttribute("data-player-id");

            fetch(`/get_player_details/${playerId}`)
                .then(response => response.json())
                .then(data => {
                    console.log("Received player data:", data);

                    const otherPlayerPopup = document.getElementById("other-player-popup");
                    const detailsContainer = document.getElementById("other-player-details");

                    // Habilidades
                    const habilidades = data.habilidades ? Object.entries(data.habilidades) : [];
                    // Perícias
                    const pericias = data.pericias ? Object.entries(data.pericias) : [];

                    detailsContainer.innerHTML = `
                        <h2>${data.name}</h2>
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
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });

    window.onclick = function(event) {
        if (event.target == profilePopup) {
            profilePopup.style.display = "none";
        } else if (event.target == document.getElementById("other-player-popup")) {
            document.getElementById("other-player-popup").style.display = "none";
        }
    };
});
