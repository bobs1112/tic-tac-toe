#python
from flask import Flask, render_template, jsonify, session
from flask_session import Session
import threading
import time
app = Flask("__name__")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


beforeStartState = "До начала"
waitSecondPlayerGameState = "Ждем подключения второго игрока"
crossMakeMove = "Крестики делают ход"
nullMakeMove = "Нолики делают ход"
crossTimeOut = "Крестики вышли по времени"
nullTimeOut = "Нолики вышли по времени"
gameComplete = "Конец игры"
def empty():
    return

timer_theard = threading.Thread(target=empty)
timer_theard.start()
currentState = beforeStartState
time_left = 0
stop_event = threading.Event()
@app.route("/")
def index():
    return render_template('index.html')
def delay_action(sym):
    global time_left
    global currentState
    global stop_event
    time_left = 15
    for i in range(15):
        time.sleep(1)
        time_left -= 1
        if stop_event.is_set():
            return

    if sym == 'O':
        currentState = nullTimeOut
    elif sym == 'X':
        currentState = crossTimeOut
    return 'lol'

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
def rowreturn(row):
    global cells
    return cells[row]
def returncolumn(column):
    global cells
    return [cells[0][column], cells[1][column], cells[2][column]]
def count(arr, sym):
    acc = 0
    for i in arr:
        if i == sym:
            acc += 1
    return acc
def returndiagonal(diagonal):
    global cells
    if diagonal == 0:
        return [cells[0][0], cells[1][1], cells[2][2]]
    elif diagonal == 1:
        return [cells[0][2], cells[1][1], cells[2][0]]
    return 'Erorr'
def exa(sym):
    for i in range(3):
        theRow = rowreturn(i)
        if count(theRow, sym) == 3:
            return True
    for i in range(3):
        theColumn = returncolumn(i)
        if count(theColumn, sym) == 3:
            return True
    for i in range(2):
        TheDiagonal = returndiagonal(i)
        if count(TheDiagonal, sym) == 3:
            return True
    return False


@app.route('/cells')
def returncells():
    global currentState
    global time_left
    if currentState == waitSecondPlayerGameState:
         return jsonify({
            'state' : "netural",
            'message' : waitSecondPlayerGameState,
            'cells' : cells
        });
    if (currentState == crossMakeMove and session["role"] == 'X') or (currentState == nullMakeMove and session["role"] == 'O'):
        return jsonify({
            'state' : "netural",
            'message' : f"ваш ход, осталось: {time_left} сек.",
            'cells' : cells
        });
    if (currentState == crossMakeMove and session["role"] == 'O') or (currentState == nullMakeMove and session["role"] == 'X'):
         return jsonify({
            'state' : "netural",
            'message' : f"ждем хода второго игрока, осталось: {time_left} сек.",
            'cells' : cells
        });
    if currentState == crossTimeOut and session["role"] == 'O':
        return jsonify({
            'state' : "win",
            'message' : "крестики вышли по времени",
            'cells' : cells
        });
    if currentState == nullTimeOut and session["role"] == 'X':
        return jsonify({
            'state' : "win",
            'message' : "нолики вышли по времени",
            'cells' : cells
        });
    return jsonify({
            'state' : "netural",
            'message' : "",
            'cells' : cells
        });

@app.route('/make_move/<int:column>/<int:row>')
def make_move(column, row):
    global cells
    global stop_event
    global currentState
    global timer_theard
    if cells[column][row] != '_' :
        return jsonify({
            'success' : False,
            'error' : "Эта ячейка уже занята!"
        });
    
    
    stop_event.set()
    timer_theard.join()
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
        stop_event.clear()
        timer_thread = threading.Thread(target=delay_action, args=('O'))
        timer_thread.start()
        
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
        stop_event.clear()
        timer_thread = threading.Thread(target=delay_action, args=('X'))
        timer_thread.start()
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
    if currentState == gameComplete:
        global cells
        cells = [['_', '_', '_'], 
         ['_', '_', '_'],
         ['_', '_', '_'],  ]
        return ""
    return "No, sorry—that vulnerability has already been patched)))"
if __name__ == '__main__':
    app.run(debug=True)