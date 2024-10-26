// Função para carregar o conteúdo do arquivo data.json
function loadData() {
    return fetch('data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar o arquivo JSON');
            }
            return response.json();
        })
        .catch(error => console.error('Erro:', error));
}


function populateCargoOptions(data) {
    const cargoSelect = document.getElementById('cargo');
    const uniqueCargos = [...new Set(data.map(item => item.cargo))]; 
    
    uniqueCargos.forEach(cargo => {
        const option = document.createElement('option');
        option.value = cargo;
        option.textContent = cargo;
        cargoSelect.appendChild(option);
    });
}

// Função para exibir as questões
function displayQuestions(selectedData) {
    const questionContainer = document.getElementById('question-container');
    questionContainer.innerHTML = ''; 

    selectedData.forEach((item, index) => {
        const card = document.createElement('div');
        card.classList.add('card', 'question-card');
        card.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">${item.cargo} </h5>
                <p class="question-text">${index + 1}. ${item.questão}</p>
                <div class="options">
                    ${Object.keys(item.alternativas).map(letter => `
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="question-${index}" id="question-${index}-${letter}" value="${letter}">
                            <label class="form-check-label" for="question-${index}-${letter}">
                                ${letter}: ${item.alternativas[letter]}
                            </label>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        questionContainer.appendChild(card);
    });
    
    document.getElementById('submit-btn').style.display = 'block'; 
}


document.getElementById('simulado-form').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const selectedCargo = document.getElementById('cargo').value;
    const numeroQuestoes = parseInt(document.getElementById('numero-questoes').value);


    loadData().then(data => {
        const filteredData = data.filter(item => item.cargo === selectedCargo);
        
    
        const selectedQuestions = [];
        for (let i = 0; i < Math.min(numeroQuestoes, filteredData.length); i++) {
            const randomIndex = Math.floor(Math.random() * filteredData.length);
            selectedQuestions.push(filteredData[randomIndex]);
            filteredData.splice(randomIndex, 1); 
        }

        displayQuestions(selectedQuestions); 
    });
});


document.addEventListener('DOMContentLoaded', () => {
    loadData().then(data => {
        populateCargoOptions(data); 
    });
});
