from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(req):
    weatherData = dict()
    # return HttpResponse("Hello World")
    if 'city' in req.GET:
        city = req.GET.get('city')
        html_content = get_html_content(city)

        # print(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        weatherData['region'] = soup.find('div', attrs={'id': 'wob_loc'}).text
        weatherData['time'] = soup.find('div', attrs={'id': 'wob_dts'}).text
        weatherData['status'] = soup.find('span', attrs={'id': 'wob_dc'}).text
        weatherData['img'] = soup.find('img', attrs={'id': 'wob_tci'})['src']
        weatherData['temperature'] = soup.find('span', attrs={'id': 'wob_tm'}).text
        weatherData['humidity'] = soup.find('span', attrs={'id': 'wob_hm'}).text
        weatherData['windSpeed'] = soup.find('span', attrs={'id': 'wob_ws'}).text
    return render(req, 'core/home.html', {'weather': weatherData})


def get_html_content(city):
    import requests
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city = city.replace(' ', '+')
    return session.get(f'https://www.google.com/search?q=weather+in+{city}').text
