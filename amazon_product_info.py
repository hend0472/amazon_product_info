import requests
import bs4
import random
import ast


header_1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
						  'Chrome/54.0.2840.71 Safari/537.36'}
header_2 = {'User-Agent': 'Mozilla/5.0'}
header_3 = {'User-Agent': 'my-app/0.0.1'}
header_4 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
header_5 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
header_6 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}


header_list = []
header_list.append(header_1)
# header_list.append(header_2)
# header_list.append(header_3)
header_list.append(header_4)
header_list.append(header_5)
header_list.append(header_6)


test_url = 'https://www.amazon.com/gp/product/B00M5CUU7Y/ref=s9u_simh_gw_i1?ie=UTF8&fpl=fresh&pd_rd_i=B00M5CUU7Y&pd_rd_r=6ZKN4V2FZ8CER3PVJ760&pd_rd_w=UvlA6&pd_rd_wg=Df1hZ&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=&pf_rd_r=7XW3Y96AV7V4V04S8NAR&pf_rd_t=36701&pf_rd_p=d9f78c36-24d5-402e-866f-a50358a0504c&pf_rd_i=desktop'
test_url2 = 'https://www.amazon.com/gp/product/B0051NPRTK/ref=s9u_wsim_gw_i1?ie=UTF8&fpl=fresh&pd_rd_i=B0051NPRTK&pd_rd_r=MARC4AP07Q08WJSMK2Z0&pd_rd_w=nxnZI&pd_rd_wg=UxkXh&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=&pf_rd_r=DH5YRAG3QNHESQF7CA4M&pf_rd_t=36701&pf_rd_p=0411ffec-c026-40ae-aac5-2cd3d48aeeac&pf_rd_i=desktop'



def get_amazon_product_info(url, printyesno):
	printyesno = False
	cheaper = False
	weight_value = False
	dimensions_value = False
	upc_value = False
	upc = 0
	weight = '0'
	dimensions = '0'
	main_image_url = 'none'
	ranked_item = False
	asin_list = url.split('/')
	for i in asin_list:
		if len(i) == 10:
			asin = i
	header_choice = header_list[random.randint(0,3)]
	res = requests.get(url, headers=header_choice)
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	product_name = str(soup.find('span', attrs={'id':'productTitle'}).text).lstrip().rstrip()
	try:
		review_count = soup.find('span', attrs={'id':'acrCustomerReviewText'}).text
		review_count = str(review_count).split(' ')[0]
		review_count = review_count.replace(',', '')
	except:
		review_count = 0
	for span in soup.findAll('span', attrs={'class':'a-icon-alt'}):
		if 'stars' in span.text:
			review_stars = span.text
			review_stars = str(review_stars).split(' ')[0]
			break		# so it only catches first stars
	if review_count == 0:
		review_stars = 0
	try:
		amazon_price = float(str(soup.find('span', attrs={'id': 'priceblock_ourprice'}).text).replace('$', ''))
	except:
		try:
			amazon_price = float(str(soup.find('span', attrs={'id': 'priceblock_saleprice'}).text).replace('$', ''))
		except:
			pass
			amazon_price = 'Not Sold by Amazon'

	try:
		main_image = soup.find('img', attrs={'id':'landingImage'}).attrs.get('data-a-dynamic-image')
		image_dict = ast.literal_eval(main_image)
		main_images = {}
		for key, value in image_dict.items():
			image_size = (str(key).split('_')[1])[2:]
			main_images[image_size] = key
		max_key = max(k for k, v in main_images.items() if v != 'd')
		main_image_url = main_images[max_key]
		# print(main_images[max_key])
	except:
		pass

	soup2 = soup.find('div', attrs={'id':'prodDetails'})
	ranks2 = {}
	for tr in soup2.findAll('tr'):
# FIRST KIND OF AMAZON PAGE
		try:
			label = str(tr.find('td', attrs={'class':'label'}).text).lstrip().rstrip()
			value = str(tr.find('td', attrs={'class':'value'}).text).lstrip().rstrip()
			value2 = (tr.find('td', attrs={'class':'value'}))
			if 'weight' in str(label).lower():
				weight = str(value).replace('(View shipping rates and policies)', '')
				weight_value = True
			elif 'dimensions' in str(label).lower():
				dimensions = value
				dimensions_value = True
			elif 'best sellers rank' in str(label).lower():
				ranks = str(value).replace('\n', '')
				ranks = ranks.split('#')
				del ranks[0]
				# ranks2 = {}
				for rank in ranks:
					if '(' in rank:
						rank = rank.split('(')[0]
						rank = rank.split(' in ')
						ranks2[rank[1]] = int(str(rank[0]).replace(',', ''))
					else:
						index_loc = (rank.index('i'))
						ranknum = str(rank[:index_loc]).replace(',', '')
						category = rank[(index_loc + 3):]
						ranks2[category] = int(ranknum)
			elif 'asin' in str(label).lower():
				asin = str(value)
			elif 'upc' in str(label).lower():
				upc = str(value)
				upc_value = True
		except:
			pass
