import os 
import time 
import pandas as pd 
import json 
import logging
import requests
from openai import OpenAI
from openai import RateLimitError
from dotenv import load_dotenv
from helpers.config import record_data_path, glo_data_path, buy_rent_path
from helpers.prompt_templates import property_all_template, property_not_all_template, user_details_confirmation_prompt, house_details_confirmation_prompt, extract_user_query_prompt


def load_openai_model():
    """ Prepare OpenAI model for use """
    load_dotenv()
    client = OpenAI(
        api_key = os.getenv("OPENAI_API_KEY"))
    return client

def get_completion_from_messages(
        messages: list ,
        function_description: list , 
        model: str = "gpt-3.5-turbo-1106",
        temperature: float = 0.0,
         ):
    """ Get completion from messages """
    openai = load_openai_model()
    for i in range(3):
        try:
            response = openai.chat.completions.create(
                model = model,
                messages = messages,
                temperature = temperature,
                functions = function_description,
                function_call = "auto",
            )
            return response.choices[0].message
        except RateLimitError as e:
            #log this error using logger 
            logging.error(f"RateLimitError: {e}")
            time.sleep(5)
            if i == 2:
                return {"content": "Thank you for visiting Glo realtors assistant. We are sorry for the inconvenience. Please try again later."}

def parse_query_results(prompt: str, model: str = "gpt-3.5-turbo-1106"):
    """ Summarize conversation """
    openai = load_openai_model()
    for i in range(3):
        try:
            response = openai.Completion.create(
                model = model,
                prompt = prompt,
                temperature = 0.0,
                max_tokens = 150,
            )
            return response.choices[0].message["content"]
        except RateLimitError as e:
            #log this error using logger 
            logging.error(f"RateLimitError: {e}")
            time.sleep(5)
            if i == 2:
                return {"content": "We are sorry for the inconvenience. Please try again later."}

def extract_user_query(messages: list):
    """ Extract key details from a list of messages """

    extract_user_query_prompt_template = f"{extract_user_query_prompt} ####{messages}####"
    response = parse_query_results(extract_user_query_prompt_template)

    return response


def get_list_property_info(property_type: str,furnished: str,service_type: str,number_of_bedrooms: str,amenities:str ,income: str,flag: bool):
    """ Get the property info provided by the user for renting"""
    if flag:
        return  f"Type: {property_type}\nFurnished: {furnished}\nService Type: {service_type}\nNumber of Bedrooms: {number_of_bedrooms}\nAmenities: {amenities}\nIncome: {income}\n"
    

def get_buy_rent_property_info(property_type:str, furnished: str, number_of_bedrooms: str, amenities: str, location: str, budget_range: str, flag: bool):
    """ Get the property info provided by the user for buying"""
    if flag:
        return  f"Type: {property_type}\nFurnished: {furnished}\nNumber of Bedrooms: {number_of_bedrooms}\nAmenities: {amenities}\nLocation: {location}\nBudget Range: {budget_range}\n"
    
def get_property_management_info(property_type: str, location: str, additional_info: str, estimated_income: str, flag: bool):
    """ Get the property info provided by the user for management"""
    if flag:
        return  f"Type: {property_type}\nLocation: {location}\nAdditional Info: {additional_info}\nEstimated Income: {estimated_income}\n"
    
def send_whatsapp_message(message: str):
    """ send whatsapp message : developers.facebook.com/"""
    FROM_PHONE_ID = os.getenv("FROM_PHONE_ID")
    TOKEN = os.getenv("WHATSAPP_TOKEN")
    TO_PHONE_ID = os.getenv("TO_PHONE_ID")

    print(FROM_PHONE_ID, TO_PHONE_ID)
    URL =  "https://graph.facebook.com/v13.0/"+FROM_PHONE_ID+"/messages"
    headers = {
        "Authorization": "Bearer "+TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": TO_PHONE_ID,
        "type": "text",
        "text": json.dumps({"preview_url": False, "body": message})

    }
    response = requests.post(URL, headers=headers, data=data)
   # Check if the request was successful (status code 200)
    if response.status_code == 200:
        logging.info(f"Successfully sent message: {message}")
    else:
        logging.error(f"Failed to send message: {message}, with status code: {response.status_code} and response: {response.text}")


