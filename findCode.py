from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import time

def matched_url(current_url, herf_url):
	black_words = ['resource', 'sitemap', 'tentang-kami', 'upload','pasang', 'category', 'author', 'page', 'disclaimer', 'privacy', 'policy', 'about', 'contac', 'contact', 'tag', 'cookies', 'search', 'topic', 'topik', 'politica', 'legal', 'term', 'menu', 'page']
	if current_url == herf_url:
		return False
	domain1 = urlparse(current_url).netloc
	domain2 = urlparse(herf_url).netloc

	if domain1 != domain2 or len(herf_url) - 20 < len(domain1):
		return False
	for word in black_words:
		if word in herf_url:
		    return False
	return True

def find_code(driver2, link_to_open, key):
    try:
        driver2.get(link_to_open)
        time.sleep(3)
        text_value = ['', '']
        try:
            text_value[0] = driver2.find_element(By.ID, 'kode').text
            text_value[1] = driver2.current_driver
        except:
            text_value[0] = ''
            text_value[1] = ''
            
        if text_value[0] == '':
            a_tags = driver2.find_elements(By.TAG_NAME, 'a')
            herfs = []
            herfs.append(link_to_open)
			
            if a_tags is not None:
                for a in a_tags:
                    if a is not None:
                        try:
                            href = a.get_attribute('href').split('#')[0]
                        except:
                            href = ''
                        if href != '' :
                            if not matched_url(link_to_open, href):
                                continue
                            if href not in herfs:
                                herfs.append(href)
            for i in herfs[::-1]:
                try:
                    driver2.get(i)
                except:
                    continue
                p_tags = driver2.find_elements(By.TAG_NAME, 'p')
                if p_tags is not None:
                    for p in p_tags:
                        if p is not None:
                            if ('code:' in p.text.lower() or 'codes:' in p.text.lower() or 'hint cd:' in p.text.lower()) and len(p.text) < 35 and len(p.text) > 6:
                                print(p.text)
                                text_value[0] = p.text.split(':')[1].strip()
                                text_value[1] = driver2.current_url
                                return text_value
        else:
            print(text_value[0])
        return text_value
    except Exception as e:
        print(e)
    return ['', '']
