from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import random
import requests

def get_domain(url):
	from urllib.parse import urlparse
	parsed_url = urlparse(url)
	domain = parsed_url.netloc
	if domain.startswith("www."):
		domain = domain[4:]  # Remove 'www.' if present
	return domain

def scroll(driver):
	initial_height = driver.execute_script("return document.body.scrollHeight")
	total_scrolls = 10
	scroll_increment = initial_height // total_scrolls

	for _ in range(total_scrolls):
	    driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
	    time.sleep(0.5)  # Adjust sleep time as needed

def find_main_ads(driver, ads_container_a, recent_ads):
	if ads_container_a is None:
		return ''
	main_ads = ''
	st = time.perf_counter()
	for l in ads_container_a:
		et = time.perf_counter()
		if et - st > 30:
			break
		if l is not None and l.get_attribute('href') is not None:
			et = time.perf_counter()
			if et - st > 30:
				break
			try:
				response = requests.get(l.get_attribute('href'), allow_redirects=True, timeout=2)
			except:
				continue
			if 'gclid' in response.url and 'ad' not in response.url.lower() and get_domain(response.url) not in recent_ads:
				main_ads = response.url
				main_ads = main_ads.replace('&gclsrc=aw.ds', '').replace('#_=_', '')
				break
	return main_ads

def get_ads_infor(driver, url, has_para, lkey, finding, ads_link, recent_ads):
	ads_infor = {
		"main": "",
		"inside1": "",
		"inside2": "",
		"about": "",
		"contact": "",
		"para1": "",
		"para2": ""
	}

	try:
		if finding:
			driver.delete_all_cookies()
			time.sleep(1)
			try:
				driver.get(url)
			except:
				return ads_infor
				
			time.sleep(3)
			scroll(driver)
		
			ads_link = ''

			for i in range(3):
				try:
					driver.switch_to.frame(i)
				except:
					continue

				if driver.find_elements(By.ID, 'mys-wrapper'):
					ads_container = driver.find_element(By.ID, 'mys-wrapper')
					anchor_elements = ads_container.find_elements(By.TAG_NAME, 'a')

					ads_link = find_main_ads(driver, anchor_elements, recent_ads)

				if ads_link == '':
					time.sleep(3)
					anchor_elements = driver.find_elements(By.TAG_NAME, 'a')

					ads_link = find_main_ads(driver, anchor_elements, recent_ads)

				if ads_link != '':
					break

		if ads_link != '':
			ads_infor["main"] = ads_link

			domain = get_domain(ads_link)
			if driver.current_url != ads_link:
				try:
					driver.get(ads_link)
					time.sleep(2)
				except:
					pass

			ads_infor["about"] = 'http://www.' + domain + "/about" + "|0"
			ads_infor["contact"] = 'http://www.' + domain + "/contact" + "|0"

			anchor_ads = driver.find_elements(By.TAG_NAME, 'a')
			inside_links = []
			
			for element in anchor_ads:
				if element is not None:
					href = element.get_attribute('href')
					if href is not None and 'mailto' not in href and 'ad' not in href.lower():
						href = href.split('?')[0].split('#')[0].split('=')[0]
						if domain in href:
							if 'www' in href:
								if len(href) > len(domain) + 15:
									inside_links.append(href)
							else:
								if len(href) > len(domain) + 12:
									inside_links.append(href)

			if len(inside_links) < 5:
				return ads_infor

			ads_infor["inside1"] = random.choice(inside_links)
			inside_links.remove(ads_infor["inside1"])
			ads_infor["inside2"] = random.choice(inside_links)

			for i in range(len(inside_links)):
				if 'about' in inside_links[i]:
					ads_infor["about"] = inside_links[i] + "|1"
				elif 'contact' in inside_links[i]:
					ads_infor["contact"] = inside_links[i] + "|1"

			if has_para:
				count = 0
				cp_inside_links = inside_links
				while len(cp_inside_links) > 0 and count < 5:
					count += 1
					
					random_link = random.choice(cp_inside_links)
					cp_inside_links.remove(random_link)

					if (ads_infor["para1"] != "" and ads_infor["para2"] != ""):
						break
					try:
						driver.get(random_link)
					except:
						pass
					time.sleep(2)
					para_tags = driver.find_elements(By.TAG_NAME, 'p')

					for j in range(len(para_tags)):
						para_tmp = para_tags[j].text
						if len(para_tmp.split(' ')) < 5:
							continue
						if ads_infor["para1"] != "" and ads_infor["para2"] != "":
							break
						if len(para_tmp) > 30:
							if ads_infor["para1"] == "":
								ads_infor["para1"] = para_tmp
							elif ads_infor["para2"] == "" and para_tmp != ads_infor["para1"]:
								ads_infor["para2"] = para_tmp
			else:
				ads_infor["para1"] = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
				ads_infor["para2"] = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

	except TimeoutException as e:
		pass

	except Exception as e:
		if lkey == 'admin':
			print("Exception at ads find", e)
			import traceback
			traceback.print_exc()
	return ads_infor