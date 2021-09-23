# Импортируем все нужные библиотеки
import os

from flask import (
    Flask, render_template, request,
    session, redirect, url_for, 
    jsonify, Response
)
from flask_session import Session
from flask_cors import CORS

from pyowm import OWM
from pyowm.utils.config import get_default_config

import json

# Создаём объект (экземпляр) класса, указываем в нём папки, откуда нужно брать html, css, js для сайта
app = Flask(
    __name__,
    static_folder = "./dist/static",
    template_folder = "./dist"
)

# Создаём секретный ключ и задаём тип для нашей сессии, где будут храниться данные от аккаунтов
# текущих авторизованных пользователей.
app.secret_key = 'adDsJDsjaAlG02fCs'
app.config['SESSION_TYPE'] = 'filesystem'

# Устанавливаем русский язык для PYOWM, создаём объект (экземпляр) класса для последующего взаимодействия
# с библиотекой PyOWM - получения данных о погоде в Москве.
config_dict = get_default_config()
config_dict['language'] = 'ru' 

owm = OWM('a99967bc9ee70d5b4bd387902982f400', config_dict)

mgr = owm.weather_manager()


# Если пользователь захочет войти на страницу 127.0.0.1:5000 - то его перенаправит сюда.
# Функция перенаправляет человека на другие страницы, если он не авторизован, или наоборот 
# уже авторизован и имеет статус Administration/Hospital/MES/House
@app.route("/")
def index():
    if not "already_participated" in session:
        return redirect(url_for("login"))
    if session['status'] == 'Administration':
        return redirect(url_for("administration"))
    if session['status'] == 'Hospital':
        return redirect(url_for("hospital"))
    if session['status'] == 'MES':
        return redirect(url_for("mes"))
    if session['status'] == 'House':
        return redirect(url_for("home"))
    return render_template("index.html")


# Если пользователь зайдёт на подссылку /home, то его либо перевведёт
# к авторизации, либо переведёт в / для перенаправления человека на ту
# подссылку, к которой относится его статус (сработает в том случае,
# если сессионный статус не равен House), или покажет саму страницу.
@app.route("/home")
def home():
    if not "already_participated" in session:
        return redirect(url_for("login"))
    if session['status'] != 'House':
        return redirect(url_for("index"))
    return render_template("index.html")


# Если пользователь зайдёт на подссылку /administration, то его либо перевведёт
# к авторизации, либо переведёт в / для перенаправления человека на ту
# подссылку, к которой относится его статус (сработает в том случае,
# если сессионный статус не равен Administration), или покажет саму страницу.
@app.route("/administration")
def administration():
    if not "already_participated" in session:
        return redirect(url_for("login"))
    if session['status'] != 'Administration':
        return redirect(url_for("index"))
    return render_template("index.html")


# Если пользователь зайдёт на подссылку /hospital, то его либо перевведёт
# к авторизации, либо переведёт в / для перенаправления человека на ту
# подссылку, к которой относится его статус (сработает в том случае,
# если сессионный статус не равен Hospital), или покажет саму страницу.
@app.route("/hospital")
def hospital():
    if not "already_participated" in session:
        return redirect(url_for("login"))
    if session['status'] != 'Hospital':
        return redirect(url_for("index"))
    return render_template("index.html")


# Если пользователь зайдёт на подссылку /mes, то его либо перевведёт
# к авторизации, либо переведёт в / для перенаправления человека на ту
# подссылку, к которой относится его статус (сработает в том случае,
# если сессионный статус не равен MES), или покажет саму страницу.
@app.route("/mes")
def mes():
    if not "already_participated" in session:
        return redirect(url_for("login"))
    if session['status'] != 'MES':
        return redirect(url_for("index"))
    return render_template("index.html")


# Если пользователь зайдёт на подссылку /login, то его либо перевведёт
# в / для перенаправления человека на ту подссылку, к которой относится
# его статус (сработает в том случае, если человек уже авторизован), либо
# покажет страницу для авторизации.
@app.route("/login")
def login():
    if "already_participated" in session:
        return redirect(url_for("index"))
    return render_template("index.html")


