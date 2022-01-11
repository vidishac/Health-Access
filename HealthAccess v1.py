"""
HealthAccess app main file

1. User enters street address
2. User chooses emergency/non emergency/Know your wellbeing
3. If emergency, user gets a table of ranked hospital list
4. If non emergency, same as above but with additional information about each hospital
5. If Know your wellbeing, user chooses a)AQI information b)sleep hours comparison
    a) AQI gives pittsburgh's current AQI information
    b) Sleep hours comparison shows user's sleep and user income againt national average


Programs used:
    1. hospitals_list.py
    2. travel_time_finder.py
    3. hospital_website_finder_2.py
    4. appt_page_link.py
    5. average_sleep.py
    6. aqi.py

Datasets required in user directory:
    1. sleep_hours.csv
    2. pennsylvania_PM2.5_historical_data.csv

Libraries required:
    1. re
    2. json
    3. pandas
    4. bs4
    5. matplotlib
    6. seaborn
    7. requests
    8. datetime

"""

#Importing supporting files
import travel_time_finder as ttf
import hospital_website_finder_2 as hwf
import appt_page_link as apl
import hospitals_list as hl
import average_sleep as asl
import aqi_info as aq


#Importing libraries
import pandas as pd


#Developer setting (# of results the user should see)
no_of_results = 10
hospital_sample = 70

#Running the hospitals list code to generated the necessary hospital_list_with_keywords.csv
hl.hospital_list()


#Ask for user input
user_address = input('Please enter your street address: ')

check_1 = 0
while check_1 ==0:
    try:
        type = int(input('Please choose: 1 for emergency, 2 for non-emergency, 3 for know your wellbeing: '))
        if type not in [1,2,3]:
            print('Please choose an integer among 1,2,3')
        else:
            check_1 =1
    except:
        print('Please enter an integer that is 1,2 or 3')


#Formatting and cleaning the hospital dataset 
if type !=3:
    #Import the full list of hospitals, categories and keywords
    hospital_list = pd.read_csv('hospital_list_with_keywords.csv')
    hospital_list = hospital_list.dropna(subset = ['Keywords'])          #Drop hospitals with blank keywords
    hospital_list_sample  = hospital_list.sample(hospital_sample)        #Because of limited computing power
    
    
    #Creating a dataframe of just keywords
    matched_cat_1 = hospital_list_sample[['Keywords_1']]
    matched_cat_1 = matched_cat_1.drop_duplicates()
    matched_cat_1=matched_cat_1.rename(columns = {'Keywords_1':'Keywords'})
    
    matched_cat_2 = hospital_list_sample[['Keywords_2']]
    matched_cat_2 = matched_cat_2.dropna()
    matched_cat_2 = matched_cat_2.drop_duplicates()
    matched_cat_2=matched_cat_2.rename(columns = {'Keywords_2':'Keywords'})
    
    #Append the 2 keywords dataframe
    matched_cat = pd.concat([matched_cat_1, matched_cat_2], ignore_index=True)
    
    matched_cat.drop_duplicates(subset = ['Keywords'],keep = 'first', inplace=True, ignore_index = True)
    
    
    
    #Calculating distances from user location to each hospital in our sampled list
    travel_time_text = []
    travel_time_numeric = []
    
    for i in range(0,len(hospital_list_sample)):  
            time = ttf.time(user_address,hospital_list_sample['Organization Name'].iloc[i])
            travel_time_text.append(time['text'])
            travel_time_numeric.append(time['value'])
            
    hospital_list_sample['travel time text'] = travel_time_text    
    hospital_list_sample['travel time value'] = travel_time_numeric 
            
    #Dropping invalid values
    hospital_list_sample = hospital_list_sample.loc[hospital_list_sample['travel time value'] !=-999]

    #Creating a non duplicated file for emergency 
    hospital_list_sample_2 = hospital_list_sample[['Organization Name','Address','Tel-no',
                                                   'travel time value','travel time text']]
    hospital_list_sample_2 = hospital_list_sample_2.drop_duplicates()    
    

