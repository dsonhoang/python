import time
import asyncio
import pyppeteer
from pyppeteer.errors import ElementHandleError
import requests
from bs4 import BeautifulSoup
import random
import html

async def find_code(page, sorted_url, key):
    try:
        if len(sorted_url) == 0:
            return ['', '']
        text_value = ['', '']
        count = 0

        num_pages = 0
        for i in sorted_url:
            count += 1
            try:
                if 'unidosenoracion.org' in i:
                    i = 'https://unidosenoracion.org/united-in-prayer/'
                elif 'sarkariaadmi' in i:
                    i = 'https://sarkariaadmi.com/paris-paralympics-2024-indias-schedule-and/'
                await page.goto(i, {'timeout': 60000})
                await asyncio.sleep(1)
                await page.evaluate('() => window.scrollTo(0, document.documentElement.scrollHeight)')
            except:
                continue

            next_href = await page.evaluate('''() => {
                const links = document.querySelectorAll('a[target="_blank"]');
            
                for (let i = 0; i < links.length; i++) {
                    const link = links[i];
                    
                    // Check if the link has 'rel' attribute equal to 'noopener'
                    if (link.getAttribute('rel') === 'noopener') {
                        return link.href;
                    }
                    
                    // Check if the link contains the text 'NEXT'
                    if (link.textContent.includes('NEXT') || link.textContent.includes('>')) {
                        return link.href;
                    }
                }
                
                return null; // Return null if no matching link is found
            }''')

            if next_href and not 'clashranger' in i:
                for _ in range(6):
                    await page.goto(next_href, {'timeout': 60000})
                    await asyncio.sleep(2)

                    next_href = await page.evaluate('''() => {
                        const links = document.querySelectorAll('a[target="_blank"]');
                    
                        for (let i = 0; i < links.length; i++) {
                            const link = links[i];
                            
                            // Check if the link has 'rel' attribute equal to 'noopener'
                            if (link.getAttribute('rel') === 'noopener') {
                                return link.href;
                            }
                            
                            // Check if the link contains the text 'NEXT'
                            if (link.textContent.includes('NEXT') || link.textContent.includes('>')) {
                                return link.href;
                            }
                        }
                        
                        return null; // Return null if no matching link is found
                    }''')

                    if ((await page.querySelectorAll('.srd') or await page.querySelectorAll('[clashaderutis=srd]')) and not next_href) or not next_href:
                        break

                if await page.querySelectorAll('.srd') or await page.querySelectorAll('[clashaderutis=srd]'):
                    page_url = page.url
                    
                    response = requests.get(page_url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        element = soup.find(id='download')
                        
                        if element:
                            element_text = element.get_text().strip()
                            print(element_text)
                            if len(element_text) > 0:
                                return [element_text, page_url]
                            else:
                                center_elements = await page.querySelectorAll('center')
                                if center_elements:
                                    for center_element in center_elements:
                                        center_text = await page.evaluate('(element) => element.textContent', center_element)
                                        if '\\2O24' in center_text:
                                            center_words = center_text.split(' ')
                                            for center_word in center_words:
                                                if '\\2O24' in center_word:
                                                    return [center_word.strip(), page.url]

            if await page.querySelectorAll('.border-white'):
                try:
                    code_text = ''
                    random_urls = random.sample(sorted_url, 3)
                    for url in random_urls:
                        response = requests.get(url, timeout=10)
                    
                        soup = BeautifulSoup(response.text, 'html.parser')
                        element = soup.find(class_='border-white')
                        
                        if element:
                            text = element.get_text(strip=True)
                        code_text = code_text + text + '\n'

                    code_text = code_text.strip()
                    if len(code_text.split('\n')) == 3:
                        return [code_text, page.url]
                    else:
                        return ['', '']
                except:
                    return ['', '']

            if await page.querySelectorAll('.g-btn'):
                for _ in range(10):
                    next_btn = await page.querySelector('.g-btn')
                    next_btn_title = await page.evaluate('(element) => element.getAttribute("title")', next_btn)
                    if next_btn_title.lower() == 'next':
                        next_href = await page.evaluate('(element) => element.dataset.externalUrl', next_btn)
                        await page.goto(next_href)
                        await asyncio.sleep(2)
                    elif next_btn_title.lower() == 'get code':
                        code_text = await page.evaluate('(element) => element.dataset.msg', next_btn)
                        return [code_text, page.url]
                    else:
                        break

            if 'semuaja' in i and await page.querySelectorAll('.google-anno-skip'):
                ads_element = await page.querySelector('.google-anno-skip')
                ads_text = await page.evaluate('(element) => element.textContent', ads_element)
                return [ads_text, page.url]

            if await page.querySelectorAll('.detail_lagi'):
                await page.goto('view-source:'+i, {'timeout': 60000})
                await asyncio.sleep(2)

                page_content = await page.content()
                page_content = html.unescape(page_content)

                if 'const code =' in page_content:
                    index = page_content.find('const code =')
                    sub_string = page_content[index:]
        
                    first_index = sub_string.find("'")
                    second_index = sub_string.find("'", first_index + 5)
                    code_text = sub_string[first_index + 1:second_index]
                    text_value[0] = code_text
                    text_value[1] = i
                    return text_value
                else:
                    return ['','']
            if await page.querySelectorAll('.show_code'):
                page_content = await page.content()

                if 'key_code = ' in page_content:
                    first_index = page_content.index('key_code = ') + len('key_code = ')
                    second_index = page_content.index(';', first_index)
                    code_text = page_content[first_index:second_index].replace('"', '').strip()
                    if len(code_text) < 15:
                        text_value[0] = code_text
                        text_value[1] = page.url
                        return text_value
                return ['', '']

            if await page.querySelector('#countdownContainer'):
                await page.goto('view-source:'+i, {'timeout': 60000})
                await asyncio.sleep(2)
                page_content = await page.content()

                if 'special code:' in page_content:
                    index = page_content.find('special code')
                    sub_string = page_content[index:]
        
                    first_index = sub_string.find(":")
                    second_index = sub_string.find(";/p", first_index + 5)
                elif 'codeElement.textContent' in page_content:
                    index = page_content.find('codeElement.textContent')
                    sub_string = page_content[index:]
    
                    first_index = sub_string.find("'")
                    second_index = sub_string.find("'", first_index + 5)
                else:
                    return ['','']
    
                code_text = sub_string[first_index + 1:second_index]
                if ':' in code_text:
                    code_text = code_text.split(':')[1].strip().replace('&lt', '')
                else:
                    code_text = code_text.strip().replace('&lt', '')
                text_value[0] = code_text
                text_value[1] = i
                return text_value

            if await page.querySelectorAll('.arpw-random-post'):
                digits_code = ''
                for c in range(5):
                    arpw_random_post = await page.querySelector('.arpw-random-post')
                    links = await arpw_random_post.querySelectorAllEval('a', 'nodes => nodes.map(a => a.href)')
                    first_link = links[0] if links else None
                    if first_link:
                        if c == 4:
                            text_value[1] = first_link
                        await page.goto(first_link, {'timeout': 60000})
                        await asyncio.sleep(2)
                        if await page.querySelectorAll('.pbc-replacetext-raw'):
                            code_text_element = await page.querySelector('.pbc-replacetext-raw')
                            code_text_content = await page.evaluate('(element) => element.textContent', code_text_element)
                            if code_text_content and 'Digit of CODE is:' in code_text_content:
                                code_text_content = code_text_content.split('\n')[0]
                                digits_code += code_text_content.split(':')[1].strip()
                            else:
                                return ['','']
                        else:
                            return ['','']
                    else:
                        return ['','']
                if len(digits_code.strip()) == 5:
                    text_value[0] = digits_code.strip()
                    return text_value
                else:
                    return ['','']

            if await page.querySelectorAll('.pcode_countdown-wrapper'):
                countdown_e = await page.querySelector('.pcode_countdown-wrapper')
                display_attribute = await page.evaluate('(element) => window.getComputedStyle(element).getPropertyValue("display")', countdown_e)
                if display_attribute == 'flex':
                    await asyncio.sleep(25)
                    if await page.querySelectorAll('.countdown-footer'):
                        for _ in range(10):
                            if await page.querySelectorAll('.pcode_countdown-wrapper'):
                                countdown_e = await page.querySelector('.pcode_countdown-wrapper')
                                display_attribute = await page.evaluate('(element) => window.getComputedStyle(element).getPropertyValue("display")', countdown_e)
                                if display_attribute == 'flex':
                                    if await page.querySelectorAll('#the_code'):
                                        the_code_element = await page.querySelector('#the_code')
                                        the_code_value = await page.evaluate('(element) => element.value', the_code_element)
                                        text_value[0] = the_code_value.strip()
                                        text_value[1] = page.url
                                        return text_value
                                    await page.evaluate('''() => {
                                        const button = document.querySelector('.next-page-btn');
                                        button.click();
                                    }''')
                                    await asyncio.sleep(30)
                                else:
                                    return ['','']
            
            if await page.querySelectorAll('#loading'):
                await asyncio.sleep(25)
                if await page.querySelectorAll('#generated-code'):
                    code_span = await page.querySelector('#generated-code')
                    code_span_text = await page.evaluate('(element) => element.textContent', code_span)
                    code_span_text = code_span_text.strip()
                    text_value[0] = code_span_text
                    text_value[1] = page.url
                    return text_value

            elif await page.querySelectorAll('.hurrytimer-cdt'):
                if await page.querySelectorAll('.hurrytimer-headline'):
                    headline = await page.querySelector('.hurrytimer-headline')
                    headline_text = await page.evaluate('(element) => element.textContent', headline)
                    headline_text = headline_text.lower()
                    if 'next' in headline_text:
                        continue
                    else:
                        await asyncio.sleep(30)
                else:
                    await asyncio.sleep(30)
                    
            timer_code = await page.querySelector('.hurrytimer-campaign-message')
            if timer_code:
                s = await page.evaluate('(element) => element.textContent', timer_code)
                
                if 'next post' in s.lower():
                    continue
                if ':' in s:
                    if 'Worker' in s:
                        s = s.split('Worker')[1]
                    text_value[0] = s.split(':')[1].strip()
                elif '-' in s:
                    text_value[0] = s.split('-')[1].strip()
                else:
                    text_value[0] = s.split('\n')[-1]
                text_value[1] = page.url
                return text_value
            
            kode_element = await page.querySelector('#kode')
            if kode_element:
                await asyncio.sleep(65)
                s = await page.evaluate('(element) => element.textContent', kode_element)

                if ':' in s:
                    text_value[0] = s.split(':')[1].strip()
                else:
                    text_value[0] = s
                text_value[1] = page.url
                return text_value

            center_elements = await page.querySelectorAll('.has-text-align-center')
            if center_elements:
                text_code = await page.evaluate('(element) => element.textContent', center_elements[-1])

                if ':' in text_code.lower():
                    text_value[0] = text_code.split(':')[1].strip()
                else:
                    text_value[0] = text_code.strip()
                text_value[1] = page.url
                return text_value

            if await page.querySelectorAll('.post-page-numbers'):
                page_numbers = await page.querySelectorAll('.post-page-numbers')
                page_numbers_urls = []
                for j in range(len(page_numbers) - 1):
                    current_page_url = page.url
                    if current_page_url[-1] != '/':
                        current_page_url = current_page_url + '/' + str(j+2)
                    else:
                        current_page_url = current_page_url + str(j+2)
                    page_numbers_urls.append(current_page_url)
                for j in page_numbers_urls:
                    await page.goto(j, {'timeout': 60000})
                    await asyncio.sleep(1)
                    if await page.querySelectorAll('.hurrytimer-timer'):
                        await asyncio.sleep(25)
                        if await page.querySelectorAll('.hurrytimer-campaign-message'):
                            timer_code = await page.querySelector('.hurrytimer-campaign-message')
                            if timer_code:
                                s = await page.evaluate('(element) => element.textContent', timer_code)
                                if ':' in s:
                                    if 'Worker' in s:
                                        s = s.split('Worker')[1]
                                    text_value[0] = s.split(':')[1].strip()
                                else:
                                    text_value[0] = s
                                text_value[1] = page.url
                                return text_value
                    await find_code_by_p(page, text_value)
                    if text_value[0] is not None and text_value[0] != '':
                      return text_value
            
            async def find_code_by_p(page, text_value):
                if 'evolva.site' in page.url or 'baelax.site' in page.url or 'venoms.site' in page.url or 'clashranger.com':
                    red_spans = await page.evaluate('''() => {
                        return Array.from(document.querySelectorAll('span')).filter(span => {
                            return window.getComputedStyle(span).color === 'rgb(255, 0, 0)';
                        }).map(span => span.textContent);
                    }''')

                    # Process the text content of red spans
                    for text in red_spans:
                        text = text.strip()
                        if len(text) == 5 and text.startswith('C'):
                            text_value[0] = text
                            text_value[1] = page.url
                            return

                else:
                    p_tags = await page.querySelectorAll('p, li, h1, h2, h3, strong, span, font')
                    if p_tags:
                        for p_element in p_tags[::-1]:
                            text_lower_ = await page.evaluate('(element) => element.textContent', p_element)
                            text_lower = text_lower_.lower()
                            if 'prnt' in text_lower or 'manual' in text_lower or 'https' in text_lower:
                                continue
                            if (any(keyword in text_lower for keyword in ['code :', 'code:', 'codes:', 'codes :', 'hint cd:']) and 9 < len(text_lower) < 55) or ('for proof' in text_lower):
                                if len(text_lower_) > 0:
                                    print(2)
                                    if ':' in text_lower_:
                                        text_value[0] = text_lower_.split(':')[1].strip()
                                    else:
                                        text_value[0] = text_lower_.strip()
                                    if len(text_value[0]) >= 2 and text_value[0][0] == '{' and text_value[0][-1] == '}':
                                        text_value[0] = text_value[0][1:-1]
                                    text_value[1] = page.url
                                    return
                                else:
                                    return

            await find_code_by_p(page, text_value)

            if text_value[0] and len(text_value[0]) > 0:
                return text_value
                
        return text_value
    except Exception as e:
        if key == 'admin':
            print("Exception at find_code ", e)
            import traceback
            traceback.print_exc()
    return ['', '']
