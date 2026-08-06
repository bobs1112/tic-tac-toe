function AddButton(id){
    const link = document.createElement('a');
    const ButtonGame = document.createElement('button')
    
    link.href = window.location.href + `start_game/${id}`;

    ButtonGame.textContent = `зайти в игру: ${id}`;
    ButtonGame.className = "button"

    link.append(ButtonGame);
    document.querySelector('#games').append(link);
}
async function updategame() {
        setTimeout(async function() {
            const CurrUrl = window.location.href
            const urlg = CurrUrl + `games`;
            try {
                const response = await fetch(urlg);
                if (!response.ok) {
                    throw new Error(`Response status: ${response.status}`);
                }
                document.querySelector('#games').textContent = '';
                // здесь тоже json
                json = await response.json();
                for (let i = 1; i <=json.lenght; i++) {
                    AddButton(i);
                }
                //await update();
                
            } catch (error) {
                console.error(error.message);
            }
            if (json.lenght >0){
                document.getElementById('h').style.display = 'none';
            }
            updategame();
    }, 1000);
}
updategame()