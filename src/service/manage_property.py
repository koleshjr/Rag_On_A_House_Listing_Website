import os 
import openai
import json 
import time 
import logging
from openai.error import RateLimitError
from helpers.function_descriptions import property_management_function_descriptions
from helpers.prompt_templates import property_management_system_prompt
from helpers.utils import get_completion_from_messages,get_property_management_info, get_user_info, confirm_house_info, confirm_user_info, error_handling

class PropertyManagementService:
    def __init__(self):
        self.messages = property_management_system_prompt

    def reply_to_property_management_inquiries(self, user_input):
        self.messages.append({'role': 'user', 'content': user_input})
        
        try:
            response = get_completion_from_messages(self.messages,property_management_function_descriptions)

            if response.get('function_call'):
                function_called = response['function_call']['name']
                if function_called == "get_property_info":
                    function_args = json.loads(response['function_call']['arguments'])

                    available_functions = {
                        "get_property_info": get_property_management_info,
                    }
                    function_to_call = available_functions[function_called]
                    string_result = function_to_call(**function_args)
                    response = confirm_house_info(string_result)

                elif function_called == "get_user_info":
                    function_args = json.loads(response['function_call']['arguments'])

                    available_functions = {
                        "get_user_info": get_user_info,
                    }
                    function_to_call = available_functions[function_called]
                    string_result = function_to_call(**function_args, messages=self.messages)
                    response = confirm_user_info(string_result)

                else:
                    response = "Unexpected behavior"
            else:
                response = response["content"]

            self.messages.append({'role': 'assistant', 'content': response})
            return response

        except RateLimitError as ex:
            logging.error(f"Rate Limit Error: {ex}")
            error_handling(ex)