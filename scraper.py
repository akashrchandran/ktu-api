import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse


NOTIF_URL = 'https://ktu.edu.in/eu/core/announcements.htm'


def scrape_notifications(limit):
	req = requests.get(NOTIF_URL)
	if req.status_code != 200:
		return 'Ktu site is not accessible!'
	soup = BeautifulSoup(req.content, 'html.parser')
	notif_list = []
	for tags in soup.find_all('tr', limit=limit):
		bold = tags.find_all('b')
		date, title = bold[0].get_text(), bold[1].get_text()
		description = bold[1].next_sibling.strip()
		circular = extract_attachments(tags.find_all('a'))
		if not isinstance(circular, list):
			return circular
		notif_list.append({"date": date, "title": title, "description": description, "attachment": circular})
	return notif_list


def extract_attachments(soup):
	attachments = []
	for anchors in soup:
		try:
			title = anchors.get_text()
			link = "https://ktu.edu.in/{}".format(re.sub(r'\s+', '', anchors['href']))
			attachments.append({'title': title, 'link': link})
		except Exception as e:
			return e
	return attachments
