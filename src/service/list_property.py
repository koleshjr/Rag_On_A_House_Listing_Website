import json 
import logging
from helpers.function_descriptions import list_property_function_descriptions
from helpers.prompt_templates import list_system_prompt
from helpers.utils import get_completion_from_messages, get_list_property_info, get_user_info, confirm_house_info, confirm_user_info, error_handling


class ListingService:
    def __init__(self):
        self.messages = list_system_prompt

    def reply_to_list_property_inquiries(self, user_input):
        self.messages.append({'role': 'user', 'content': user_input})
        response = get_completion_from_messages(self.messages, list_property_function_descriptions)

        if response.get('function_call'):
            function_called = response['function_call']['name']
            if function_called == "get_property_info":
                function_args = json.loads(response['function_call']['arguments'])

                available_functions = {
                    "get_property_info": get_list_property_info,
                }
                try: 
                    function_to_call = available_functions[function_called]
                    string_result = function_to_call(**function_args)
                    response = confirm_house_info(string_result)   
                except Exception as ex:
                    logging.error(f"Function Calling Error(confirm house info): {ex}")
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
                except Exception as ex:
                    logging.error(f"Function Calling Error(confirm user info): {ex}")
                    response = error_handling(ex)

            else:
                response = "Unexpected behavior"
        else:
            response = response["content"]

        self.messages.append({'role': 'assistant', 'content': response})
        return response