# Функция для проверки пароля и логина, который пользователь ввёл при авторизации.
# Если пароль/логин не введенны - отправит соответствующую ошибку, если пароль/логин
# введены не верно - отправит success = False, если авторизация произведенна успешно -
# отправит success = True и присвоит пользователю нужный статус сессии, и, если пользователь
# был авторизован под аккаунтом дома будет присвоинна data, в которой будет храниться номер дома
# пользователя. 
@app.route("/check_user")
def check_user() -> Response:
    if request.args.get("username") and request.args.get("password"):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
        for v in data['users']:
            if data['users'][v]['name'] == request.args['username'] and \
                data['users'][v]['password'] == request.args['password']:
                    session['already_participated'] = True
                    if v.startswith("House"):
                        session['status'] = "House"
                        session['data'] = v.split("-")[1]
                    else:
                        session['status'] = v
                        session['data'] = ""
                    return jsonify({'success': True})
        return jsonify({'success': False})
    return jsonify({'success': False, 'error': 'Имя пользователя/пароль не верны!'})


# Функция удалит все данные с текущей сессии пользователя.
@app.route("/exit")
def quit_user() -> Response:
    del session['already_participated']
    return jsonify({'success': True})


# Функция выдаст информацию о том, подключенны, или отключенны здания
# к сети.
@app.route("/get_buildings_status")
def get_buildings_status() -> Response:
    with open("здания.txt", "r") as file:
        data = file.read() # Если значение 0 - отключенно, значение 1 - поделюченно.
        # data[0] - администрация, data[1] - больница, data[2] - МЧС
        # Пример:

        # 0 - отключенна (Администрация)
        # 1 - подключенна (Больница)
        # 1 - подключенно (МЧС)

        data = ["подключенно" if idx == "1" else "отключенно" 
                for idx in data.split("\n")]
        return jsonify(
            {"admin": data[0], "hospital": data[1], "mes": data[2]}
        )


# Функция выдаст информацию о том, подключенны, или отключенны дома
# к сети.
@app.route("/get_houses_status")
def get_houses_status() -> Response:
    with open("дома.txt", "r") as file:
        data = file.read() # Если значение 0 - отключенно, значение 1 - поделюченно.
        # data[0] - дом 1, data[1] - дом 2
        # Пример:

        # 0 - отключён (дом 1)
        # 1 - подключён (дом 2)

        data = ["подключенно" if idx == "1" else "отключенно" 
                for idx in data.split("\n")]
        return jsonify(
            {"house1": data[0], "house2": data[1]}
        )


# Функция возращает информацию о текущем заряде всех батарей города
# суммарно в процентном значении.
@app.route("/get_batteries_status")
def get_batteries_status() -> str:
    with open("батареи.txt", "r") as file:
        return f"{file.read()}%" # эквивалент к str(file.read()) + "%"


# Функция вернёт текущий статус работы, опираясь на текущее значение
# заряда всех батарей города.
@app.route("/get_status")
def get_status() -> str:
    battarey = get_batteries_status()
    battarey = int(battarey[:-1]) # переводим в число полученный ответ от функции "get_batteries_status"
    # [:-1] - обрезание на 1 символ строки с задней стороны. Пример:
    # a = "Hello, world !" - нам нужно обрезать строку на один символ, то есть убрать !
    # Мы можем сделать так: a[:-1], что выдаст данный результат - "Hello, world".
    # В данном случае battarey.replace("%", "") - аналогия к battarey[:-1], так как мы уже точно знаем,
    # какой символ нам нужно убрать.
    if battarey > 80:
        return "режим переработки"
    elif battarey < 80 and battarey > 50:
        return "cтандартный режим"
    elif battarey < 50 and battarey > 20:
        return "режим сохранения энергии"
    return "режим энергосбережения"


# Функция вернёт текущее количество воды в "ГЭС", доступное для всего города.
# в миллилитрах.
@app.route("/get_count_water")
def get_count_water() -> str:
    with open("вода.txt", "r") as file:
        return f"{file.read()} мл" # эквивалент к str(file.read()) + " мл"


# Функция вернёт текущее значение выработки всего города в амперах.
@app.route("/get_production_status")
def get_production_status() -> str:
    with open("выработка.txt", "r") as file:
        return f"{file.read()} ам" # эквивалент к str(file.read()) + " ам"


# Функция вернёт текущее значение потребления всего города в амперах.
@app.route("/get_total_consumption_status")
def get_total_consumption_status() -> str:
    with open("потребление.txt", "r") as file:
        return f"{file.read()} ам" # эквивалент к str(file.read()) + " ам"


