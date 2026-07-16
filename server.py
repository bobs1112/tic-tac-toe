#python
from flask import Flask, render_template, jsonify, session
from flask_session import Session
import threading
import time
app = Flask("__name__")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

beforeStartState = "До начала"
waitSecondPlayerGameState = "Ждем подключения второго игрока"
crossMakeMove = "Крестики делают ход"
nullMakeMove = "Нолики делают ход"
crossTimeOut = "Крестики вышли по времени"
nullTimeOut = "Нолики вышли по времени"
gameComplete = "Конец игры"

Session(app)
class Game:
    def empty():
        return
    
    def __init__(self):
        self.currentState = beforeStartState
        self.stop_event = threading.Event()
        self.timer_theard = threading.Thread(target=self.empty)

        self.timer_theard.start()

        self.time_left = 0
        self.cells = [['_', '_', '_'], 
                     ['_', '_', '_'],
                     ['_', '_', '_'],  ]
        
    def returndiagonal(self, diagonal):
    
        if diagonal == 0:
            return [self.cells[0][0], self.cells[1][1], self.cells[2][2]]
        elif diagonal == 1:
            return [self.cells[0][2], self.cells[1][1], self.cells[2][0]]
        return 'Erorr'

    def rowreturn(self, row):
        return self.cells[row]

    def returncolumn(self, column):
        return [self.cells[0][column], self.cells[1][column], self.cells[2][column]]
    def count(self, arr, sym):
        acc = 0
        for i in arr:
            if i == sym:
                acc += 1
        return acc

    def exa(self, sym):
        for i in range(3):
            theRow = self.rowreturn(i)
            if self.count(theRow, sym) == 3:
                return True
        for i in range(3):
            theColumn = self.returncolumn(i)
            if self.count(theColumn, sym) == 3:
                return True
        for i in range(2):
            TheDiagonal = self.returndiagonal(i)
            if self.count(TheDiagonal, sym) == 3:
                return True
        return False
    def delay_action(self, sym):
        self.time_left = 15
        for i in range(15):
            time.sleep(1)
            self.time_left -= 1
            if self.stop_event.is_set():
                return

        if sym == 'O':
            self.currentState = nullTimeOut
        elif sym == 'X':
            self.currentState = crossTimeOut
        return 'lol'

    def IsBeforeStartGame(self):
        return self.currentState == beforeStartState
    
    def IsGameComplete(self):
        return self.currentState == gameComplete
    
    def IsWaitSecondPlayerGame(self):
        return self.currentState == waitSecondPlayerGameState
    
    def PlayerCanMakeMove(self, sym):
        return self.currentState == crossMakeMove and sym == 'X' or self.currentState == nullMakeMove and sym == 'O'
    
    def WaitForOtherPlayer(self, sym):
        return self.currentState == crossMakeMove and sym == 'O' or self.currentState == nullMakeMove and sym == 'X'
    
    def TimeOut(self, sym):
        return self.currentState == crossTimeOut and sym == 'O' or self.currentState == nullTimeOut and sym == 'X'
    
    def CellIsEmpty(self, column, row):
        return self.cells[column][row] != '_'
    
    def MakeMoveCross(self, column, row):
        self.stop_event.set()
        self.timer_theard.join()
        self.cells[column][row] = 'X'
        if self.exa('X') :
            currentState = gameComplete
            return
        
        self.currentState = nullMakeMove
        self.stop_event.clear()
        self.timer_thread = threading.Thread(target=self.delay_action, args=('O'))
        self.timer_thread.start()
    def MakeMoveNull(self, column, row):
        self.stop_event.set()
        self.timer_theard.join()
        self.cells[column][row] = 'O'
        if self.exa('O') :
            currentState = gameComplete
            return
        
        self.currentState = crossMakeMove
        self.stop_event.clear()
        self.timer_thread = threading.Thread(target=self.delay_action, args=('X'))
        self.timer_thread.start()






@app.route("/")
def index():
    return render_template('index.html')


games = {}


@app.route('/start_game/<int:id>')
def start(id) :
    global games
    existGame = games.get(id)
    if existGame is None:
        newGame = Game()
        games[id] = newGame
        
        newGame.currentState = waitSecondPlayerGameState
        session["role"] = 'X'
        
        return render_template('game.html')
    elif existGame.currentState == waitSecondPlayerGameState :
        session["role"] = 'O'
        existGame.currentState = crossMakeMove
        return render_template('game.html')
            
    return "Error"


@app.route('/start_game/<int:id>/cells')
def returncells(id):
    global games
    role = session["role"]
    game : Game = games[id]
    if game.IsWaitSecondPlayerGame():
         return jsonify({
            'state' : "netural",
            'message' : waitSecondPlayerGameState,
            'cells' : game.cells
        });
    if game.PlayerCanMakeMove(role):
        return jsonify({
            'state' : "netural",
            'message' : f"ваш ход, осталось: {game.time_left} сек.",
            'cells' : game.cells
        });
    if game.WaitForOtherPlayer(role):
         return jsonify({
            'state' : "netural",
            'message' : f"ждем хода второго игрока, осталось: {game.time_left} сек.",
            'cells' : game.cells
        });
    if game.TimeOut('X'):
        return jsonify({
            'state' : "win",
            'message' : "крестики вышли по времени",
            'cells' : game.cells
        });
    if game.TimeOut('O'):
        return jsonify({
            'state' : "win",
            'message' : "нолики вышли по времени",
            'cells' : game.cells
        });
    return jsonify({
            'state' : "netural",
            'message' : "",
            'cells' : game.cells
        });

@app.route('/start_game/<int:id>/make_move/<int:column>/<int:row>')
def make_move(id, column, row):
    global games
    game : Game = games[id]
    role = session["role"]
    if game.CellIsEmpty(column, row):
        return jsonify({
            'success' : False,
            'error' : "Эта ячейка уже занята!"
        });
    if game.PlayerCanMakeMove(role) == False:
        return  jsonify({
            'success' : False,
            'error' : "Сейчас не ваш ход!"
        })
    
    
    
    
    # если игра пока не закончена, то дать команду ждать второго игрока, а второму игроку показать сделанный ход и ждать его хода 
    
    #проверка, что сейчас крестики делают ход (или нолики)
    if role == 'X':  
        game.MakeMoveCross(column, row)
        # если текущий игрок выиграл, то вернуть страницу победы (а второму - дать сигнал, что он проиграл)
        if game.IsGameComplete() :
            return jsonify({
                'success' : True,
                'winner' : 'X',
                'cells' : game.cells
            })
    
    #проверка, что сейчас крестики делают ход (или нолики)
    if role == 'O' :  
        game.MakeMoveNull(column, row)
        if game.IsGameComplete() :
            return jsonify({
                'success' : True,
                'winner' : 'O',
                'cells' : game.cells
            })
        
    return jsonify({
        'success' : True,
        'cells' : game.cells
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

if __name__ == '__main__':
    app.run(debug=True)