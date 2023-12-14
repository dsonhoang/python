import time
import asyncio
import pyppeteer

async def find_code(page, sorted_url, key):
    try:
        if len(sorted_url) == 0:
            return ['', '']
        text_value = [[], []]
        count = 0

        num_pages = 0
        for i in reversed(sorted_url):
        #for i in sorted_url:
            count += 1
            try:
                if 'frankenstein' in i:
                    i = 'https://frankenstein45.com/inter/nine-guilt-free-donate-car-tips/'
                await page.goto(i)
                await asyncio.sleep(1)
                await page.evaluate('() => window.scrollTo(0, document.documentElement.scrollHeight)')
            except:
                continue

            if await page.querySelectorAll('.hurrytimer-cdt'):
                await asyncio.sleep(30)
                if not (await page.querySelectorAll('.hurrytimer-campaign-message')):
                    await asyncio.sleep(40)
            elif await page.querySelectorAll('.detail_lagi'):
                current_page_num = await page.evaluate('(element) => element.textContent', await page.querySelector('.info_page'))
                try:
                    current_page_num = int(current_page_num.strip())
                except:
                    current_page_num = 0

                if current_page_num > num_pages:
                    num_pages = current_page_num
                    
                if count > num_pages + 2:
                    return [[], []]
                try:
                    time_wait = await page.querySelector('.info_detik')
                    time_wait = await page.evaluate('(element) => element.textContent', time_wait)
                    time_wait = int(time_wait.strip())
                except:
                    time_wait = None
                if time_wait:
                    await asyncio.sleep(time_wait + 3)
                else:
                    await asyncio.sleep(30)
                if num_pages - count <= 1:
                    await asyncio.sleep(12)
                
                code_block = await page.querySelectorAll('.detail_lagi')
                code_block_text = await page.evaluate('(element) => element.textContent', code_block[2])
                code_block_text = code_block_text.strip()
                if len(code_block_text.split(':')[1].strip()) > 5:
                    s = code_block_text.split(':')[1].strip()
                    if ':' in s:
                        text_value[0].append(s.split(':')[1].strip())
                    else:
                        text_value[0].append(s)
                    text_value[1].append(page.url)
                    
            timer_code = await page.querySelector('.hurrytimer-campaign-message')
            if timer_code:
                s = await page.evaluate('(element) => element.textContent', timer_code)
                if ':' in s:
                    text_value[0].append(s.split(':')[1].strip())
                else:
                    text_value[0].append(s)
                text_value[1].append(page.url)
            kode_element = await page.querySelector('#kode')
            if kode_element:
                s = await page.evaluate('(element) => element.textContent', kode_element)

                if ':' in s:
                    text_value[0].append(s.split(':')[1].strip())
                else:
                    text_value[0].append(s)
                text_value[1].append(page.url)

            # Check if elements with class 'has-text-align-center' are present
            center_elements = await page.querySelectorAll('.has-text-align-center')
            if center_elements:
                text_code = await page.evaluate('(element) => element.textContent', center_elements[-1])

                if ':' in text_code.lower():
                    text_value[0].append(text_code.split(':')[1].strip())
                else:
                    text_value[0].append(text_code.strip())
                text_value[1].append(page.url)

            async def find_code_by_p(page, text_value):
                p_tags = await page.querySelectorAll('p, li, h1, h2, h3, strong, span, font')
                if p_tags:
                    for p_element in p_tags[::-1]:
                        text_lower_ = await page.evaluate('(element) => element.textContent', p_element)
                        text_lower = text_lower_.lower()
                        if 'prnt' in text_lower or 'manual' in text_lower:
                            continue
                        if (any(keyword in text_lower for keyword in ['code :', 'code:', 'codes:', 'codes :', 'hint cd:']) and 9 < len(text_lower) < 55) or ('for proof' in text_lower):
                            if 'auto link code :' and 'http' in text_lower:
                                link_code = text_lower.split('auto link code :')[1].strip()
                                await page.goto(link_code)
                                await asyncio.sleep(1)
                                p_tags_2 = await page.querySelectorAll('p, li, h1, h2, h3, strong, span')
                                for p_element_2 in p_tags_2[::-1]:
                                    tmp_text_ = await page.evaluate('(element) => element.textContent', p_element_2)
                                    tmp_text = tmp_text_.lower()
                                    if any(keyword2 in tmp_text for keyword2 in ['code :', 'code:', 'codes:', 'codes :', 'hint cd:']) and 9 < len(tmp_text) < 55:
                                        text_value[0].append(tmp_text_.split(':')[1].strip())
                                        if len(text_value[0]) >= 2 and text_value[0][0] == '{' and text_value[0][-1] == '}':
                                            text_value[0].append(text_value[0][1:-1])
                                        text_value[1].append(page.url)
                                        
                            if 'https' in text_lower:
                                continue
                            text_value[0].append(text_lower_.split(':')[1].strip())
                            if len(text_value[0][-1]) >= 2 and text_value[0][-1][0] == '{' and text_value[0][-1][-1] == '}':
                                text_value[0][-1] = text_value[0][-1][1:-1]
                            text_value[1].append(page.url)
                            
            # Check various elements for specific keywords
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
                    await page.goto(j)
                    await asyncio.sleep(1)
                    await find_code_by_p(page, text_value)
            else:
                await find_code_by_p(page, text_value)
                
        return text_value
    except Exception as e:
        if key == 'admin':
            print("Exception at find_code ", e)
            import traceback
            traceback.print_exc()
    return [[], []]