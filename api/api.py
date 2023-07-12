from flask import Flask, request
from flask_restful import Api, Resource
import json


app = Flask(__name__)
api = Api()


class GetGameData(Resource):
    def get(self):
        gameId = request.args.get('gameId')
        with open("gamesdata.json", "r", encoding="utf-8") as file:
            gameData = json.load(file)
        for game in gameData:
            if game["gameId"] == int(gameId):
                return game
        return "Error: There is no game with this id"
    

class PostGameData(Resource):
    def post(self):
        with open("gamesdata.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        postData = json.loads(request.data)
        gamedata = {}
        gamedata["gameId"] = postData["gameId"]
        gamedata["players"] = [
            dict(
                username=postData['username1'], current_game_state=dict(is_game_over=True, score=postData['score1'])
            ),
            dict(
                username=postData['username2'],
                current_game_state=dict(is_game_over=True, score=postData['score2']),
            ),
        ]
        gamedata["is_game_over"] = True
        gamedata["questions"] = []
        for i in range(len(postData['text'])):
            gamedata["questions"].append(dict(
                text = postData['text'][i],
                options = list(*postData["answers"][i][0].values()),
                answer = list(postData["answers"][i][1].values()),
            ))

        data.append(gamedata)


        with open("gamesdata.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


api.add_resource(GetGameData, "/getgamedata")
api.add_resource(PostGameData, "/postgamedata")
api.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)