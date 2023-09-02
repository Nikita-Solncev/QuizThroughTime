from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json
import uuid
from pprint import pprint


app = Flask(__name__)
api = Api()


class GameData(Resource):
    def get(self, gameId):
        """
        Получаем игровую сессию по её id
        """
        with open("gamesdata.json", "r", encoding="utf-8") as file:
            gameData = json.load(file)
        for game in gameData:
            if game["gameId"] == gameId:
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

        
        game = next((x for x in gameData if x["gameId"] == id), None)              
        game = gameData.pop(gameData.index(game))

    
        player = {
            "username": requestData["username"],
            "current_game_state": {"is_game_over": True, "score": requestData["score"]},
            "questions": []
        }
        game["players"].append(player)

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

        gamedata = {
            "gameId": uuid.uuid4().hex,
            "is_game_over": False,
            "players": []
        }


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
        
        availableSessions = [game["gameId"] for game in data if not game["is_game_over"]]
        
    
        return jsonify({"AVAILABLE SESSIONS": availableSessions})
    

api.add_resource(GameData, "/gamedata/<id>")
api.add_resource(CreateGame, "/gamedata")
api.add_resource(Sessions, "/sessions")
api.init_app(app)


if __name__ == "__main__":
    app.run(debug=True, port=5000)