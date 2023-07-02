from time import sleep, strftime
import flightradar24 as fl
from bs4 import BeautifulSoup
import requests
import webbrowser
from colorama import Fore, Back, Style

api=fl.Api()


def get_key(val,dict):
    for key, value in dict.items():
         if val in value:
             return key
 
    return None

def get_aiport_iata(country):

    all_airports = api.get_airports()
    data = []

    for airport in all_airports['rows']:
        if airport["country"].lower() == country.lower():
            temp = {}
            temp["name"] = airport["name"]
            temp["iata"] = airport['iata']

            data.append(temp)
    return data



def get_airline_code(airline_name):
    all_airlines = api.get_airlines()
    results = []
    code = ''
    for airline in all_airlines['rows']:
        if airline["Name"].lower() == airline_name.lower():
            code = airline['Code']
    
    for airline in all_airlines['rows']:
        if airline["Name"].lower().find(airline_name.lower()) != -1:
            results.append(airline)

    if code != '':
        return code
    else:
        return results



def list_flights(arr_iata,dep_iata,year,month,date,hour):
    flights = []
    departure_time = []
    arrival_time = []
    base_url=f'https://www.flightstats.com/v2/flight-tracker/route/{arr_iata}/{dep_iata}/?year={year}&month={month}&date={date}&hour={hour}'
        
    res=requests.get(base_url)
    soup=BeautifulSoup(res.content,'html.parser')

    flights_data = soup.find_all('h2',class_='flights-list-bold-text flights-list-margined leftText')
    dept_time_data = soup.find_all('h2',class_='flights-list-bold-text flights-list-margined departureTimePadding')
    arr_time_data = soup.find_all('h2',class_='flights-list-light-text flights-list-margined')
           
    if len(flights_data) and len(dept_time_data) and len(arr_time_data) != 0:
        for flight in flights_data:
            flights.append(flight.text)

        for dep_time in dept_time_data:
            departure_time.append(dep_time.text)

        for arr_time in arr_time_data:
            arrival_time.append(arr_time.text)

        return flights, departure_time, arrival_time, base_url
    
    else:
        return None

