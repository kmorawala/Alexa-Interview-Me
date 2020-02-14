# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

#added for remembering category
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

#added to pick a random question from the list
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#Added questions in each category, eventually this will be moved to a database
c_questions = ["What is modular programming?", "What is variable?", "What is the return type of printf() function, and what it returns?", "What is the return type of scanf() function, and what it returns?", "What is the difference between printf() and puts()?"]
c_plus_plus_questions = ["What is this pointer?"]
java_questions = ["What is JAVA?", "What are the features in JAVA?", "How does Java enable high performance?", "What are the Java IDE's?", "What do you mean by Constructor?","What is meant by Local variable and Instance variable?","What is a Class?","What is an Object?"]
python_questions = ["How do you debug a Python program?", "What is <Yield> Keyword in Python?", "How to convert a list into a string?", "How to convert a list into a tuple?", "How to convert a list into a set?"]
coding_questions = ["Implement a binary tree.", "Implement a linked list.", "Implement a stack.", "Implement a queue."]
behavioral_questions = ["How do you handle a pressuresome situation?", "Tell me about the toughest decision you've had to make in the past six months.", "Tell me about a major mistake you made, and what you did to correct it.", "Tell me about the last time a customer or co-worker got upset with you.", "Tell me about a time you knew you were right, but still had to follow directions or guidelines."]
technical_questions = ["What is recurssion?", "What’s the most challenging/exciting project you have done in the past two years?", "What kind of tech projects do you work on in your spare time?", "Tell me about the most difficult technical challenge you’ve encountered and how you resolved it.", "What technologies could you not live without?"]

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Practice buddy! I will help you sharpen your interview skills. You can practice questions by saying a category name, like Behavioral, Technical or Coding questions. What would you like to practice?"
        # ask this after user selects the category for the first time.
        # speak_output_return = "Welcome to Practice buddy! I will help you sharpen your interview skills. You can practice questions by saying a category name, like Behavioral, Technical or Coding questions. What would you like to practice?"
        # Here are a few things you should know: Your responses will be recorded for you to review during practice sessions. When you are done, say end recording. Let's get started!
        # ask_output = "You can practice questions by saying a category name, like Behavioral, Technical or Coding questions. What would you like to practice?"

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
        #retrieve the attribute
        attr = handler_input.attributes_manager.persistent_attributes
        category = attr['interview_category']

        speak_output = "Welcome back to Practice buddy. Want to keep practicing {category}? If yes, say next question or to switch say switch category!".format(category=category)
        # handler_input.response_builder.speak(speak_output)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Can you please say it again?")
                .response
        )
        # return handler_input.response_builder.response

class CaptureCategoryIntentHandler(AbstractRequestHandler):
    """Handler for CaptureCategoryIntent Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CaptureCategoryIntent")(handler_input)

    def handle(self, handler_input):
        # bringing in the slot values
        slots = handler_input.request_envelope.request.intent.slots

        #specifically extracting INTERVIEW_CATEGORY
        category = slots["INTERVIEW_CATEGORY"].value

        #saving the interview category in the "interview_category" persistent_attribute
        attributes_manager = handler_input.attributes_manager
        category_attributes = {
            "interview_category": category
        }
        attributes_manager.persistent_attributes = category_attributes
        attributes_manager.save_persistent_attributes()

        # type: (HandlerInput) -> Response
        question = " "

        if category is 'C programming language':
            question = random.choice(c_questions)
        elif category is 'C plus plus':
            question = random.choice(c_plus_plus_questions)
        elif category is 'coding':
            question = random.choice(coding_questions)
        elif category is 'behavioral':
            question = random.choice(behavioral_questions)
        elif category is 'technical':
            question = random.choice(technical_questions)
        elif category is 'python':
            question = random.choice(python_questions)
        elif category is 'java':
            question = random.choice(java_questions)
        else:
            question = random.choice(coding_questions)

        # question = python_questions[0]
        # speak_output = "Ok, Here you go - a question in {category}. ".format(category=category) + " " +  question + " " + "Say next question!"
        speak_output = "Ok, Here is a question. " +  question + " " + "When done, say next question or switch category!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .speak(question)
                # .ask(ask_output)
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

        if slots is not "":
            #specifically extracting INTERVIEW_CATEGORY
            category = slots["INTERVIEW_CATEGORY"].value

            #saving the interview category in the "interview_category" persistent_attribute
            attributes_manager = handler_input.attributes_manager
            category_attributes = {
                "interview_category": category
            }
            attributes_manager.persistent_attributes = category_attributes
            attributes_manager.save_persistent_attributes()

        # type: (HandlerInput) -> Response
        question = " "

        if category is 'C programming language':
            question = random.choice(c_questions)
        elif category is 'C plus plus':
            question = random.choice(c_plus_plus_questions)
        elif category is 'coding':
            question = random.choice(coding_questions)
        elif category is 'behavioral':
            question = random.choice(behavioral_questions)
        elif category is 'technical':
            question = random.choice(technical_questions)
        elif category is 'python':
            question = random.choice(python_questions)
        elif category is 'java':
            question = random.choice(java_questions)
        else:
            question = random.choice(coding_questions)

        speak_output = ""
        if slots is "":
            speak_output = "Ok, which category would you like?"
        else:
            # speak_output = "Ok, Here you go - a question in {category}. ".format(category=category) + " " +  question + " " + "When done, say next question or switch category!"
            speak_output = "Ok, Here is a question. " +  question + " " + "When done, say next question or switch category!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .speak(question)
                .ask("Say it again?")
                .response
        )

class AskNextQuestionIntentHandler(AbstractRequestHandler):
    """Handler for launch after the user have set the interview_category"""

    def can_handle(self, handler_input):

        # attr = handler_input.attributes_manager.persistent_attributes
        # attributes_are_present = ("interview_category" in attr)

        return ask_utils.is_intent_name("AskNextQuestionIntent")(handler_input)

    def handle(self, handler_input):

        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("interview_category" in attr)

        attr = handler_input.attributes_manager.persistent_attributes
        if attributes_are_present:
            category = attr['interview_category']

        # attr = handler_input.attributes_manager.persistent_attributes

        # extract persistent attributes and check if they are all present
        # attr = handler_input.attributes_manager.persistent_attributes
        # attributes_are_present = ("interview_category" in attr)

        # attr = handler_input.attributes_manager.persistent_attributes
        # category = attr['interview_category']

        # type: (HandlerInput) -> Response
        question = " "

        if category is 'C programming language':
            question = random.choice(c_questions)
        elif category is 'C plus plus':
            question = random.choice(c_plus_plus_questions)
        elif category is 'coding':
            question = random.choice(coding_questions)
        elif category is 'behavioral':
            question = random.choice(behavioral_questions)
        elif category is 'technical':
            question = random.choice(technical_questions)
        elif category is 'python':
            question = random.choice(python_questions)
        elif category is 'java':
            question = random.choice(java_questions)
        else:
            question = random.choice(coding_questions)

        # speak_output = "Here is a question in {category}. ".format(category=category) + " " +  question + " " + "When done, say next question or switch category!"
        speak_output = "Ok, Here is a question. " +  question + " " + "When done, say next question or switch category!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Say it again?")
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

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


#sb = SkillBuilder()
sb = CustomSkillBuilder(persistence_adapter=s3_adapter)
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureCategoryIntentHandler())
sb.add_request_handler(AskNextQuestionIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
