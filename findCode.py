from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import time

def matched_url(current_url, herf_url):
    black_words = ['resource', 'sitemap', 'tentang-kami', 'upload','pasang', 'category', 'author', 'page', 'disclaimer', 'privacy', 'policy', 'about', 'contac', 'contact', 'tag', 'cookies', 'search', 'topic', 'topik', 'politica', 'legal', 'term']
    if current_url == herf_url:
        return False
    # Get the domain name of the first URL
    domain1 = urlparse(current_url).netloc

    # Get the domain name of the second URL
    domain2 = urlparse(herf_url).netloc

    # Check if the domain names match
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
        text_value = ''
        try:
            text_value = driver2.find_element(By.ID, 'kode').text
        except:
            pass
        if text_value == '':
            a_tags = driver.find_elements(By.TAG_NAME, 'a')
            herfs = []

            if a_tags is not None:
                for a in a_tags:
                    if a is not None:
                        try:
                            href = a.get_attribute('href')
                        except:
                            href = ''
                        if href != '' :
                            if not matched_url(link_to_open, href):
                                continue
                            if href not in herfs:
                                herfs.append(href)

            for i in herfs:
                driver.get(i)
                p_tags = driver.find_elements(By.TAG_NAME, 'p')
                if p_tags is not None:
                    for p in p_tags:
                        if p is not None:
                            if 'code:' in p.text.lower():
                                print(p.text)
                                return p.text
        else:
            print(text_value)
        return text_value
    except Exception as e:
        if (key == 'admin'):
            print(e)
    return ''
