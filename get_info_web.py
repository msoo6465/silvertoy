from bs4 import BeautifulSoup
import requests


def get_weather():
    weather_dict = {}
    URL = f'https://weather.naver.com/today/06110517'
    headers = {
        "User-Agent": 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf8")

    temp = soup.find("strong", {"class": "current"}).text
    misae = soup.find('em',{'class' : 'level_text'}).text
    state = soup.find('span',{'class':'weather'}).text
    humic = soup.find('dd', {'class':'desc'}).text

    weather_dict['온도'] = temp[-3:-1]
    weather_dict['상태'] = state
    weather_dict['습도'] = humic
    weather_dict['미세먼지'] = misae

    return weather_dict

def get_news():
    URL = 'https://news.naver.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding='utf8')
    data = soup.find('ul',{'class':'hdline_article_list'})
    refind = data.findAll('li')

    news_title = {idx:i.find('a').text.strip() for idx, i in enumerate(refind,1)}
    return news_title

get_weather()