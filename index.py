#2. Используя Python и модули requests и re написать скрипт, получающий все
#адреса подразделов сайта(относительные url) и для каждой из них выполнить
#поиск адресов электронной почты(см. задание 1)

import requests
import re

#http://www.tsu.ru/help/contacts.php
#http://space-monkey.ru
#http://mosigra.ru
#https://goncharnoedelo.ru
url = 'http://mosigra.ru'

#функция получения кода страницы и извлечение относительных ссылок сайта. Сохраняем в список все адреса, проверив их на локальность.
def get_urls(url):
	site = requests.get(url).text
	pattern = re.compile(r'href="(^http://|^https://|^mailto:|^tel:|^#|/\w+/*\w*/*\w*/*\w*/*\w*/*\.*\w*)')
	urls = list(set(pattern.findall(site)))
	return urls

# функция получения кода страницы сайта и извлечение email адресов.
def get_emails(url, list_pages, limit_pages):
	result = []
	count = 0
	pattern = re.compile(r'\w+\.*-*_*\w*\.*-*_*\w*@\w+\.*-*_*\w*\.\w{2,10}')

	if not list_pages:
		site = requests.get(url).text
		result = pattern.findall(site)
	else:
		for i in list_pages:
			site = requests.get(url+i).text
			emails = pattern.findall(site)
			result += emails
			count += 1
			if count == limit_pages:
				break 
			print(i)

	result = set(result)	
	print(result)
	return result

list_pages = get_urls(url)
emails = get_emails(url, list_pages, 0)


with open('emails.csv', 'w') as file:
	for i in emails:
		file.write(i)
		file.write('\n')
	file.close()
