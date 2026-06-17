#python
from flask import Flask, render_template, jsonify, session
from flask_restful import Api, Resource
from flask_session import Session

app = Flask("__name__")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


beforeStartState = "До начала"
waitSecondPlayerGameState = "Ждем подключения второго игрока"
crossMakeMove = "Крестики делают ход"
nullMakeMove = "Нолики делают ход"
gameComplete = "Конец игры"

currentState = beforeStartState


@app.route("/")
def index():
    return render_template('index.html')

games = {}
cells = [['_', '_', '_'], 
         ['_', '_', '_'],
         ['_', '_', '_'],  ]

@app.route('/start_game')
def start() : 
    global cells
    global currentState
    if currentState == beforeStartState or currentState == gameComplete :
        currentState = waitSecondPlayerGameState
        session["role"] = 'X'
        cells = [['_', '_', '_'], 
                ['_', '_', '_'],
                ['_', '_', '_'],  ]
        
        return render_template('game.html')
    
    if currentState == waitSecondPlayerGameState :
        session["role"] = 'O'
        currentState = crossMakeMove
        return render_template('game.html')
        
    return "Error"

def exa(sym):
    if cells[0][0] == sym and cells[1][0] == sym and cells[2][0] == sym:
        return True
    if cells[0][0] == sym and cells[0][1] == sym and cells[0][2] == sym:
        return True
    if cells[0][0] == sym and cells[1][1] == sym and cells[2][2] == sym:
        return True
    
    return False


@app.route('/cells')
def returncells():
    return jsonify(cells)

@app.route('/make_move/<int:column>/<int:row>')
def make_move(column, row):
    global cells
    global currentState
     

    if cells[column][row] != '_' :
        return jsonify({
            'success' : False,
            'error' : "Эта ячейка уже занята!"
        });
    
    
    role = session["role"]
    
    # если игра пока не закончена, то дать команду ждать второго игрока, а второму игроку показать сделанный ход и ждать его хода 
    
    #проверка, что сейчас крестики делают ход (или нолики)
    if currentState == crossMakeMove and role == 'X':  
        cells[column][row] = 'X'

        # если текущий игрок выиграл, то вернуть страницу победы (а второму - дать сигнал, что он проиграл)

        if exa('X') :
            currentState = gameComplete
            return jsonify({
                'success' : True,
                'winner' : 'X',
                'cells' : cells
            })
        
        currentState = nullMakeMove

        return jsonify({
            'success' : True,
            'cells' : cells
        })
    
    #проверка, что сейчас крестики делают ход (или нолики)
    if currentState == nullMakeMove and role == 'O' :  
        cells[column][row] = 'O'
        currentState = crossMakeMove

        if exa('O') :
            currentState = gameComplete
            return jsonify({
                'success' : True,
                'winner' : 'O',
                'cells' : cells
            })
        

        return jsonify({
            'success' : True,
            'cells' : cells
        })

    

    return  jsonify({
            'success' : False,
            'error' : "Сейчас не ваш ход!"
        })
    

#    for column_index, columns in enumerate(cells):
#        for row_index, cell in enumerate(columns):
#            if cell == '_' :
#                cells[column_index][row_index] = 'O'
#                answer = {
#                    'column' : column_index,
#                    'row' : row_index
#                }

#               return jsonify(answer)

    return ''

@app.route("/clear")
def clear():
    global cells
    cells = [['_', '_', '_'], 
         ['_', '_', '_'],
         ['_', '_', '_'],  ]
    return ""

if __name__ == '__main__':
    app.run(debug=True)