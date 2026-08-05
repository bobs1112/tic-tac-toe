function AddButt(id){
    const link = document.createElement('a');
    const ButtGame = document.createElement('button')
    
    link.href = window.location.href + `start_game/${id}`;

    ButtGame.textContent = `зайти в игру: ${id}`;
    ButtGame.className = "butt"

    link.append(ButtGame);
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
                    AddButt(i);
                }
                //await update();
                
            } catch (error) {
                console.error(error.message);
            }

            updategame();
    }, 1000);
}
updategame()