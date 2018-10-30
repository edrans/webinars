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
        local_time = datetime.datetime.now().strftime('%I:%M %p')

        speech_text = "<speak>Son <say-as interpret-as='time'>{}</say-as></speak>".format(local_time)

        print(speech_text)

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Reloj Mundial", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response

# GetCityTime Intent handler
class GetCityTimeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GetCityTimeIntent")(handler_input)

    def handle(self, handler_input):

        slots = handler_input.request_envelope.request.intent.slots

        if city_slot in slots:
            city = slots[city_slot].value
            city_trim = city.replace(" ","_")

            matching = [s for s in pytz.all_timezones if city_trim.lower() in s.lower()][0]
            city_timezone = pytz.timezone(matching)
            city_time = datetime.datetime.now(city_timezone).strftime('%I:%M %p')

            speech_text = "<speak>En {} son <say-as interpret-as='time'>{}</say-as></speak>".format(city, city_time)

            print(speech_text)

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Reloj Mundial", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    # Handler for Help Intent
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
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
