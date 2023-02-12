import os
import requests
def get_lat_lon(city):
    city=city.strip().lower()
    url="https://api.openweathermap.org/data/2.5/weather"
    parameters={
        'q':city,
        'appid':'c36e95b1d9dac939f9118cfb934fa6c5'
    }
    resp=requests.get(url,params=parameters)
    if resp.status_code==200:
        try:
            data=resp.json()
            lat=data['coord']['lat']
            lon=data['coord']['lon']
            return lat, lon
        except:
            return False
    return False

def get_temprature(lat,lon):
    url="https://api.openweathermap.org/data/2.5/weather"
    parameters={
        "lat":lat,
        'lon':lon,
        'units':'metric',
        'appid':'c36e95b1d9dac939f9118cfb934fa6c5'
    }
    resp=requests.get(url,params=parameters)
    if resp.status_code==200:
        try:
            data=resp.json()
            name=data['name']
            temp=data['main']['temp']
            desc=data['weather'][0]['description']
            icon=data['weather'][0]['icon']
            return{
                'name':name,
                'temp':temp,
                'desc':desc,
                'icon':f'https://openweathermap.org/img/wn/{icon}@4x.png'
            }
        except Exception as e:
            print('error',e)
            return {}
    else:
        print('\nSomething Went Wrong')
        print(f'Status Code: {resp.status_code} {resp.reason}')
        return {}

if __name__=='__main__':
    os.system('cls')
    print('\n\n\n')
    city=input('Enter city name: '.rjust(50))
    coord=get_lat_lon(city)
    if coord:
        lat,lon=coord
        data=get_temprature(lat,lon)
        for key, values in data.items():
            print(f'{key:>30} = {values}')
        print('\n\n\n')
    else:
        print('City not found!')
    
