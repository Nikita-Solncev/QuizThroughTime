import json
import random
import requests


score = 0


def createNewSession(username):
    return requests.post(
        url="http://127.0.0.1:5000/gamedata",
        data=json.dumps(
            {
                "username": username,
            }
        ),
        headers={"Content-Type": "application/json"},
    )


def updateCurrentSession(id, data):
    return requests.put(url=f"http://127.0.0.1:5000/gamedata/{id}", data=data)


def getQuestions():
    questions = {}

    with open("questions.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    for _ in range(5):
        question = random.choice(data["questions"])
        questions[question["question"]] = [
            dict(options=question["options"]),
            dict(answer=question["answer"]),
        ]

        data["questions"].remove(question)

    return questions


def startGameLoop(gameId):
    questions = getQuestions()
    questionsForGameData = questions.copy()

    while len(questions) != 0:
        global score
        currentQuestion = random.choice(list(questions))
        correctAnswer = questions[currentQuestion][1]["answer"]
        optionalAnswers = questions[currentQuestion][0]["options"]
        random.shuffle(optionalAnswers)

        print(currentQuestion)
        print("Возмжные варианты ответов:\n")
        print("\n".join(optionalAnswers))
        userAnswer = input("\n")

        if userAnswer == correctAnswer:
            score += 1
            print(f"ОТВЕТ ВЕРНЫЙ! ВАШ ТЕКУЩИЙ СЧЁТ: {score}")
        else:
            print(f"ОТВЕТ НЕВЕРНЫЙ! ВАШ ТЕКУЩИЙ СЧЁТ: {score}")
            print(f"Правильный ответ: {correctAnswer}")

        del questions[currentQuestion]

    print(f"ИГРА ОКОНЧЕНА. ВАШ СЧЁТ {score}")

    updateCurrentSession(
        gameId,
        data=json.dumps(
            {
                "score": score,
                "text": list(questionsForGameData.keys()),
                "answer": list(questionsForGameData.values()),
            }
        ),
    )


def searchingForGame():
    response = requests.get(url="http://127.0.0.1:5000/sessions").json()
    username = input("Введите ваше имя: ")

    print(f"ИГР ДОСТУПНО: {len(response['AVAILABLE SESSIONS'])}")

    if len(response["AVAILABLE SESSIONS"]) == 0:
        print("ДОСТУПНЫХ ИГР НЕТ, ГОТОВЫ НАЧАТЬ НОВУЮ?")
        while True:
            userChoice = input("y/n\n")
            try:
                if userChoice == "y":
                    createNewSession(username)
                    response = requests.get(url="http://127.0.0.1:5000/sessions").json()
                    gameId = response["AVAILABLE SESSIONS"][0]
                    startGameLoop(gameId)
                    break
                elif userChoice == "n":
                    print("УВИДИМСЯ В СЛЕДУЮЩИЙ РАЗ!")
                    break
            except ValueError:
                print("Значение неверно")
    # else:
    #     print("ПРИСОЕДИНЯЕМСЯ К НЕЗАКОНЧЕННОЙ ИГРЕ")
    # startGameLoop()

    # gameId = response['AVAILABLE SESSIONS'][0]
    # data = {"username": username,
    #         "gameId": gameId,
    #         ""
    #         }
    # updateCurrentSession(gameId, data)


if __name__ == "__main__":
    searchingForGame()
