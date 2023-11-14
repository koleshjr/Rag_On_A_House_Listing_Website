#create function descriptions for listing a property
list_property_function_descriptions = [
    {
        "name": "get_property_info",
        "description": "call this function only when the flag is true",
        "parameters": {
            "type": "object",
            "properties": {

                "property_type": {
                    "type": "string",
                    "description":  "the type of property can either be a house, apartment, townhouse or a villa  and should not be null",
                },

                "furnished": {
                    "type": "string",
                    "description": "flag to indicate if the property is furnished  or not  and should not be null",
                },

                "service_type": {
                    "type": "string",
                    "description":  "the type of service can either be sale or rent and should not be null",
                },    

                "number_of_bedrooms": {
                    "type": "string",
                    "description": "number of bedrooms in the property and should not be null",
                },     

                "amenities": {
                    "type": "string",
                    "description": "amenities present in the property and should not be null",
                },

                "income": {
                    "type": "string",
                    "description": "estimated income from the property in kenya shillings and should not be null",
                },

                "flag":{
                    "type": "boolean",
                    "description": "flag to indicate that the user is satisfied with the captured information"
                }
            },
            "required": ["property_type", "furnished", "service_type", "number_of_bedrooms", "amenities", "income", "flag"],
        },
    },

     {
        "name": "get_user_info",
        "description": " call this function only when the confirmation flag is true",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "user's personal name and should not be null",
                },                

                "phone_number": {
                    "type": "string",
                    "description": "user's phone number and should not be null",
                },

                "email_address": {
                    "type": "string",
                    "description": "Users email address and should not be null",
                },

                "confirmation_flag":{
                    "type": "boolean",
                    "description": "flag to indicate if the user has confirmed that the information is correct"
                },


            },
            "required": ["name", "phone_number", "email_address", "confirmation_flag"],
        },
    }    
]

# create function descriptions for the buy property engine
buy_property_function_descriptions = [
    {
        "name": "get_house_info",
        "description": "call this function only when the flag is true",
        "parameters": {
            "type": "object",
            "properties": {
               "property_type": {
                    "type": "string",
                    "description": "the type of property can either be a house, apartment, townhouse or a villa and should not be null",
                },           

                "number_of_bedrooms": {
                    "type": "string",
                    "description": "number of bedrooms in the property and should not be null",
                },

                "amenities": {
                    "type": "string",
                    "description": "amenities present in the property and should not be null",
                },


                "location": {
                    "type": "string",
                    "description": "preferred location for the user and should not be null",
                },

                "budget_range": {
                    "type": "string",
                    "description": "Users budget range in kenya shillings and should not be null",
                },

                "flag":{
                    "type": "boolean",
                    "description": "flag to indicate if the user has given all the required information"
                }
            },
            "required": ["property_type", "number_of_bedrooms", "amenities", "location", "budget_range", "flag"],
        },
    },

    {
        "name": "get_user_info",
        "description": " call this function only when the confirmation flag is true",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "user's personal name and should not be null",
                },                

                "phone_number": {
                    "type": "string",
                    "description": "user's phone number and should not be null",
                },

                "email_address": {
                    "type": "string",
                    "description": "Users email address and should not be null",
                },

                "confirmation_flag":{
                    "type": "boolean",
                    "description": "flag to indicate if the user has confirmed that the information is correct"
                },


            },
            "required": ["name", "phone_number", "email_address", "confirmation_flag"],
        },
    }    
]

# create function descriptions for the rent property engine

rent_property_function_descriptions = [
    {
        "name": "get_house_info",
        "description": "call this function only when the flag is true",
        "parameters": {
            "type": "object",
            "properties": {
               "property_type": {
                    "type": "string",
                    "description": "the type of property can either be a house, apartment, townhouse, commercial_property etc and should not be null",
                },       

                "furnished": {
                    "type": "string",
                    "description": "flag to indicate if the property is furnished or not and should not be null",

                },      

                "number_of_bedrooms": {
                    "type": "string",
                    "description": "number of bedrooms in the property and should not be null",
                },

                "amenities": {
                    "type": "string",
                    "description": "amenities present in the property and should not be null",
                },


                "location": {
                    "type": "string",
                    "description": "preferred location for the user and should not be null",
                },

                "budget_range": {
                    "type": "string",
                    "description": "Users budget range in kenya shillings and should not be null",
                },

                "flag":{
                    "type": "boolean",
                    "description": "flag to indicate if the user has given all the required information"
                }
            },
            "required": ["property_type", "furnished", "number_of_bedrooms", "amenities", "location", "budget_range", "flag"],
        },
    },

    {
        "name": "get_user_info",
        "description": " call this function only when the confirmation flag is true",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "user's personal name and should not be null",
                },                

                "phone_number": {
                    "type": "string",
                    "description": "user's phone number and should not be null",
                },

                "email_address": {
                    "type": "string",
                    "description": "Users email address and should not be null",
                },

                "confirmation_flag":{
                    "type": "boolean",
                    "description": "flag to indicate if the user has confirmed that the information is correct"
                },


            },
            "required": ["name", "phone_number", "email_address", "confirmation_flag"],
        },
    }    
]


property_management_function_descriptions = [
    {
        "name": "get_house_info",
        "description": "call this function only when the flag is true",
        "parameters": {
            "type": "object",
            "properties": {
                "property_type": {
                    "type": "string",
                    "description": "the type of property can either be a house, apartment, townhouse, commercial_property etc and should not be null",
                },                

                "location": {
                    "type": "string",
                    "description": "preferred location for the user and should not be null",
                },

                "additional_info": {
                    "type": "string",
                    "description": "additional information about the property such as the number of rooms or the size, amenities present in the property and features of the property",
                },

                "estimated_income": {
                    "type": "string",
                    "description": "estimated income from the property in kenya shillings and should not be null",
                },

                "flag":{
                    "type": "boolean",
                    "description": "flag to indicate if the user has given all the required information"
                }
            },
            "required": ["property_type", "location", "additional_info", "estimated_income", "flag"],
        },
    },

    {
        "name": "get_user_info",
        "description": " call this function only when the confirmation flag is true",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "user's personal name and should not be null",
                },                

                "phone_number": {
                    "type": "string",
                    "description": "user's phone number and should not be null",
                },

                "email_address": {
                    "type": "string",
                    "description": "Users email address and should not be null",
                },

                "confirmation_flag":{
                    "type": "boolean",
                    "description": "flag to indicate if the user has confirmed that the information is correct"
                },


            },
            "required": ["name", "phone_number", "email_address", "confirmation_flag"],
        },
    }    
]