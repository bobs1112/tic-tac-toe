// js 
function AddButton(id, state){
    const link = document.createElement('a');
    const ButtonGame = document.createElement('button')
    link.href = window.location.href + `start_game/${id}`;
    if (state == "нолики выиграли" || state == "крестики выиграли" || state == "Нолики вышли по времени" || state == "Крестики вышли по времени"){
        return;
        //ButtonGame.disabled = true;
    }
    ButtonGame.textContent = `зайти в игру: ${id}`;
    if (state == "Крестики делают ход" || state == "Нолики делают ход"){
        ButtonGame.textContent = `наблюдать за игрой: ${id}`;
    }
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
                json.keys.forEach((element, index) => {
                    if (element.index != 0){
                        document.getElementById('h').style.display = 'none';
                    };
                    AddButton(element.index, element.state)
                });
                //for (let i = 1; i <=json.lenght; i++) {
                    //AddButton(i);
                //}
                //await update();
                
            } catch (error) {
                console.error(error.message);
            }
            if (json.keys.index >0){
                document.getElementById('h').style.display = 'none';
            }
            updategame();
    }, 1000);
}
updategame()