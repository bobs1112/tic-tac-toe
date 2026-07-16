// js
const tg = ['#oos', '#ots', '#oths', '#tos', '#tts', '#tths', '#thos', '#thts', '#thths']


async function MakeMove(column, row) {
    const currentUrl = window.location.href
    const url = currentUrl + `/make_move/${column}/${row}`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
        }

        const result = await response.json();
        console.log(result);

        
        if(result.success == false) {
            alert(result.error);
            return;
        }

        update(result.cells);

        if(result.winner == 'X') {
            alert("Выиграли крестики!")
        }

        if(result.winner == 'O') {
            alert("Выиграли нолики!")
        }

                
    } catch (error) {
        console.error(error.message);
    }
       
}
async function update(cells) {
    document.querySelector('#oos').textContent = cells[0][0];
    document.querySelector('#tos').textContent = cells[1][0];
    document.querySelector('#thos').textContent = cells[2][0];

    document.querySelector('#ots').textContent = cells[0][1];
    document.querySelector('#tts').textContent = cells[1][1];
    document.querySelector('#thts').textContent = cells[2][1];

    document.querySelector('#oths').textContent = cells[0][2];
    document.querySelector('#tths').textContent = cells[1][2];
    document.querySelector('#thths').textContent = cells[2][2];
}


document.querySelector('#oo').onclick = function() {
    MakeMove(0, 0);
    
}
document.querySelector('#ot').onclick = function() {
    MakeMove(0, 1);
}
document.querySelector('#oth').onclick = function() {
    MakeMove(0, 2);
}
document.querySelector('#to').onclick = function() {
    MakeMove(1, 0);
}
document.querySelector('#tt').onclick = function() {
    MakeMove(1, 1);
}
document.querySelector('#tth').onclick = function() {
    MakeMove(1, 2);
}
document.querySelector('#tho').onclick = function() {
    MakeMove(2, 0);
}
document.querySelector('#tht').onclick = function() {
    MakeMove(2, 1);
}
document.querySelector('#thth').onclick = function() {
    MakeMove(2, 2);
}