def get_user_info(name: str, phone_number: str, email_address: str, confirmation_flag: bool, messages: list):
    """ Get the user info provided by the user """
    if confirmation_flag:
        key_details = extract_user_query(messages)
        user_info = {
            'Name': name,
            'Phone Number': phone_number,
            'Email Address': email_address,
            'User Query': key_details
        }

        csv_file_path = record_data_path
        if not os.path.exists(csv_file_path):
            user_info_df = pd.DataFrame([user_info])
            user_info_df.to_csv(csv_file_path, index=False)
        else:
            user_info_df = pd.read_csv(csv_file_path)
            #create a new dataframe and concat to the prev df
            new_user_info_df = pd.DataFrame([user_info])
            user_info_df = pd.concat([user_info_df, new_user_info_df], ignore_index=True)
            user_info_df.to_csv(csv_file_path, index=False)

        message = f"the user's name is {name} and his phone number is {phone_number} and his email address is {email_address} and his query is {key_details}"
        send_whatsapp_message(message)
        
        return f"the user's name is {name} and his phone number is {phone_number} and his email address is {email_address}"
    
def confirm_user_info(string_result: str):
    """ COnfirm the user info back to the user"""

    user_info_confimration_prompt_temmplate = f"{user_details_confirmation_prompt} ####{string_result}####"
    response = parse_query_results(user_info_confimration_prompt_temmplate)
    return response

def confirm_house_info(string_result: str):
    """ COnfirm the house info back to the user"""

    house_info_confimration_prompt_temmplate = f"{house_details_confirmation_prompt} ####{string_result}####"
    response = parse_query_results(house_info_confimration_prompt_temmplate)
    return response

def error_handling(exception: Exception):

    """ Handle errors that might occur during the conversation"""
    if "Incorrect API key provided" in str(exception).lower():
        return "Thank you for visiting Glo realtors website. We are sorry for the inconvenience. Please try again later."
    elif "you exceeded your current quota" in str(exception).lower():
        return "Thank you for visiting Glo realtors website. We are sorry for the inconvenience. Please try again later."
    elif "missing" and "required positional argument" in str(exception).lower():
        return "Looks like you have not provided all the required information."
    elif "'NoneType' object has no attribute 'get'" in str(exception):
        return "Thank you for visiting Glo realtors website. We are sorry for the inconvenience. Please try again later."
    else:
        pass

def find_n_property_by_location(location: str, glo: pd.DataFrame, buyrent_kenya: pd.DataFrame, n: int=10):
    """ Find n property by location"""


    # Convert query values to lowercase
    location = location.lower()

    glo['house_location'] = glo['house_location'].str.lower()

    glo_filtered = glo[
        (glo['house_location'].str.contains(location)) 
    ]

    # Sort the 'glo' DataFrame by house price
    glo_sorted = glo_filtered.sort_values(by='house_price')

    # Extract the house hrefs from 'glo' and add them to the result list
    result = glo_sorted['house_href'].head(n).tolist()

    # Check if we need to search in 'buyrent_kenya'
    remaining = n - len(result)
    if remaining > 0:
        # Convert 'buyrent_kenya' DataFrame column values to lowercase
        buyrent_kenya['house_location'] = buyrent_kenya['house_location'].str.lower()


        # Filter the 'buyrent_kenya' DataFrame based on the provided criteria, including the budget range
        kenya_filtered = buyrent_kenya[
            (buyrent_kenya['house_location'].str.contains(location))
        ]

        # Sort the 'buyrent_kenya' DataFrame by house price
        kenya_sorted = kenya_filtered.sort_values(by='house_price')

        # Extract additional house hrefs from 'buyrent_kenya' and add them to the result
        kenya_href_list = kenya_sorted['house_href'].head(remaining).tolist()
        result.extend(kenya_href_list)

    return result