# SECOND KIND OF AMAZON PAGE
		try:
			label = str(tr.find('th', attrs={'class':'a-color-secondary a-size-base '
													 'prodDetSectionEntry'}).text).lstrip().rstrip()
			value = str(tr.find('td', attrs={'class':'a-size-base'}).text).lstrip().rstrip()
			if 'weight' in str(label).lower():
				weight = str(value).replace('(View shipping rates and policies)', '')
				weight_value = True
			elif 'dimensions' in str(label).lower():
				dimensions = value
				dimensions_value = True
			elif 'best sellers rank' in str(label).lower():
				ranks = str(value).replace('\n', '')
				ranks = ranks.split('#')
				del ranks[0]
				# ranks2 = {}
				for rank in ranks:
					if '(' in rank:
						rank = rank.split('(')[0]
						rank = rank.split(' in ')
						ranks2[rank[1]] = int(str(rank[0]).replace(',', ''))
					else:
						index_loc = (rank.index('i'))
						ranknum = str(rank[:index_loc]).replace(',', '')
						category = rank[(index_loc + 3):]
						ranks2[category] = int(ranknum)
			elif 'asin' in str(label).lower():
				asin = str(value)
			elif 'upc' in str(label).lower():
				upc = str(value)
				upc_value = True
		except:
			pass
# THIRD KIND OF AMAZON PAGE
		try:
			label = str(tr.find('th', attrs={'class':'a-color-secondary a-size-base '
													 'prodDetSectionEntry'}).text).lstrip().rstrip()
			value = str(tr.find('td').text).lstrip().rstrip()
			if 'weight' in str(label).lower():
				weight = str(value).replace('(View shipping rates and policies)', '')
				weight_value = True
			elif 'dimensions' in str(label).lower():
				dimensions = value
				dimensions_value = True
			elif 'best sellers rank' in str(label).lower():
				ranks = str(value).replace('\n', '')
				ranks = ranks.split('#')
				del ranks[0]
				# ranks2 = {}
				for rank in ranks:
					if '(' in rank:
						rank = rank.split('(')[0]
						rank = rank.split(' in ')
						ranks2[rank[1]] = int(str(rank[0]).replace(',', ''))
					else:
						index_loc = (rank.index('i'))
						ranknum = str(rank[:index_loc]).replace(',', '')
						category = rank[(index_loc + 3):]
						ranks2[category] = int(ranknum)
			elif 'asin' in str(label).lower():
				asin = str(value)
			elif 'upc' in str(label).lower():
				upc = str(value)
				upc_value = True
		except:
			pass
	if printyesno == True:
		print('\n')
		print('~' * 120)
		print('      PRODUCT NAME: ' + product_name)
		print('      PRODUCT ASIN: ' + asin)
		if upc_value == True:
			print('          UPC CODE: ' + upc)
		print('        AMAZON URL: ' + url)
		print('      AMAZON PRICE: ' + str(amazon_price))
		print('           REVIEWS: ' + str(review_count))
		print('             STARS: ' + str(review_stars) + '/5.0')
		if weight_value == True:
			print('    PRODUCT WEIGHT: ' + str(weight))
		if dimensions_value == True:
			print('PRODUCT DIMENSIONS: ' + str(dimensions))
		print('    MAIN IMAGE URL: ' + str(main_image_url))
		if len(ranks2) != 0:
			print('     -----BEST SELLER RANKINGS-----')
			for category, rank in ranks2.items():
				front_space = 17 - (len(str(rank)))
				print((' ' * front_space) + str(rank) + ' : ' + category.upper())
		print('~' * 120)
	return product_name, asin, upc, amazon_price, review_count, review_stars, weight, dimensions, main_image_url, ranks2

# print(get_amazon_product_info('https://www.amazon.com/J5-Tactical-V1-Pro-Flashlight-Original/dp/B00V7T1YRQ/ref=sr_1_4?ie=UTF8&qid=1513660454&sr=8-4&keywords=flashlight', True)

# print(get_amazon_product_info(test_url, True))
# amazon_name, amazon_asin, amazon_upc, amazon_price, amazon_reviews, amazon_stars, amazon_weight, amazon_dimensions, \
# amazon_image, amazon_ranks = get_amazon_product_info(test_url, False)
#
# print(amazon_name)
# print(amazon_ranks)
# for key, value in amazon_ranks.items():
# 	print(value, key)


# get_amazon_product_info(test_url)
# get_amazon_product_info('https://www.amazon.com/dp/B01FJSG5Z6?th=1')
# get_amazon_product_info(test_url2)