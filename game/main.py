import json
import random
import requests


score = 0


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


def postDataOnServer(username, score, questionsData):
    questions = list(questionsData.keys())
    answers = list(questionsData.values())
    payload = json.dumps({
        "gameId": random.randint(1, 10000),
        "username1": username,
        "username2": "None",
        "score1": score,
        "score2": score,
        "text": questions,
        "answers": answers
    })
    headers = {'Content-Type': 'application/json'}
    
    return requests.post(url="http://127.0.0.1:5000/postgamedata", data=payload, headers=headers)


def startGame():
    username = input("Введите ваше имя: ")
    questions = getQuestions()
    questionsForPostData = questions.copy()
    
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
    postDataOnServer(username=username, score=score, questionsData=questionsForPostData)


if __name__ == "__main__":
    startGame()
    