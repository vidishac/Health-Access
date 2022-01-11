"""
Objective: This program uses google APIs to intake a text field and return a website associated
           with it (if any). The intake, in our context, are the names of healthcare providers. 
           

Packages required:
    a. requests 
    b. json
    c. re

Other things to note:
    a. To increase accuracy, the program does a 3 stage search:
        1. Use google maps textsearch API to get details for a string
        2. Use the google maps textsearch API again to get the official name of the searched string 
            (from the results of 1)
        3. Use the place ID in the result of 2 on google maps details API to get the website of the place
"""

#Import required files
import requests
import json
import re

#Keys
API_KEY = 'AIzaSyABxu5Q65XqI2ndTkA58OMs75ahlumci10'
    
def hospital_website_2(hospital_name):    

    try:
        #Define API query
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
        search_url = base_url + hospital_name + '&key=' + API_KEY
        
        
        
        payload={}
        headers = {}
        
        response = requests.request("GET", search_url, headers=headers, data=payload)
        data = json.loads(response.content.decode('utf-8'))
        
        #part 2 (improvements)
        
        #Get the name from results, search again
        interim_name = data['results'][0]['name']
        search_url = base_url + interim_name + '&key=' + API_KEY
        response = requests.request("GET", search_url, headers=headers, data=payload)
        data = json.loads(response.content.decode('utf-8'))
        
        #Get the place_id from this part 2 search
        place_id = data['results'][0]['place_id']
        
        #Construct the query for the details API
        base_url_2 = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='
        website_search_url = base_url_2 + place_id + '&key=' + API_KEY
        response = requests.request("GET", website_search_url, headers=headers, data=payload)
        
        data_2 = json.loads(response.content.decode('utf-8'))
        
        #Now get the website and 3 more pieces of information
        
        #Website (info 1)
        try:
            website = data_2['result']['website']
        except:
            website = 'does not exist'
        
        #Rating (info 2)
        try:
            rating = data_2['result']['rating']
        except:
            rating = 'no ratings'
        
        #Whether open now (info 3)
        try:
            open = data_2['result']['opening_hours']['open_now']
        except:
            open = 'no information available'
        
        #Business status (info 4)
        try:
            business_status = data_2['result']['business_status']
        except:
            business_status = 'no information available'
        
        
        #Trim the website name (required for searching appointment page link)
        trimmed_website_1 = re.search(r'www.*.org',website)
        trimmed_website_2 = re.search(r'www.*.com',website)
        
        if trimmed_website_1 !=None:
            final_website = trimmed_website_1.group(0)
        elif trimmed_website_2 !=None:
            final_website = trimmed_website_2.group(0)
        else:
            final_website = 'website not found'
        
        return {'website':final_website,'rating':rating,'open':open,'url':website_search_url,
                'business status':business_status}
    
    except:
        return {'website':'website not found','rating':'website not found',
                'open':'website not found','url':'website not found',
                'business status':'website not found'}




        
    
    
