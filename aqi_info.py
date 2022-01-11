"""
Objective: This program displays data on current air quality indicator levels in Pittsburgh
by scraping https://aqicn.org/city/usa/pennsylvania/allegheny/parkway-east/ and shows the
category of air quality along with a health warning. 

In addition, it takes the CSV file pennsylvania_PM2.5_historical_data.csv as input 
(obtained from https://aqicn.org/data-platform/register/) and graphs monthly averages of 
Air Quality Index (AQI) (based on last six months’ data). This graph also shows the current 
maximum AQI in Pittsburgh. 

Packages required:
    a. requests 
    b. BeautifulSoup
    c. pandas
    d. re
    e. matplot.lib
    f. datetime
    

"""



def main():

    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import re
    import matplotlib.pyplot as plt
    from datetime import datetime
    
    
    
    httpString = "https://aqicn.org/city/usa/pennsylvania/allegheny/parkway-east/"
    
    page = requests.get(httpString)
    
    # Scraping the webpage
    
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
    
    # Find the required tag
    
    # Storing current PM2.5 AQI
    pm_aqi = soup.find_all(id = "cur_pm25")[0].get_text() 
    
    print("\nCurrent PM2.5 AQI is {}".format(pm_aqi))
    
    # Storing current O3 AQI
    pm_o3 = soup.find_all(id = "cur_o3")[0].get_text() 
    
    print("Current O3 AQI is {}".format(pm_o3)) 
    
    # Storing current NO2 AQI
    pm_no2 = soup.find_all(id = "cur_no2")[0].get_text() 
    
    print("Current NO2 AQI is {}".format(pm_no2))
    
    # Storing the category in which the highest AQI (max(pm_aqi, pm_o3, pm_no2)) lies
    
    aqi_info = soup.find_all(id = "aqiwgtinfo") 
    
    print("\nThe current AQI is '{}' as per WHO standards.".format(aqi_info[0].get_text()))
    
    # Storing health warnings for every AQI category in a dict
    
    cautionary_notes = {"Good":"None", 
                        "Moderate": "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.",
                        "Unhealthy for Sensitive Groups":"Active children and adults, and people with respiratory \
                            disease, such as asthma, should limit prolonged outdoor exertion.",
                        "Unhealthy":"Active children and adults, and people with respiratory disease, such as asthma,\
                            should avoid prolonged outdoor exertion; everyone else, especially children, should limit\
                                prolonged outdoor exertion",
                        "Very Unhealthy":"Active children and adults, and people with respiratory disease,\
                            such as asthma, should avoid all outdoor exertion; everyone else, especially children,\
                                should limit outdoor exertion.",
                        "Hazardous":"Everyone should avoid all outdoor exertion"}
        
    
    # If air quality is good, no warning is displayed. Otherwise every other category displays
    # an associate warning
        
    if aqi_info[0].get_text() != "Good":
        print("\n{}".format(cautionary_notes[aqi_info[0].get_text()]))
        
    
    ## Reading and cleaning csv file containing historical AQI data for Pittsburgh ##
    
    data = pd.read_csv('pennsylvania_PM2.5_historical_data.csv')
    
    # Keeping only 'date' ,'pm25' ,'o3', 'no2' columns
    
    data = data[['date', 'pm25', 'o3', 'no2']]
    
    # Extracting month and year from dates
    
    def month(d) :
        x = re.search(r'/[0-9]+/',d)
        return x.group(0).strip('/')
        
        
    data["Month"] = data["date"].apply(month)
    
    f = lambda x: float(x)
       
    data["Month"] = data["Month"].apply(f)
    
    def year(d) :
        x = re.search(r'^[0-9]+/',d)
        return x.group(0).strip('/')
            
    data["Year"] = data["date"].apply(year)
    
      
    data["Year"] = data["Year"].apply(f)
    
    # Restricting data to year 2021
    
    a = data["Year"] == 2021
    
    data = data.loc[a]
    
    
    # Removing missing values from AQI data and converting to float values

    PM25 = data[["date","pm25","Month"]]
    PM25 = PM25.loc[PM25["pm25"]!=' ']
    PM25["pm25"] = PM25["pm25"].apply(f)
    PM25_month = PM25.groupby(["Month"],as_index = False).mean()
    
    O3 = data[["date","o3","Month"]]
    O3 = O3.loc[O3["o3"]!=' ']
    O3["o3"] = O3["o3"].apply(f)
    O3_month = O3.groupby(["Month"],as_index = False).mean()
    
    NO2 = data[["date","no2","Month"]]
    NO2 = NO2.loc[NO2["no2"]!=' ']
    NO2["no2"] = NO2["no2"].apply(f)
    NO2_month = NO2.groupby(["Month"],as_index = False).mean()
    
    #AQI graph
    
    def plotter():
        plt.title("Monthly Average of Air Quality Index in Pittsburgh")
        plt.xlabel("Month")
        plt.ylabel("AQI")
        month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct", "Nov", "Dec"]
        plt.xticks(range(1,13),month_labels)
        plt.plot(PM25_month["Month"],PM25_month["pm25"], color = "Red", label="PM2.5")
        plt.plot(O3_month["Month"],O3_month["o3"], color = "Darkgreen", label= "O3")
        plt.plot(NO2_month["Month"],NO2_month["no2"], color = "Blue", label="NO2")
        
        # Plotting current AQI
        plt.scatter(datetime.now().month,float(max(pm_aqi, pm_o3, pm_no2)), color = "Black", label = "Current AQI")    
        
        plt.legend()
        plt.savefig('AQI.pdf')
        plt.show()
        
    
    plotter()
    
    
if __name__ == "__main__":
    main()    
    
    









