from pyowm import OWM
from pyowm.utils.config import get_default_config

place = "Волгоград"

config_dict = get_default_config()
config_dict['language'] = 'ru' 

owm = OWM( 'a99967bc9ee70d5b4bd387902982f400', config_dict  )

mgr = owm.weather_manager()
observation = mgr.weather_at_place(place)
w = observation.weather

print(w.temperature('celsius'))