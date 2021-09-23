from datetime import date, datetime, time
from tensorflow.keras.preprocessing import image  # Для отрисовки изображения
from tensorflow.keras.optimizers import Adam  # Подключаем оптимизатор Adam
from tensorflow.keras.models import (  # Подлючаем класс создания модели Sequential
    Sequential, load_model)
from tensorflow.keras.layers import (  # Подключаем класс Dense - полносвязный слой
    BatchNormalization, Dense)
from tensorflow.keras.datasets import mnist  # Библиотека с базой Mnist
from tensorflow.keras import utils  # Утилиты для to_categorical
from pyowm.utils.config import get_default_config
from pyowm import OWM
from PIL import Image  # Отрисовка изображений
from mpl_toolkits.mplot3d import Axes3D  # Модуль для трехмерной графики
import seaborn as sns
import pylab  # Модуль для построения графиков
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np  # linear algebra; Подключаем библиотеку numpy
import matplotlib.pyplot as plt  # Отрисовка изображений


def collect_data():
    now = datetime.now()
    hour = str(time(now.hour))
    print(hour)
    month = int(time(now.month))
    place = "Москва"
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM('bb2a15ee564dc99c215f9820f991dc57', config_dict)
    observation = owm.weather_manager().weather_at_place(place)
    w = observation.weather
    temp = w.temperature('celsius')['temp']
    wind_speed = w.wind()['speed']
    return np.asarray([temp, wind_speed, hour, month])


def predict(data):
    model = load_model("./house_a_2.h5")
    a = model.predict([data])
    return a[0]/50


while True:
    pred = predict(collect_data())
    print(pred)
