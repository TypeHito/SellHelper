import requests

def correct_spelling(text):
    url = "https://speller.yandex.net/services/spellservice.json/checkText"
    params = {
        "text": text,
        "lang": ""
    }
    response = requests.get(url, params=params).json()
    if response:
        return response[0]['s'][0]  # Возвращает исправленное слово
    return text

user_input = "olma bom"
corrected = correct_spelling(user_input)  # Вернет "яблоко"
print(corrected)