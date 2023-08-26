from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def find_code(driver2, sorted_url, key):
    try:
        driver2.get(sorted_url[0])
        time.sleep(3)
        text_value = ['', '']
		
        for i in sorted_url[::-1]:
            try:
                driver2.get(i)
            except:
                continue
            if driver2.find_elements(By.ID, 'kode'):
                text_value[0] = driver2.find_element(By.ID, 'kode').text
                text_value[1] = driver2.current_url
                return text_value
            else:
                p_tags = []
                p_tags += driver2.find_elements(By.TAG_NAME, 'p')
                p_tags += driver2.find_elements(By.TAG_NAME, 'li')
                p_tags += driver2.find_elements(By.TAG_NAME, 'h1')
                p_tags += driver2.find_elements(By.TAG_NAME, 'h2')
                p_tags += driver2.find_elements(By.TAG_NAME, 'h3')
                p_tags += driver2.find_elements(By.TAG_NAME, 'strong')
                if p_tags is not None:
                    for p in p_tags:
                        if p is not None:
                            if ('code :' in p.text.lower() or 'code:' in p.text.lower() or 'codes:' in p.text.lower() or 'hint cd:' in p.text.lower()) and len(p.text) < 35 and len(p.text) > 6:
                                print(p.text)
                                text_value[0] = p.text.split(':')[1].strip()
                                text_value[1] = driver2.current_url
                                return text_value
                                
        return text_value
    except Exception as e:
        if key == 'admin':
            print("exception at find_code ", e)
            import traceback
            traceback.print_exc()
    return ['', '']
