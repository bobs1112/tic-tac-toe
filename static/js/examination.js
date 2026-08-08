// js
async function updatecells() {
        setTimeout(async function() {
            const currentUrl = window.location.href
            const url = currentUrl + `/cells`;
                try {
                    const response = await fetch(url);
                    if (!response.ok) {
                    throw new Error(`Response status: ${response.status}`);
                }

            const result = await response.json();
            console.log(result);
            document.querySelector('#state').textContent = result.message;
            if (result.state == "win"){
                const winSound = new Audio('/static/sound/win.mp3')
                winSound.currentTime = 0
                winSound.play()
                setTimeout(function() {
                    if (result.winner == 'X') {
                        window.location.href = "http://localhost:5000/win/X";
                    } 
                    if (result.winner == 'O') {
                        window.location.href = "http://localhost:5000/win/O";
                    }
                    return;
                }, 500);
            }
                await update(result.cells);
                
            } catch (error) {
                console.error(error.message);
            }

            updatecells();
    }, 500);
}
updatecells();