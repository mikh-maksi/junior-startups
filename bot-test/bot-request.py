import requests, json
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
r = requests.get('https://innovations.kh.ua/quiz/list/?author_id=0&n=1',headers=HEADERS)
element = r.json()
print(element['question_arr'][0])


# r = requests.get('https://innovations.kh.ua/quiz/list/?author_id=0&n=1',headers=HEADERS)
# print(str(r.text))
# k = json.loads(str(r.text))
# print(k[0])

# import requests
# print("Hello")
# print(r.status_code)

print("Hello")