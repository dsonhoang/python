import time
import asyncio
import pyppeteer

async def find_code(page, sorted_url, key):
    try:
        if len(sorted_url) == 0:
            return ['', '']
        
        await page.goto(sorted_url[0])
        await asyncio.sleep(3)
        text_value = ['', '']

        for i in reversed(sorted_url):
            try:
                await page.goto(i)
            except:
                continue

            # Check if the element with ID 'kode' is present
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
            p_tags = await page.querySelectorAll('p, li, h1, h2, h3, strong')
            if p_tags:
                for p_element in p_tags:
                    text_lower_ = await page.evaluate('(element) => element.textContent', p_element)
                    text_lower = text_lower.lower()
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
