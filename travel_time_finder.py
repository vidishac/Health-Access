"""
Objective: This program takes in 2 parameters a)User's location b)Destination location
           and uses Google Map's API to calculate the distance between the 2 locations
           

Packages required:
    a. requests (should already be there)
    b. json (should already be there)

Other things to note:
    a. The API KEY used is the author's google cloud API key.
    
"""

#Import required files
import requests
import json
    
#Keys
API_KEY = 'AIzaSyABxu5Q65XqI2ndTkA58OMs75ahlumci10'
    
    
#Travel time function
def time(x,y):
        try:
            #Base API url
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
            
            #Adding parameters to the API url query
            search_address = url + 'origins=' + x + '&destinations=' + y \
                                    + '&units=imperial&key=' + API_KEY
            
            payload={}
            headers = {}
            
            response = requests.request("GET", search_address, headers=headers, data=payload)
            data = json.loads(response.content.decode('utf-8'))
            
            #Getting relevant parts of the returned dict
            travel_time_raw = data['rows'][0]['elements'][0]
            
            #Sometimes, google maps cannot find the text query 
            if travel_time_raw['status'] == 'NOT_FOUND':
                travel_time = {'text': 'not found', 'value': -999}
                
            else:   
                travel_time = travel_time_raw['duration']
            
            return travel_time
            
        except:
            travel_time = {'text': 'not found', 'value': -999}
            return travel_time
        
    


    
        

