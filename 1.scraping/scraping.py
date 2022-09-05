import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
from tanks import Tank

def remove_non_ascii(text):
		return ''.join([i if ord(i) < 128 else '' for i in text])

def get_basic_info(soup, class_):
	basic_info_soup = soup.find('div', {'class':'specs_card_main'})
	div = basic_info_soup.find('div', {'class':f'general_info_{class_}'})
	return div

def get_tank_data(name):
	page = req.get(f'https://wiki.warthunder.com/{name}')
	soup = bs(page.text, features='html.parser')

	tank = Tank()

	tank.name_ = remove_non_ascii(get_basic_info(soup, 'name').text.strip())
	tank.nation = get_basic_info(soup, 'nation').text.strip()
	tank.rank = get_basic_info(soup, 'rank').text.replace('Rank','').strip()
	tank.battle_rating = get_basic_info(soup, 'br').find('table').findAll('td')[4].text.strip()

	class_divs = get_basic_info(soup, 'class').findAll('div')
	for i, div in enumerate(class_divs):
		if div.text.strip() == 'PREMIUM':
			class_divs.pop(i)

			price = get_basic_info(soup, 'price_buy').text.replace('Purchase:','')
			if price == 'Bundle or Gift':
				tank.category = 'Premium - Bundle or Gift'
			else:
				tank.category = 'Premium - Golden Eagles'
		else:
			tank.category = 'Researchable'
		if div.text.strip() == 'SQUADRON':
			class_divs.pop(i)
			tank.category = 'Squadron'

	tank.class_ = [div.text for div in class_divs][0]

	return tank.to_dataframe()

def get_nation_tank_names(nation):
	page = req.get(f'https://wiki.warthunder.com/Category:{nation}_ground_vehicles')
	soup = bs(page.text, features='html.parser')

	return [i.text.replace(' ','_') for i in soup.find('div', {'class':'mw-category'}).findAll('li')]

def get_nations_tank_data(nation):
	tanks_df = pd.DataFrame()

	for tank in get_nation_tank_names(nation):
		print(tank)
		tanks_df = pd.concat([tanks_df,get_tank_data(tank)])

	path = 'C:\\Users\\zacha\\Desktop\\repo\\data\\'
	tanks_df.to_csv(path+f'{nation}_tanks.csv')

get_nations_tank_data('Israel')