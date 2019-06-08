import googlemaps
import datetime
import pandas as pd
import matplotlib.pyplot as plt

gmaps = googlemaps.Client(key='INSERT_YOUR_API_KEY_HERE')

geocode_home = 'HOME_ADDRESS'
geocode_school = 'Av. Horácio Macedo, 1749-1577 - Cidade Universitária da Universidade Federal do Rio de Janeiro'
#generating the 48 instants of time (every 30 minutes of the day)
time_range = pd.date_range('2019-6-10', '2019-6-11', periods=49)
time_range = time_range[:-1]
#dict to create the dataFrame. Format: {'monday':[traffic_times], 'tuesday':[traffic_times]....}
dict = {}
#since I'm using the future time in June2019 (10-14) to generate the data, this dictionary co-relates day number to weekday
number_to_weekday = {10:'Monday', 11:'Tuesday', 12:'Wednesday', 13:'Thursday', 14:'Friday'}


#10 = monday, 14= friday
for day in range(10, 15):
    traffic_times = []
    #varying every hour in a day
    for hour in range(0, 23+1):
        #in every hour, set minutes to 00 and to 30
        for minutes in range(0, 31, 30):
            #time used on the directions function
            time = datetime.datetime(2019,6,day,hour,minutes,0,0)
            #gathering data from Google's directionsApi. I don't want tolls, LoL
            home_to_school = gmaps.directions(geocode_school, geocode_home, mode='driving', units='metric', departure_time=time, avoid='tolls')
            #getting trip time in seconds
            traffic_time = home_to_school[0]['legs'][0]['duration_in_traffic']['value']
            #appending each time into the "this weekday" list
            traffic_times.append(traffic_time)
            #log
            if(minutes == 30):
                print ("Done {} {}:{}".format(number_to_weekday[day], hour, minutes))
            else:
                print ("Done {} {}:0{}".format(number_to_weekday[day], hour, minutes))

    #Transforming time stamps from seconds to minutes
    for index in range(len(traffic_times)):
        traffic_times[index] = traffic_times[index]/60
    #adding each 'day':[traffic_times] to the dict before it iterates into the next day
    dict[number_to_weekday[day]] = traffic_times

#creating the dataFrame
dataFrame = pd.DataFrame (dict, index=time_range)
#log
print("Data Frame: \n\n")
print (dataFrame)

#Setting the plotting variables
ax = dataFrame.plot(title='Traffic Time Values')
ax.set_xlabel("Time of day")
ax.set_ylabel("Time in traffic (minutes)")
#plotting
plt.show()
