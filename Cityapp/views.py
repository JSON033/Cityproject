from django.shortcuts import render, redirect
import requests
from .models import City 
from .forms import CityForm

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=5ab3eebe2d746cadead519c9da6d1155'
    turl = 'https://api.ipgeolocation.io/timezone?apiKey=153ae96c62b442fbb65c78b889047a61&&location={}'
   
    city = City.objects.all()
    error = ''
    notification =''
    message_class=''    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            newcity = form.cleaned_data['name']
            if City.objects.filter(name = newcity).count() ==0:
                r = requests.get(url.format(newcity)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    error ='City Not Found!'
            else:
                error = 'City Already Added!'
    
        if error:
            notification = error
            message_class = 'is-danger'
        else:
            notification = 'City Added Successfully!'
            message_class = 'is-success'
    form = CityForm()
    
    cities = []
    for C in city:
        
        
         

        tr = requests.get(turl.format(C)).json()
        
        r = requests.get(url.format(C)).json()
        
        city_data ={
            'city' : str(C).title(),
            'temperature' : r['main']['temp'] ,
            'description' :r['weather'][0]['description'].upper() ,
            'icon' : r['weather'][0]['icon']  ,
            'country' :r['sys']['country'],
            'countryicon' :r['sys']['country'].lower() ,
            'time' : tr['time_12'],
        }

        cities.append(city_data)



    context = {'cities' : cities, 
                'form' : form,
                 'notification' : notification,
                 'message_class' : message_class   
    }
    return render(request, 'Cityapp/Cityapp.html', context)

def DeleteCity(request, cityname):
    City.objects.get(name = cityname).delete()
    return redirect('index')