# Функция вернёт полную информацию о том доме, под которым авторизировался
# пользователь. Для определения, под какой именно дом был авторизован человек
# к его сессии добавляется data, в которой и указан номер дома. В нашем случае
# есть лишь два дома - соответственно и возможных номеров сейчас может быть только
# двое, но при желании их количество можно спокойно увеличить, логику функции это не
# сломает.
@app.route("/get_house_information")
def get_house_information() -> Response:
    # Мы открываем файл, к примеру дом_1, цифра автоматически
    # подставится по той data, которая была присвоина к сессии
    # пользователя при авторизации.
    with open(f"дом_{session['data']}.txt") as file:
        data = file.read().split("\n")
        # В data записывается вся нужная информация о доме пользователя:
        # - статус подключенния к сети (data[0])
        # - статус заряда батареии дома пользователя в процентном значении (data[1])
        # - количество воды, доступной для использования в этом доме (data[2])
        # - количество потребления энергии домом в амперах.
    return jsonify(
        {
            "status": "подключён"
            if data[0] == "1" else
            "отключён",
            "battery": f"{data[1]}%",
            "water": f"{data[2]} мл",
            "total_consumption": f"{data[3]} ам"
        }
    )


# Делает точно тоже, что и предидущая функция, только уже
# именно для больницы города.
@app.route("/get_hospital_information")
def get_hospital_information() -> Response:
    with open("больница.txt") as file:
        data = file.read().split("\n")
    return jsonify(
        {
            "status": "подключена"
            if data[0] == "1" else
            "отключена",
            "battery": f"{data[1]}%",
            "water": f"{data[2]} мл",
            "total_consumption": f"{data[3]} ам"
        }
    )


# Делает точно тоже, что и предидущая функция, только уже
# именно для МЧС города.
@app.route("/get_mes_information")
def get_mes_information() -> Response:
    with open("мчс.txt") as file:
        data = file.read().split("\n")
    return jsonify(
        {
            "status": "подключено"
            if data[0] == "1" else
            "отключено",
            "battery": f"{data[1]}%",
            "water": f"{data[2]} мл",
            "total_consumption": f"{data[3]} ам"
        }
    )


# Возращает всю информацию о текущей погоде в Москве.
@app.route("/get_weather")
def get_weather() -> dict:
    observation = mgr.weather_at_place("Москва")
    w = observation.weather
    print(w.temperature('celsius'))
    return w.temperature('celsius') # это словарь, с такими данными:
    # {'temp': 17.43, 'temp_max': 17.43, 'temp_min': 17.05, 'feels_like': 17.11}
    # - temp - средняя температура за день
    # - temp_max - максимальная температура за день
    # - temp_min - минимальная температура за день
    # - feels_like - температура по ощущениям в данный момент


# Функция для получение data сессии пользователя, если её нет - вернёт пустую строку.
@app.route("/get_user_data")
def get_user_data() -> str:
    return session['data']


# Функция, возращающая статус погоды в Москве.
# Возможные значения статуса:
# - ясно.
# - пасмурно.
# и т. д.
@app.route("/get_status_weather")
def get_status_weather() -> str:
    observation = mgr.weather_at_place("Москва")
    w = observation.weather

    return w.detailed_status


# Все последующие функции возращают точный путь для фотографий графиков.
@app.route("/get_photo_administration")
def get_photo_administration() -> str:
    return "/static/img/администрация.png"


@app.route("/get_photo_hospital")
def get_photo_hospital() -> str:
    return "/static/img/больница.png"


@app.route("/get_photo_mes")
def get_photo_mes() -> str:
    return "/static/img/мчс.png"


@app.route("/get_photo_house")
def get_photo_house() -> str:
    return f"/static/img/дом_{session['data']}.png"


# Функия изменяет темы. 0 - белая, 1 - чёрная.
@app.route("/set_theme")
def set_theme() -> str:
    if request.args.get("theme") and request.args["theme"] == "white":
        with open("тема.txt", "w") as file:
            file.write("0")
    else:
        with open("тема.txt", "w") as file:
            file.write("1")
    return "theme changed."


if __name__ == "__main__":
    CORS(app) # ОБЯЗАТЕЛЬНО НУЖНО ДЛЯ ВЗАИМОДЕЙСТВИЯ html, js, css С ПРОЕКТОМ, НЕ УДАЛЯТЬ!!!
    Session(app) # Нужно для создания сессий пользователей, хранение информации о их авторизации и т.д.
    app.run(host='0.0.0.0', port=5000) # запуск самого проекта на хосте 0.0.0.0 (127.0.0.1, localhost) и порте 5000
    # ПОРТ НЕ МЕНЯТЬ!!!!!!!!!!!!!!
