import os 
import openai
import json 
import time 
import logging
from openai.error import RateLimitError
from helpers.config import rent_data_path
from helpers.function_descriptions import rent_property_function_descriptions
from helpers.prompt_templates import rent_system_prompt
from helpers.utils import get_completion_from_messages, find_n_property_rent, get_user_info, confirm_user_info,error_handling


class RentingService:
    def __init__(self):
        self.path = rent_data_path
        self.messages = rent_system_prompt

    def reply_to_rent_inquiries(self, user_input):
        self.messages.append({'role': 'user', 'content': user_input})

        try:
            response = get_completion_from_messages(self.messages, rent_property_function_descriptions)

            if response.get('function_call'):
                function_called = response['function_call']['name']
                if function_called == "get_house_info":
                    function_args = json.loads(response['function_call']['arguments'])

                    available_functions = {
                        "get_house_info": find_n_property_rent,
                    }
                    function_to_call = available_functions[function_called]
                    response = function_to_call(**function_args, service_type="Rent")

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