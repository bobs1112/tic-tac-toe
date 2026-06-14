// js
async function updatecells() {
        setTimeout(async function() {
            const url = `/cells`;
            try {
                const response = await fetch(url);
                if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
                }

                const result = await response.json();
                console.log(result);
                await update(result);
                
                
            } catch (error) {
                console.error(error.message);
            }

            updatecells();
    }, 1000);
}
updatecells();