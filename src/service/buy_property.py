import os 
import openai
import json 
import time 
import logging
from openai import RateLimitError
from helpers.config import buy_data_path
from helpers.function_descriptions import buy_property_function_descriptions
from helpers.prompt_templates import buy_system_prompt
from helpers.utils import get_completion_from_messages, find_n_property_buy, get_user_info, confirm_user_info, error_handling

class BuyingService:
    def __init__(self):
        self.path = buy_data_path
        self.messages = buy_system_prompt

    def reply_to_buy_property_queries(self, user_input):
        self.messages.append({'role': 'user', 'content': user_input})
        
        response = get_completion_from_messages(self.messages, buy_property_function_descriptions)
        if response.get('function_call'):
            function_called = response['function_call']['name']
            if function_called == "get_house_info":
                function_args = json.loads(response['function_call']['arguments'])

                available_functions = {
                    "get_house_info": find_n_property_buy,
                }
                try:
                    function_to_call = available_functions[function_called]
                    response = function_to_call(**function_args, service_type="Sale")
                except Exception as ex:
                    logging.error(f"Function Calling Error(find n property buy): {ex}")
                    response = error_handling(ex)


            elif function_called == "get_user_info":
                function_args = json.loads(response['function_call']['arguments'])

                available_functions = {
                    "get_user_info": get_user_info,
                }
                try:
                    function_to_call = available_functions[function_called]
                    string_result = function_to_call(**function_args, messages=self.messages)
                    response = confirm_user_info(string_result)
                except:
                    logging.error(f"Function Calling Error(confirm user info): {ex}")
                    response = error_handling(ex)


            else:
                response = "Unexpected behavior"
        else:
            response = response["content"]

        self.messages.append({'role': 'assistant', 'content': response})
        return response

