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

                // Verifique se class_habilidades e race_habilidades são arrays
                const classHabilidades = Array.isArray(data.class_habilidades) ? data.class_habilidades : [];
                const raceHabilidades = Array.isArray(data.race_habilidades) ? data.race_habilidades : [];

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
                            ${classHabilidades.map(hab => `<li>${hab}</li>`).join('')}
                            ${raceHabilidades.map(hab => `<li>${hab}</li>`).join('')}
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

                    // Verifique se class_habilidades e race_habilidades são arrays
                    const classHabilidades = Array.isArray(data.class_habilidades) ? data.class_habilidades : [];
                    const raceHabilidades = Array.isArray(data.race_habilidades) ? data.race_habilidades : [];

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
                                ${classHabilidades.map(hab => `<li>${hab}</li>`).join('')}
                                ${raceHabilidades.map(hab => `<li>${hab}</li>`).join('')}
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
