# -*- coding: utf-8 -*-
#
import sys
import importlib
importlib.reload(sys)

# SDK lib
sys.path.append('sdk/lib/python3.6/site-packages/')

# SDK import
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard

# Timezone
import pytz
from pytz import country_timezones
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pycountry
import gettext

# Logging 
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


sb = SkillBuilder()

help_text = "puedes preguntarme la hora"
welcome_text = "Bienvenido a la skill del reloj mundial. Para empezar " + help_text


# Slot

city_slot = "city"
city_slot_key = "CITY"


class LaunchRequestHandler(AbstractRequestHandler):
    # Handler for Skill Launch
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = welcome_text

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Reloj Mundial", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response

# GetTime Intent handler
class GetTimeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GetTimeIntent")(handler_input)

    def handle(self, handler_input):

        (local_time, ampm) = datetime.datetime.now().strftime('%I:%M %p').split(" ")

        if ampm == "AM":
            ampm = "A.M."
        else:
            ampm = "P.M."

        speech_text = "<speak>Son <say-as interpret-as='time'>{} {}</say-as></speak>".format(local_time, ampm)

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Reloj Mundial", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response

# GetCityTime Intent handler
class GetCityTimeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GetCityTimeIntent")(handler_input)

    def handle(self, handler_input):

        slots = handler_input.request_envelope.request.intent.slots

        if city_slot in slots:

            city_name = slots[city_slot].value

            geolocator = Nominatim(user_agent='worldclock skill')
            location = geolocator.geocode(city_name)
            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
            timezone = pytz.timezone(timezone_str)

            # Get country
            timezone_countries = {timezone: country for country, timezones in country_timezones.items() for timezone in timezones}
            country_code = timezone_countries[timezone_str]
            country = pycountry.countries.get(alpha_2=country_code)

            country_translation = gettext.translation('iso3166', pycountry.LOCALES_DIR, languages=['es'])
            country_translation.install()
            country_name = _(country.name)
            country_name = country_name.split(",")[0]


            (city_time, ampm) = datetime.datetime.now(timezone).strftime('%I:%M %p').split(" ")

            if ampm == "AM":
                ampm = "A.M."
            else:
                ampm = "P.M."

            if " de " + country_name.lower() not in city_name.lower():
                city_name = "".join(city_name.lower().rsplit(country_name.lower()))

            if not city_name:
                speech_text = "<speak>En {}, son <say-as interpret-as='time'>{} {}</say-as></speak>".format(country_name, city_time, ampm)
            else:
                speech_text = "<speak>En {}, {}, son <say-as interpret-as='time'>{} {}</say-as></speak>".format(city_name, country_name, city_time, ampm)

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Reloj Mundial", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    # Handler for Help Intent
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):

        help_text = "Puedes preguntar la hora, por ejemplo, diciendo: 'dime la hora en Buenos Aires'"
        speech_text = help_text

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(SimpleCard("Reloj Mundial", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    # Single handler for Cancel and Stop Intent
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speech_text = "Adios!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Reloj Mundial", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    # AMAZON.FallbackIntent is only available in en-US locale.
    # This handler will not be triggered except in that locale,
    # so it is safe to deploy on any locale
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = (
            "Lo siento, esta Skill de no puede ayudarte con eso." +
            "Puedes pedir otras opciones desde la Ayuda!")
        reprompt = help_text
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    # Handler for Session End
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    # Catch all exception handler, log exception and
    # respond with custom message
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.info("Exception: %s" % (exception))

        print("Encountered following exception: {}".format(exception))

        speech = "Lo siento, hubo un problema. Por favor intente nuevamente!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetTimeIntentHandler())
sb.add_request_handler(GetCityTimeIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