def flight_status(flight_id,year,month,date):
    airline = flight_id.split()[0]   
    id = flight_id.split()[1]
    base_url=f'https://www.flightstats.com/v2/flight-tracker/{airline}/{id}?year=20{year}&month={month}&date={date}'
    print(base_url)
    res=requests.get(base_url)
    soup=BeautifulSoup(res.content,'html.parser')
    try:
        status=soup.find("div",class_='text-helper__TextHelper-sc-8bko4a-0 iicbYn').text
    except:
        status=soup.find("div",class_='text-helper__TextHelper-sc-8bko4a-0 iicbYn').text

            
    dep_city=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 efwouT')[0].text
    dep_airport=soup.find_all('div',class_='text-helper__TextHelper-sc-8bko4a-0 cHdMkI')[0].text
    
    arr_city=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 efwouT')[1].text
    arr_airport=soup.find_all('div',class_='text-helper__TextHelper-sc-8bko4a-0 cHdMkI')[1].text

    scheduled_dep_time=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[0].text
    actual_dep_time=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[1].text

    scheduled_arr_time=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[2].text
    actual_arr_time=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[3].text

    terminal_dep = soup.find_all("div",class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[0].text
    gate_dep = soup.find_all("div",class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[1].text

    terminal_arr = soup.find_all("div",class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[2].text
    gate_arr = soup.find_all("div",class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[3].text

    return status,arr_city,arr_airport,dep_city,dep_airport,scheduled_arr_time,actual_arr_time,scheduled_dep_time,actual_dep_time,terminal_arr,gate_arr,terminal_dep,gate_dep    
    

def main():
    print()
    print('''███████╗██╗     ██╗ ██████╗ ██╗  ██╗████████╗    ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗     
██╔════╝██║     ██║██╔════╝ ██║  ██║╚══██╔══╝    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗    
█████╗  ██║     ██║██║  ███╗███████║   ██║          ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝    
██╔══╝  ██║     ██║██║   ██║██╔══██║   ██║          ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗    
██║     ███████╗██║╚██████╔╝██║  ██║   ██║          ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║    
╚═╝     ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝          ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    
                                                                                                            ''')

    print()
    print(Fore.GREEN+"--"*40+Fore.RESET)
    
    print(Fore.CYAN+"""Tool By: Madhav :)"""+Fore.RESET)
    
    # print(Fore.GREEN+"--"*40+Fore.RESET)
    
    
    while True:
        print(Fore.GREEN+"--"*40+Fore.RESET)
        print(Fore.GREEN+"""
        1. List of flights on a particular day
        2. Flight status
        3. Track Flight
        
        99. Exit"""+Fore.RESET)
        print(Fore.GREEN+"--"*40+Fore.RESET)
        print()
        choice = int(input(Fore.YELLOW+"Enter your choice: "+Fore.RESET))

        if choice==1:
            arrival_airport_country = input(Fore.GREEN+"""Enter Country Name Of the Arrival Airport: """+Fore.RESET)
            arr_data = get_aiport_iata(arrival_airport_country)
            if len(arr_data)==0:
                print(Fore.RED+"--"*40+Fore.RESET)
                print(Fore.RED+"No Airport Found"+Fore.RESET)
                print(Fore.RED+"--"*40+Fore.RESET)

            else:
                print(Fore.YELLOW+"--"*40+Fore.RESET)

                print(Fore.YELLOW+f"                    IATA Code of Airports In {arrival_airport_country}"+Fore.RESET)
                print()
                
                for each in arr_data:
                    print(Fore.YELLOW+f"{each['name']}:{each['iata']}"+Fore.RESET)
                
            
                print(Fore.YELLOW+"--"*40+Fore.RESET)

            arrival_airport = input(Fore.GREEN+"Enter IATA Code Of Arrival Airport: "+Fore.RESET)
            
            departure_airport_country = input(Fore.GREEN+"""Enter Country Name Of the Departure Airport: """+Fore.RESET)
            dep_data = get_aiport_iata(departure_airport_country)

            if len(dep_data) == 0:
                print(Fore.RED+"--"*40+Fore.RESET)
                print(Fore.RED+"No Airport Found"+Fore.RESET)
                print(Fore.RED+"--"*40+Fore.RESET)
            else:
                print(Fore.YELLOW+"--"*40+Fore.RESET)
                
                print(Fore.YELLOW+f"                    IATA Code of Airports In {departure_airport_country}"+Fore.RESET)
                print()

                for each in dep_data:
                    print(Fore.YELLOW+f"{each['name']}:{each['iata']}"+Fore.RESET)
                
            
                print(Fore.YELLOW+"--"*40+Fore.RESET)
            
            dep_airport = input(Fore.GREEN+"Departure Airport: "+Fore.RESET)
            date = input(Fore.GREEN+"Date(YYYY-MM-DD): "+Fore.RESET)
            print()
            print(Fore.CYAN+"""Select Time Interval-
    1. 00:00 - 06:00
    2. 06:00 - 12:00
    3. 12:00 - 18:00
    4. 18:00 - 00:00"""+Fore.RESET)
            print()
            ask_time = int(input(Fore.YELLOW+"Enter your choice: "+Fore.RESET))
            if  ask_time == 1:
                hour = "0"
            elif ask_time == 2:
                hour = "6"
            elif ask_time == 3:
                hour = "12"
            else:
                hour = "18"


            flights,dep_time,arr_time, base_url = list_flights(arrival_airport,dep_airport,year=date.split('-')[0],month=date.split('-')[1],date=date.split('-')[2],hour=hour)
            if flights == None:
                print(Fore.RED+"--"*40+Fore.RESET)
                print(Fore.RED+"No Flights Found! Try using another time slot."+Fore.RESET)
                print(Fore.RED+"--"*40+Fore.RESET)
            else:
                print(Fore.GREEN+"--"*40+Fore.RESET)
                print(Fore.GREEN+"                    List Of Flights"+Fore.RESET)
                print(Fore.GREEN+"--"*40+Fore.RESET)


                for i in range(len(flights)):
                    print()
                    print(Fore.GREEN+f"{flights[i]}"+Fore.RESET)
                    print(Fore.GREEN+'--'*40+Fore.RESET)
                    print(Fore.GREEN+f'Departure Time:{dep_time[i]}'+Fore.RESET)
                    print(Fore.GREEN+f'Arrival Time:{arr_time[i]}'+Fore.RESET)
                    print(Fore.GREEN+'--'*40+Fore.RESET)
                
                more_choice = input("Do you want to see more flights?(Y/n):")
                print(more_choice)
                if more_choice.lower() in ("",'\n','y'):
                    print(more_choice)
                    print(base_url)
                    webbrowser.open(base_url)

                sleep(2)
        
        elif choice == 2:
            print()
            airline_name = input(Fore.CYAN+"Enter Airline Name: "+Fore.RESET)
            flight_id = input(Fore.CYAN+"Enter Flight Id: "+Fore.RESET)
            result = get_airline_code(airline_name)
            if type(result) == str:
                code = result
            else:
                print(Fore.GREEN+"--"*40+Fore.RESET)
                print(Fore.GREEN+f"                    List Of Airlines Containing {airline_name}"+Fore.RESET)
                print(Fore.GREEN+"--"*40+Fore.RESET)
                for i in result:
                    print(Fore.GREEN+f"Airline: {i['Name']}"+Fore.RESET)
                continue
                
            date = strftime('%X %x %Z').split()[1].split('/')[1]
            month = strftime('%X %x %Z').split()[1].split('/')[0]
            year = strftime('%X %x %Z').split()[1].split('/')[2]
            data = flight_status(code + " " + flight_id,year,month,date)
            print(Fore.GREEN+"--"*40+Fore.RESET)

            print(Fore.GREEN+"                    Flight Status"+Fore.RESET)
            print(Fore.GREEN+f"Status: {data[0]}"+Fore.RESET)
            print(Fore.GREEN+f"Arrival City: {data[1]}"+Fore.RESET)
            print(Fore.GREEN+f"Arrival Airport: {data[2]}"+Fore.RESET)
            print(Fore.GREEN+f"Departure City: {data[3]}"+Fore.RESET)
            print(Fore.GREEN+f"Departure Airport: {data[4]}"+Fore.RESET)
            print(Fore.GREEN+f"Scheduled Arrival Time: {data[5]}"+Fore.RESET)
            print(Fore.GREEN+f"Actual Arrival Time: {data[6]}"+Fore.RESET)
            print(Fore.GREEN+f"Scheduled Departure Time: {data[7]}"+Fore.RESET)
            print(Fore.GREEN+f"Actual Departure Time: {data[8]}"+Fore.RESET)
            print(Fore.GREEN+f"Arrival Terminal: {data[9]}"+Fore.RESET)
            print(Fore.GREEN+f"Arrival Gate: {data[10]}"+Fore.RESET)
            print(Fore.GREEN+f"Departure Terminal: {data[11]}"+Fore.RESET)
            print(Fore.GREEN+f"Departure Gate: {data[12]}"+Fore.RESET)

            print(Fore.GREEN+"--"*40+Fore.RESET)

            sleep(1)

        elif choice == 3:
            airline_name = input(Fore.CYAN+"Enter Airline Name: "+Fore.RESET)
            flight_id = input(Fore.CYAN+"Enter Flight ID: "+Fore.RESET)
            result = get_airline_code(airline_name)
            if type(result) == str:
                code = result
            else:
                print(Fore.GREEN+"--"*40+Fore.RESET)
                print(Fore.GREEN+f"                    List Of Airlines Containing {airline_name}"+Fore.RESET)
                print(Fore.GREEN+"--"*40+Fore.RESET)
                for i in result:
                    print(Fore.GREEN+f"Airline: {i['Name']}"+Fore.RESET)
                continue
            
            webbrowser.open(f"https://www.flightradar24.com/{code}{flight_id}")
            sleep(3)

            

        elif choice == 99:            
            print(Fore.CYAN+"Good Bye."+Fore.RESET)
            break
        
if __name__=="__main__":
    main()