def load_and_filter_data(glo_data_path: str, buy_rent_path: str, service_type: str, location: str, property_type: str, budget_range: str, number_of_bedrooms: str, n: int=10, furnished=None):
    """ Load and filter data """

    glo = pd.read_csv(glo_data_path).dropna()
    buyrent_kenya = pd.read_csv(buy_rent_path).dropna()
    buyrent_kenya = buyrent_kenya[buyrent_kenya['house_price'] != "Price not communicated"]

    if service_type == "Rent":
        glo = glo[glo['service_type'] == "For Rent"]
        buyrent_kenya = buyrent_kenya[buyrent_kenya['service_type'] == "Rent"]

    else:
        glo = glo[glo['service_type'] == "For Sale"]
        buyrent_kenya = buyrent_kenya[buyrent_kenya['service_type'] == "Sale"]

    if service_type == "Rent":
        if furnished == "furnished":
            glo = glo[glo['furnished'] == True]
            buyrent_kenya = buyrent_kenya[buyrent_kenya['furnished'] == True]
        else:
            glo = glo[glo['furnished'] == False]
            buyrent_kenya = buyrent_kenya[buyrent_kenya['furnished'] == False]        

    

    location = location.lower()
    property_type = property_type.lower()
    budget_range = float(budget_range.replace(',', '').replace('ksh', ''))
    number_of_bedrooms = int(number_of_bedrooms)

    glo['house_location'] = glo['house_location'].str.lower()
    glo['property_type'] = glo['property_type'].str.lower()

    lower_budget = budget_range - 100000
    upper_budget = budget_range + 100000



    glo_filtered = glo[
        (glo['house_location'].str.contains(location)) &
        (glo['bed_rooms'] == number_of_bedrooms) &
        (glo['property_type'].str.contains(property_type)) &
        (glo['house_price'] >= lower_budget) &
        (glo['house_price'] <= upper_budget)
    ]

    glo_sorted = glo_filtered.sort_values(by='house_price')

    result = glo_sorted['house_href'].head(n).tolist()
    remaining = n - len(result)

    if remaining > 0:
        buyrent_kenya['house_location'] = buyrent_kenya['house_location'].str.lower()
        buyrent_kenya['property_type'] = buyrent_kenya['property_type'].str.lower()
        buyrent_kenya['house_price'] = buyrent_kenya['house_price'].astype(float)

        kenya_filtered = buyrent_kenya[
            (buyrent_kenya['house_location'].str.contains(location)) &
            (buyrent_kenya['bed_rooms'] == number_of_bedrooms) &
            (buyrent_kenya['property_type'].str.contains(property_type)) &
            (buyrent_kenya['house_price'] >= lower_budget) &
            (buyrent_kenya['house_price'] <= upper_budget)
        ]

        kenya_sorted = kenya_filtered.sort_values(by='house_price')
        kenya_href_list = kenya_sorted['house_href'].head(remaining).tolist()
        result.extend(kenya_href_list)

    return result, glo, buyrent_kenya


def find_n_property_rent(property_type: str, furnished: str, number_of_bedrooms: str, amenities: str, location: str, budget_range: str, flag: str, service_type: str, n: int=10):
    """ Find n property for rent conditional on the user's query"""

    if flag:
        print(property_type, furnished, number_of_bedrooms, amenities, location, budget_range, flag, service_type)
        result, glo, buyrent_kenya = load_and_filter_data(glo_data_path, buy_rent_path, service_type, location, property_type, budget_range, number_of_bedrooms, n=10, furnished=furnished)
        if len(result)> 0:
            house_search_prompt_template = f"{property_all_template} {result} "
            response = parse_query_results(house_search_prompt_template)

            return response
        else:
            result = find_n_property_by_location(location, glo, buyrent_kenya, n=10)
            if result: 
                house_search_prompt_template = f"{property_not_all_template} {result} "
                response = parse_query_results(house_search_prompt_template)
                return response
            else:
                response = "Sorry we could not find any results matching your location, would you love to talk to one of our agents to help you find a house in your preferred location?"
                return response
            
def find_n_property_buy(property_type: str, number_of_bedrooms: str, amenities: str, location: str, budget_range: str, flag: str, service_type: str, n: int=10):
    """ Find n property for buy conditional on the user's query"""
    
    if flag:
        print(property_type, number_of_bedrooms, amenities, location, budget_range, flag, service_type)
        result, glo, buyrent_kenya = load_and_filter_data(glo_data_path, buy_rent_path, service_type, location, property_type, budget_range, number_of_bedrooms, n=10)
        if len(result)> 0:
            house_search_prompt_template = f"{property_all_template} {result} "
            response = parse_query_results(house_search_prompt_template)

            return response
        else:
            result = find_n_property_by_location(location, glo, buyrent_kenya, n=10)
            if result: 
                house_search_prompt_template = f"{property_not_all_template} {result} "
                response = parse_query_results(house_search_prompt_template)
                return response
            else:
                response = "Sorry we could not find any results matching your location, would you love to talk to one of our agents to help you find a house in your preferred location?"
                return response