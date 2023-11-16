import time
import asyncio
import pyppeteer

async def find_code(page, sorted_url, key):
    try:
        if len(sorted_url) == 0:
            return ['', '']
        text_value = ['', '']
        count = 0

        num_pages = 0
        for i in reversed(sorted_url):
            count += 1
            try:
                await page.goto(i)
                await page.evaluate('() => window.scrollTo(0, document.documentElement.scrollHeight)')
            except:
                continue

            # Check if the element with ID 'kode' is present
            if await page.querySelectorAll('.hurrytimer-cdt'):
                await asyncio.sleep(30)
            elif await page.querySelectorAll('.detail_lagi'):
                current_page_num = await page.evaluate('(element) => element.textContent', await page.querySelector('.info_page'))
                try:
                    current_page_num = int(current_page_num.strip())
                except:
                    print("Error page num", current_page_num)
                    current_page_num = 0

                if current_page_num > num_pages:
                    num_pages = current_page_num
                    
                if count > num_pages + 2:
                    return ['', '']
                try:
                    time_wait = await page.querySelector('.info_detik')
                    time_wait = await page.evaluate('(element) => element.textContent', time_wait)
                    time_wait = int(time_wait.strip())
                except:
                    time_wait = None
                if time_wait:
                    await asyncio.sleep(time_wait + 5)
                else:
                    await asyncio.sleep(30)
                
                code_block = await page.querySelectorAll('.detail_lagi')
                code_block_text = await page.evaluate('(element) => element.textContent', code_block[2])
                code_block_text = code_block_text.strip()
                if len(code_block_text.split(':')[1].strip()) > 5:
                    s = code_block_text.split(':')[1].strip()
                    if ':' in s:
                        text_value[0] = s.split(':')[1].strip()
                    else:
                        text_value[0] = s
                    text_value[1] = page.url

                    return text_value
            timer_code = await page.querySelector('.hurrytimer-campaign-message')
            if timer_code:
                s = await page.evaluate('(element) => element.textContent', timer_code)
                if ':' in s:
                    text_value[0] = s.split(':')[1].strip()
                else:
                    text_value[0] = s
                text_value[1] = page.url
                return text_value
            kode_element = await page.querySelector('#kode')
            if kode_element:
                s = await page.evaluate('(element) => element.textContent', kode_element)

                if ':' in s:
                    text_value[0] = s.split(':')[1].strip()
                else:
                    text_value[0] = s
                text_value[1] = page.url
                return text_value

            # Check if elements with class 'has-text-align-center' are present
            center_elements = await page.querySelectorAll('.has-text-align-center')
            if center_elements:
                text_code = await page.evaluate('(element) => element.textContent', center_elements[-1])

                if ':' in text_code.lower():
                    text_value[0] = text_code.split(':')[1].strip()
                else:
                    text_value[0] = text_code.strip()
                text_value[1] = page.url
                return text_value

            # Check various elements for specific keywords
            p_tags = await page.querySelectorAll('p, li, h1, h2, h3, strong, span')
            if p_tags:
                for p_element in p_tags:
                    text_lower_ = await page.evaluate('(element) => element.textContent', p_element)
                    text_lower = text_lower_.lower()
                    if any(keyword in text_lower for keyword in ['code :', 'code:', 'codes:', 'codes :', 'hint cd:']) and 9 < len(text_lower) < 55:
                        text_value[0] = text_lower_.split(':')[1].strip()
                        text_value[1] = page.url
                        return text_value

        return text_value
    except Exception as e:
        if key == 'admin':
            print("Exception at find_code ", e)
            import traceback
            traceback.print_exc()
    return ['', '']
