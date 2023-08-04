import json
import random
import requests


def createNewSession(username):
    """
    Отправляет запрос на создание новой игровой сессии.
    """
    return requests.post(url="http://127.0.0.1:5000/gamedata")


def updateCurrentSession(id, data):
    """
    Отправляет запрос на обновление существующей сессии.
    """
    return requests.put(url=f"http://127.0.0.1:5000/gamedata/{id}", data=data)


def getQuestions():
    """
    Получает вопросы из json файла. Возвращает словарь с пятью случайными вопросами.
    """
    questions = {}

    with open("questions.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    for _ in range(5):
        question = random.choice(data["questions"])
        questions[question["question"]] = [
            dict(options=question["options"]),
            dict(answer=question["answer"]),
        ]

        data["questions"].remove(question) #удаляю вопрос, чтобы он не повторился ещё раз

    return questions


def startGameLoop(gameId, username):
    """
    Цикл игры. По окончанию игры отправляется запрос на обновление данных сессии.
    """
    questions = getQuestions()
    questionsForGameData = questions.copy() #Копия словаря questions, т.к. во время игры он изменяется, а после игры он нам понадобится, чтобы отправить данные в сессию. 
    score = 0

    while len(questions) != 0:
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

        del questions[currentQuestion] #Удаляем вопрос из словаря questions, т.к. цикл работает до тех пор, пока в словаре есть вопросы

    print(f"ИГРА ОКОНЧЕНА. ВАШ СЧЁТ {score}")

    updateCurrentSession(
        gameId,
        data=json.dumps(
            {
                "username": username,
                "score": score,
                "text": list(questionsForGameData.keys()),
                "answer": list(questionsForGameData.values()),
            }
        ),
    )


def searchingForGame():
    """
    Ищет игру. Если есть незаконченная сессия, то заканчиваем её.
    """
    response = requests.get(url="http://127.0.0.1:5000/sessions").json()
    username = input("Введите ваше имя: ")

    print(f"ИГР ДОСТУПНО: {len(response['AVAILABLE SESSIONS'])}")

    if len(response["AVAILABLE SESSIONS"]) == 0:
        print("ДОСТУПНЫХ ИГР НЕТ, ГОТОВЫ НАЧАТЬ НОВУЮ?")
        while True:
            userChoice = input("y/n\n")
            if userChoice == "y":
                createNewSession(username)
                response = requests.get(url="http://127.0.0.1:5000/sessions").json()
                gameId = response["AVAILABLE SESSIONS"][0]
                startGameLoop(gameId, username)
                break
            elif userChoice == "n":
                print("УВИДИМСЯ В СЛЕДУЮЩИЙ РАЗ!")
                break
            
            else:
                print("Значение неверно")
    
    else:
        gameId = response["AVAILABLE SESSIONS"][0]
        startGameLoop(gameId, username)



if __name__ == "__main__":
    searchingForGame()
