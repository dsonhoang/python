import time
import asyncio
import pyppeteer

async def find_code(page, sorted_url, key):
    try:
        if len(sorted_url) == 0:
            return ['', '']
        text_value = ['', '']
        count = 0
        for i in reversed(sorted_url):
            count += 1
            try:
                await page.goto(i)
                #await asyncio.sleep(2)
            except:
                continue

            # Check if the element with ID 'kode' is present
            if await page.querySelectorAll('.hurrytimer-cdt'):
                await asyncio.sleep(25)
            elif await page.querySelectorAll('.detail_lagi'):
                if count >= 5:
                    await asyncio.sleep(12)
                if count == 7:
                    return ['', '']
                await asyncio.sleep(21)
                code_block = await page.querySelectorAll('.detail_lagi')
                code_block_text = await page.evaluate('(element) => element.textContent', code_block[2])
                code_block_text = code_block_text.strip()
                print("aaa", code_block_text)
                if len(code_block_text.split(':')[1].strip()) > 0:
                    s = code_block_text.split(':')[1].strip()
                    if ':' in s:
                        text_value[0] = s.split(':')[1].strip()
                    else:
                        text_value[0] = s
                    text_value[1] = page.url
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
                    if any(keyword in text_lower for keyword in ['code :', 'code:', 'codes:', 'codes :', 'hint cd:']) and 6 < len(text_lower) < 35:
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
