# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
# Open issues: need to somehow call the categories in the RepeatCategoryIntent.
import random
import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

# added for remembering category
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

# added to pick a random question from the list

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Added questions in each category, eventually this will be moved to a database
python_questions = ["python placeholder"]
f = open("python.txt", "r")
for row in f:
    python_questions.add(row)
f.close()

# with open('python.txt') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         python_questions.add(row)
# if line_count == 0:
#     print(f'Column names are {", ".join(row)}')
#     line_count += 1
# else:
#     print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
#     line_count += 1
# print(f'Processed {line_count} lines.')

interview_category = ["python", "c programming language",
                      "java", "c plus plus", "behavioral", "technical", "coding"]
c_questions = ["C question placeholder."]
c_plus_plus_questions = ["C plus plus question placeholder."]
java_questions = ["JAVA question placeholder."]
coding_questions = ["Coding question placeholder."]
behavioral_questions = ["Behavioural question placeholder."]
technical_questions = ["Technical question placeholder."]


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Practice buddy! Are you ready to sharpen your interview skills? You can practice questions by saying a category name, like Behavioral, Technical or Coding questions or programming languages. What would you like to practice?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Can you please say it again?")
            .response
        )


class HasCategoryLaunchRequestHandler(AbstractRequestHandler):
    """Handler for launch after the user have set the interview_category"""

    def can_handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("interview_category" in attr)

        return attributes_are_present and ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # retrieve the attribute
        attr = handler_input.attributes_manager.persistent_attributes
        category = attr['interview_category']

        speak_output = "Welcome back to Practice buddy. Want to keep practicing {category}? Say instructions for what this skill does".format(
            category=category)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Can you please say it again?")
            .response
        )


class CaptureCategoryIntentHandler(AbstractRequestHandler):
    """Handler for CaptureCategoryIntent Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CaptureCategoryIntent")(handler_input)

    def handle(self, handler_input):
        # bringing in the slot values
        slots = handler_input.request_envelope.request.intent.slots

        # specifically extracting INTERVIEW_CATEGORY
        category = slots["INTERVIEW_CATEGORY"].value

        # saving the interview category in the "interview_category" persistent_attribute
        attributes_manager = handler_input.attributes_manager
        category_attributes = {
            "interview_category": category
        }
        attributes_manager.persistent_attributes = category_attributes
        attributes_manager.save_persistent_attributes()

        # type: (HandlerInput) -> Response
        question = find_a_question(category)

        speak_output = "Here is a question in {category}. ".format(
            category=category) + question + " " + "When done, say next question or switch category!"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Can you please say it again?")
            .response
        )


class SwitchCategoryIntentHandler(AbstractRequestHandler):
    """Handler for SwitchCategoryIntent Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SwitchCategoryIntent")(handler_input)

    def handle(self, handler_input):

        # bringing in the slot values
        slots = handler_input.request_envelope.request.intent.slots

        # if it's not null
        if slots["INTERVIEW_CATEGORY"].value is not None:

            # specifically extracting INTERVIEW_CATEGORY
            category = slots["INTERVIEW_CATEGORY"].value

            # saving the interview category in the "interview_category" persistent_attribute
            attributes_manager = handler_input.attributes_manager
            category_attributes = {
                "interview_category": category
            }
            attributes_manager.persistent_attributes = category_attributes
            attributes_manager.save_persistent_attributes()

            # type: (HandlerInput) -> Response
            # Determine the question in a specific caregory
            question = find_a_question(category)

            speak_output = "Here is a question in {category}. ".format(
                category=category) + " " + question + " " + "When done, say next question or switch category!"
        else:
            speak_output = "Which category would you like?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Can you please say it again?")
            .response
        )


class AskNextQuestionIntentHandler(AbstractRequestHandler):
    """Handler for AskNextQuestionIntent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AskNextQuestionIntent")(handler_input)

    def handle(self, handler_input):

        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("interview_category" in attr)
        attr = handler_input.attributes_manager.persistent_attributes
        if attributes_are_present:
            category = attr['interview_category']

        # type: (HandlerInput) -> Response
        question = find_a_question(category)

        speak_output = question + " When done, say next question or switch category!"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Can you please say it again?")
            .response
        )


class GetInstructionsIntentHandler(AbstractRequestHandler):
    """Handler for GetInstructionsIntent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetInstructionsIntent")(handler_input)

    def handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        # type: (HandlerInput) -> Response

        speak_output = "This skill allows you to practice your interview skills by asking you a variety of questions from various categories. You can switch question categories, ask for category names, or continue to have me ask more questions in an existing category. Happy interviewing! What would you like to do next?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Can you please say it again?")
            .response
        )


class RepeatCategoryIntentHandler(AbstractRequestHandler):
    """Handler for RepeatCategoryIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RepeatCategoryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Here are the available categories: "
        # The following is not able to pull all possible slot values from the interview_category slot
        categories = ""
        for category in interview_category:
            categories = categories + category + ", "

        return (
            handler_input.response_builder
            .speak(speak_output + categories)
            .ask("Can you please say it again?")
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


''' The following function finds the correct list based on the category given.'''


def find_a_question(str):
    if str.lower() == 'c' or str.lower() == 'c programming language':
        return random.choice(c_questions)
    elif str.lower() == 'c plus plus':
        return random.choice(c_plus_plus_questions)
    elif str.lower() == 'coding':
        return random.choice(coding_questions)
    elif str.lower() == 'behavioral':
        return random.choice(behavioral_questions)
    elif str.lower() == 'technical':
        return random.choice(technical_questions)
    elif str.lower() == 'python':
        return random.choice(python_questions)
    elif str.lower() == 'java':
        return random.choice(java_questions)
    else:
        return random.choice(coding_questions)


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
# sb = SkillBuilder()
sb = CustomSkillBuilder(persistence_adapter=s3_adapter)
sb.add_request_handler(HasCategoryLaunchRequestHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureCategoryIntentHandler())
sb.add_request_handler(AskNextQuestionIntentHandler())
sb.add_request_handler(SwitchCategoryIntentHandler())
sb.add_request_handler(RepeatCategoryIntentHandler())
sb.add_request_handler(GetInstructionsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