if type == 1:       #Emergency services
    
    #Sort on travel time
    hospital_list_sample_2 = hospital_list_sample_2.sort_values('travel time value')
    
    #Exporting result csv
    choice = []
    for i in range(0,len(hospital_list_sample_2)):
        choice.append(i+1)
    
    hospital_list_sample_2['choice #'] = choice
    cols = ['choice #','Organization Name','Tel-no','travel time text','Address']

    user_display_emergency = hospital_list_sample_2.head(no_of_results)    
    user_display_emergency.to_csv('emergency_output.csv',columns = cols, index = False)
    
    
    
    result_headings = ('{:7s}{:^50s}{:^20s}'.format('Choice #','Hospital Name','Travel time'))
    
    print(result_headings)
    for i in range(0,no_of_results):
        print('{:1d}{:>50s}{:>20s}'.format(i+1,hospital_list_sample_2['Organization Name'].iloc[i],
                                           hospital_list_sample_2['travel time text'].iloc[i]))
        
    
if type == 2:       #Non emergency services
    
    #Give user a set of keywords to choose from
    print(matched_cat['Keywords'])
    user_category = int(input('Please choose a category of care from the given list: '))
    
    #Filter based on user choice
    filtered_hospital_list_1 = hospital_list_sample.loc[hospital_list_sample['Keywords_1'] == 
                                                      matched_cat['Keywords'].iloc[user_category]]

    filtered_hospital_list_2 = hospital_list_sample.loc[hospital_list_sample['Keywords_2'] == 
                                                      matched_cat['Keywords'].iloc[user_category]]
    
    filtered_hospital_list = pd.concat([filtered_hospital_list_1, filtered_hospital_list_2], 
                                                                   ignore_index=True)

    filtered_hospital_list = filtered_hospital_list.drop_duplicates(subset = ['Organization Name'])
    
    #Sort on travel time
    filtered_hospital_list = filtered_hospital_list.sort_values('travel time value')    
    user_display = filtered_hospital_list.head(no_of_results)
    
    #Create a list of hospital names
    hosp_names = []
    for i in range(0,len(user_display)):
        hosp_names.append(user_display['Organization Name'].iloc[i])
    
    #Loop through each name to get website, open info, rating and business status
    websites=[]
    open_info=[]
    rating =[]
    business_status=[]
    for name in hosp_names:
        websites.append(hwf.hospital_website_2(name)['website'])
        open_info.append(hwf.hospital_website_2(name)['open'])
        rating.append(hwf.hospital_website_2(name)['rating'])
        business_status.append(hwf.hospital_website_2(name)['business status'])

    
    #Loop through each website to get appointmment page link
    appt_urls = []
    for site in websites:
        appt_urls.append(apl.appt_page(site)['appt_link'])
    
    
    #Add the information to the dataframe
    user_display['website'] = websites
    user_display['appointment page'] = appt_urls
    user_display['average ratings'] = rating
    user_display['open now?'] = open_info
    user_display['status'] = business_status
    
    
    
    #Exporting result csv
    choice_2 = []
    for i in range(0,len(user_display)):
        choice_2.append(i+1)
    
    user_display['choice #'] = choice_2
    cols_2 = ['choice #','Organization Name','Tel-no','travel time text',
            'average ratings','open now?','website','appointment page','status']
    
    user_display.to_csv('non-emergency_output.csv',columns = cols_2, index = False)
    
    
    
    result_headings = ('{:7s}{:^50s}{:^20s}{:>40s}'.
                       format('Choice #','Hospital Name','Travel time','appointment page'))
    
    
    
    print(result_headings)
    for i in range(0,len(user_display)):
        print('{:1d}{:>50s}{:>20s}{:>40s}'.format(i+1,user_display['Organization Name']
                                                  .iloc[i],user_display['travel time text'].iloc[i],
                                                  user_display['appointment page'].iloc[i]))

    
if type == 3:       #Know your wellbeing
    
    #Ask for the choice between the sub-options
    
    check_2 = 0
    while check_2 ==0:
        try:
            user_choice = int(input('Please choose 1 for AQI information or 2 for your sleep hours comparison: '))
            if user_choice not in [1,2]:
                print('Please choose 1 or 2')
            else:
                check_2 =1
        except:
            print('Please enter an integer that is 1 or 2')


    if user_choice ==2:
        asl.sleep_compare()
    
    if user_choice ==1:
        aq.main()
        
        
    
    
        
        
    
    
        
    
        
    
        
        
    
    
                                                                                             
