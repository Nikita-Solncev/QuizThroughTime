from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json
import uuid


app = Flask(__name__)
api = Api()


class GameData(Resource):
    def get(self, id):
        """
        Получаем игровую сессию по её id
        """
        with open("gamesdata.json", "r", encoding="utf-8") as file:
            gameData = json.load(file)
        for game in gameData:
            if game["gameId"] == id:
                return game
        return jsonify({"Error": "There is no game with this id"})
    
    
    def put(self, id):
        """
        Обновляем данные в игровой сессии
        """
        requestData = json.loads(request.data)


        #т.к. используем json(что слегка не удобно), выкачиваем все его содержимое, чтобы изменить его
        with open("gamesdata.json", "r", encoding="utf-8") as file:
            gameData = json.load(file)


        #ищем игровую сессию с нужным id. Если не находим, то возвращаем ошибку
        game = None
        for i in gameData:
            if i["gameId"] == id:
                game = i
                break
        else:
            return jsonify({"Error": "There is no game with this id"})

        game = gameData.pop(gameData.index(game)) #сессию, данные которой нужно изменить удаляем и получаем её содержимое

        game["players"].append(dict(username = requestData["username"], current_game_state=dict(is_game_over=True, score=requestData["score"]), questions=[]))

        player = None
        player = 0 if len(game["players"]) == 1 else 1

        for i in range(len(requestData['text'])):
            game["players"][player]["questions"].append(dict(
                text = requestData['text'][i],
                options = list(*requestData["answer"][i][0].values()),
                answer = list(requestData["answer"][i][1].values()),
            ))


        if len(game["players"]) == 2:
            game["is_game_over"] = True


        gameData.append(game) #Вставляем сессию обратно


        with open("gamesdata.json", "w", encoding="utf-8") as file:
            json.dump(gameData, file, ensure_ascii=False, indent=4)
        
         

class CreateGame(Resource):
    def post(self):
        """
        Создаем пустую сессию 
        """
        with open("gamesdata.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        gamedata = {}
        gamedata["gameId"] = uuid.uuid4().hex

        gamedata["is_game_over"] = False

        gamedata["players"] = []

        data.append(gamedata)


        with open("gamesdata.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class Sessions(Resource):
    def get(self):
        """
        Получаем кол-во незаконченных сессий
        """
        with open("gamesdata.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        availableSessions = []
        for game in data:
            if game["is_game_over"]:
                continue
            availableSessions.append(game["gameId"])
    
        return jsonify({"AVAILABLE SESSIONS": availableSessions})
    

api.add_resource(GameData, "/gamedata/<id>")
api.add_resource(CreateGame, "/gamedata")
api.add_resource(Sessions, "/sessions")
api.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)