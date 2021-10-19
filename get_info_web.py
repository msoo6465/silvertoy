from bs4 import BeautifulSoup
import requests


def get_weather(location):
    weather_dict = {}
    URL = f'https://www.google.com/search?client=opera&hs=iaa&ei=FHvcX9HDAtWC-QaY95HYBA&q={location}날씨&oq=서울날씨&gs_lcp=CgZwc3ktYWIQAzIICAAQsQMQgwEyBAgAEEMyAggAMgIIADICCAAyAggAMgIIADICCAAyBggAEAcQHjIGCAAQBxAeOgQIABBHOgQIABANOgcIABCxAxANUJHjBVi55wVg0OgFaAFwAngAgAFwiAHfA5IBAzQuMZgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwjRnZqooNftAhVVQd4KHZh7BEsQ4dUDCAw&uact=5'

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 OPR/67.0.3575.115'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf8")
    data = soup.find("div", {"id": "wob_d"})
    refine = data.findAll("span")

    data_list = []

    for x in refine:
        data_list.append(x.get_text())

    weather_dict['온도'] = data_list[0]
    weather_dict['강수확률'] = data_list[3]
    weather_dict['습도'] = data_list[7]
    weather_dict['풍속'] = data_list[9]
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
