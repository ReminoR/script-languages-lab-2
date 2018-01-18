#2. Используя Python и модули requests и re написать скрипт, получающий все
#адреса подразделов сайта(относительные url) и для каждой из них выполнить
#поиск адресов электронной почты(см. задание 1)

import requests
import re
import time

#http://www.tsu.ru/help/contacts.php
#http://space-monkey.ru
#http://mosigra.ru
#https://goncharnoedelo.ru
#http://my.mail.ru
url = 'http://my.mail.ru'

#функция получения кода страницы и извлечение относительных ссылок сайта. Сохраняем в список все адреса, проверив их на локальность.
def get_urls(url):
	site = requests.get(url).text
	pattern = re.compile(r'href="(^http://|^https://|^mailto:|^tel:|^#|/\w+/*\w*/*\w*/*\w*/*\w*/*\.*\w*)')
	urls = list('/') + list(set(pattern.findall(site)))
	print ('С сайта ' + url + ' собрано ' + str(len(urls)) + ' urls')
	return urls

# функция получения кода страницы сайта и извлечение email адресов.
#url - url сайта
#list_pages - список со страницами сайта
#limit_pages - установленный пользователей лимит на количество страниц. 0 - без лимита.
def get_emails(url, list_pages, limit_pages):
	result = []
	count = 0
	pattern = re.compile(r'\w+\.*-*_*\w*\.*-*_*\w*@\w+\.*-*_*\w*\.\w{2,10}')
	exceptions = [] #добавляем исключения
	pattern_mail_ru = re.compile(r'@Mail\.')
	if not limit_pages == 0:
		print('Установленный лимит: ' + str(limit_pages))

	for page in list_pages:
		count += 1
		if not limit_pages == 0:
			if count > limit_pages:
				break

		site = requests.get(url+page).text
		emails = pattern.findall(site)
		for email in emails:
			if not pattern_mail_ru.findall(email) and email not in exceptions:
				result.append(email)
		print('(' + str(count) + '/' + str(len(list_pages)) +') Поиск на странице ' + url + page)
		time.sleep(3)

	result = set(result)	
	for email in result:
		print(email)

	return result

def write_csv(data):
	with open('emails.csv', 'w') as file:
		for i in data:
			file.write(i)
			file.write('\n')
		print('\007')
		file.close()

def main():
	list_pages = get_urls(url)
	emails = get_emails(url, list_pages, 0)
	write_csv(emails)


if __name__ == '__main__':
	main()