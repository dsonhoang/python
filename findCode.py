from urllib.parse import urlparse
import requests
import random
import asyncio
import pyppeteer
from pyppeteer import launch
import html

def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def matched_url(webiste_url, herf_url):
    black_words = ['home', 'resource', 'sitemap', 'tentang-kami',
                   'upload', 'pasang', 'category', 'author', 'page', 'disclaimer',
                   'privacy', 'policy', 'about', 'contac', 'tag', 'cookies', 'search',
                   'topic', 'topik', 'politica', 'legal', 'term', 'login', 'content',
                   'page', 'keyword', 'comment', 'feed', 'my-account']
    if webiste_url == herf_url:
        return False
    domain1 = get_domain(webiste_url)

    domain2 = get_domain(herf_url)

    if domain1 != domain2:
        return False

    if len(herf_url) - len(domain1) < 20:
        return False

    for word in black_words:
        if word in herf_url and word not in domain2:
            return False
    return True

async def get_copyright(page2, url, lkey):
    try:
        await page2.goto(url)
        if await page2.querySelectorAll('.copyright-bar'):
            copyright = await page2.querySelector('.copyright-bar')
            copyright_text = await page2.evaluate('(element) => element.textContent', copyright)
            return copyright_text.strip()
        else:
            p_elements = await page2.querySelectorAll('p')
            if p_elements:
                for p_tag in p_elements:
                    p_text = await page2.evaluate('(element) => element.textContent', p_tag)
                    if 'copyright' in p_text.lower() or '©' in p_text.lower() or 'all rights reserved' in p_text.lower():
                        return p_text.strip()
        return ''
    except Exception as e:
        if lkey == 'admin':
            print("Exception at get copyright", e)
            import traceback
            traceback.print_exc()
        return ""

async def get_keyword(page2, url, lkey):
    try:
        if url == 'https://cutt.ly/qeldKNfJ':
            return random.choice(['Bar Carts','Oil Machine', 'Chocolate Machine', 'Cbd Oil', 'Cbd Pen'])

        await page2.goto(url)
        await asyncio.sleep(3)

        if await page2.querySelectorAll('.C9DxTc'):
            # Find all elements with the class="C9DxTc"
            elements = await page2.querySelectorAll('.C9DxTc')

            italic_elements = []
            keywords = []
            for element in elements:
                # Check if the element has a style of font-style: italic
                is_italic = await page2.evaluate('(element) => window.getComputedStyle(element).fontStyle', element)
                if is_italic == 'italic':
                    italic_elements.append(element)

            if italic_elements:
                for i, element in enumerate(italic_elements):
                    # Get the text content of each element
                    text = await page2.evaluate('(element) => element.textContent', element)
                    keywords.append(text)
            return random.choice(keywords)
        else:
            return ''
    except Exception as e:
        if lkey == 'admin':
            print("Exception at get keyword", e)
            import traceback
            traceback.print_exc()
        return ""

async def get_sorted_url(page2, url, lkey):
    try:
        await page2.goto(url, {'timeout': 60000})
        await asyncio.sleep(2)

        a_links = []

        if await page2.querySelector('.inside-right-sidebar'):
            block_3_element = await page2.querySelector('.inside-right-sidebar')
            a_tags = await block_3_element.querySelectorAll('a')

            for a_tag in a_tags:
                if a_tag is not None:
                    href_value = await page2.evaluate('(element) => element.getAttribute("href")', a_tag)
                    if href_value is not None:
                        if get_domain(url) in href_value and 'http' not in href_value:
                            if 'www' in url:
                                href_value = 'https://www.' + get_domain(url) + href_value
                            else:
                                href_value = 'https://' + get_domain(url) + href_value

                        if get_domain(url) in href_value:
                            a_links.append(href_value.split('?')[0])

            return a_links
        elif await page2.querySelector('.wp-block-latest-posts__list'):
            lastest_post_list = await page2.querySelector('.wp-block-latest-posts__list')
            lastest_post_list_url = await lastest_post_list.querySelectorAll('a')

            for i in lastest_post_list_url:
                url = await page2.evaluate('(element) => element.getAttribute("href")', i)
                if url is not None and url not in a_links:
                    a_links.append(url)
            return a_links
        else:
            return []

    except Exception as e:
        if lkey == 'admin':
            print("Exception at get_sorted_url", e)
            import traceback
            traceback.print_exc()
        return []

async def get_all_url(page2, url, post_urls, post_titles, lkey):
    try:
        try:
            await page2.goto(url, {'timeout': 60000})
        except:
            return
        await asyncio.sleep(2)

        if await page2.querySelector('.content-area'):
            content_area = await page2.querySelector('.content-area')
            a_tags = await content_area.querySelectorAll('a')

        else:
            a_tags = await page2.querySelectorAll('a')

        for a_tag in a_tags:
            if a_tag:
                a_href = await page2.evaluate('(element) => element.getAttribute("href")', a_tag)
                if a_href:
                    a_href = a_href.split('#')[0]
                    a_href = a_href.split('?')[0]
                    if len(a_href) > 3:
                        if a_href[-1] == '/' and a_href[len(a_href) - 3] == '/':
                            a_href = a_href[0:len(a_href) - 2]

                    if get_domain(url) not in a_href:
                        if 'www' in url:
                            a_href = 'https://www.' + get_domain(url) + a_href
                        else:
                            a_href = 'https://' + get_domain(url) + a_href
                    if matched_url(url, a_href) and a_href not in post_urls:
                        post_urls.append(a_href)

                        a_text = await page2.evaluate('(element) => element.textContent', a_tag)
                        if a_text:
                            a_text = a_text.strip()
                            a_text = a_text.replace('\xa0', ' ').replace('\t', ' ').replace('\n', ' ').replace('\r', '').replace('\u200B', '')
                            if a_text.count(' ') >= 3 and a_text not in post_titles and 'http' not in a_text:
                                post_titles.append(a_text)

    except Exception as e:
        if lkey == 'admin':
            print('Exception at get_all_url', e)
            import traceback
            traceback.print_exc()
        return

async def get_sorted_para(page2, url, lkey):
    from bs4 import BeautifulSoup
    try:
        paragraph = []
        if 'electronix.ma' in url or 'mngames.online' in url or 'belajarsam' in url:
            try:
                response = requests.get(url, timeout=15)
            except requests.Timeout:
                return []
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.find(class_='theiaPostSlider_slides'):
                class_element = soup.find(class_='theiaPostSlider_slides')
                p_tags = class_element.find_all('p')
            else:
                p_tags = soup.find_all('p')

            exclude_words = ['copyright', '©', 'log in', 'click to']
            for p_tag in p_tags:
                exclude = False
                p_tag_text = p_tag.text
                for exclude_word in exclude_words:
                    if exclude_word in p_tag_text.lower():
                        exclude = True
                if not exclude:
                    tmp = ''
                    p_tag_lines = p_tag_text.split('\n')
                    for p_line in p_tag_lines:
                        tmp += p_line + ' '
                    paragraph.append(tmp.strip())
        else:
            count = 0
            while len(paragraph) == 0 and count < 3:
                try:
                    await page2.goto(url)
                except:
                    return []
                await asyncio.sleep(2)

                selectors = [
                    '.gap-1', '.p-3', '.entry-content', '.entry', '.cm-entry-summary', '.small', '.status-publish', '#the-post'
                ]
                container = page2
                for selector in selectors:
                    if await page2.querySelector(selector):
                        container = await page2.querySelector(selector)
                        break
                p_elements = await container.querySelectorAll('p')
                li_elements = await container.querySelectorAll('li')

                all_elements = p_elements + li_elements

                elements_with_y_coords = []

                for element in all_elements:
                    bounding_box = await element.boundingBox()
                    if bounding_box:
                        y_coord = bounding_box['y']
                        elements_with_y_coords.append((element, y_coord))

                sorted_elements = sorted(elements_with_y_coords, key=lambda x: x[1])

                sorted_elements = [elem[0] for elem in sorted_elements]

                all_elements = sorted_elements

                entry_text = ''
                for element in all_elements:
                    if element:
                        e_text = await page2.evaluate('(element) => element.textContent', element)
                        e_text = e_text.strip()
                        if len(e_text) > 0:
                            if 'read more' in e_text.lower():
                                break
                            exclude_words = ['copyright', '©', 'log in', 'click to']
                            exclude = False
                            for exclude_word in exclude_words:
                                if exclude_word in e_text.lower():
                                    exclude = True
                            if not exclude:
                                entry_text += e_text.strip() + '\n'

                entry_text = entry_text.strip()
                paragraph = entry_text.split('\n')
                count += 1

            if len(paragraph) < 2:
                return []

        for i in range(len(paragraph)):
            replacements = ['advertisment', 'Advertisment', 'ADVERTISMENT',
                            'advertisement', 'Advertisement', 'ADVERTISEMENT',
                            'ads', 'Ads', 'ADS', 'ad', 'Ad', 'AD',
                            'link', 'Link', 'LINK']

            for i in range(len(paragraph)):
                for word in replacements:
                    while word in paragraph[i]:
                        paragraph[i] = paragraph[i].replace(word, '')

        final_paragraph = []
        index = 0
        while index < len(paragraph):
            if len(paragraph[index]) > 150:
                final_paragraph.append(paragraph[index])
                index += 1
            else:
                tmp = paragraph[index]
                while len(tmp) < 150 and index < len(paragraph) - 1:
                    tmp += '\n' + paragraph[index + 1]
                    index += 1

                final_paragraph.append(tmp.strip())
                index += 1

        if len(final_paragraph) > 1:
            if len(final_paragraph[-1]) < 150:
                final_paragraph[len(final_paragraph) - 2] += '\n' + final_paragraph[-1]
                final_paragraph = final_paragraph[:-1]

        return final_paragraph
    except Exception as e:
        if lkey == 'admin':
            print('Exception at get_sorted_para', e)
            import traceback
            traceback.print_exc()
        return []

async def get_all_url_v2(page, post_urls, post_titles, lkey):
    from bs4 import BeautifulSoup
    if 'electronix.ma' in post_urls[0] or 'mngames.online' in post_urls[0] or 'belajarsam' in post_urls[0]:
        try:
            response = requests.get(post_urls[0], timeout=15)
        except requests.Timeout:
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        href_strings = [str(a.get('href')) for a in soup.find_all('a', href=True)]

        for a_href in href_strings:
            if 'redirect_to' in a_href:
                continue
            if '#' in a_href:
                a_href = a_href.split('#')[0]
            if matched_url(post_urls[0], a_href) and a_href not in post_urls:
                post_urls.append(a_href)

        return
    try:
        slash_positions = [pos for pos, char in enumerate(post_urls[0]) if char == '/']
        if 'www' in post_urls[0]:
            url = 'https://www.' + get_domain(post_urls[0])
        else:
            url = 'https://' + get_domain(post_urls[0])
        
        if len(slash_positions) >= 4:
            start = slash_positions[2] + 1
            end = slash_positions[3]
            extracted_text = post_urls[0][start:end]

            special_slash = ['studyus', 'us', 'eng', 'en', 'eco']

            if extracted_text in special_slash:
                if 'www' in post_urls[0]:
                    url = url + '/' + extracted_text + '/'
                else:
                    url = url + '/' + extracted_text + '/'

        await get_all_url(page, url, post_urls, post_titles, lkey)

        if len(post_urls) < 5:
            for j in range(len(post_urls)):
                await get_all_url(page, post_urls[j], post_urls, post_titles, lkey)

    except Exception as e:
        if lkey == "admin":
            print("Exception at get_all_url_v2", e)
            import traceback
            traceback.print_exc()

async def main():
    import getLinkToOpen
    browser = await launch(
        {'executablePath': 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'headless': False})
    page = await browser.newPage()

    post_urls = ['https://build.guratanku.com/2021/06/homes-for-sale-in-guyton-ga-with-pool.html']
    post_titles = []

    sorted_url = await get_sorted_url(page, post_urls[0], 'admin')
    await get_all_url_v2(page, post_urls, post_titles, 'admin')
    if len(sorted_url) == 0:
        sorted_url = post_urls

    for url in sorted_url:
        if 'http' in url and 'www.' not in url:
            if len(url) - len(get_domain(url)) < 10:
                sorted_url.remove(url)
        elif 'http' in url and 'www.' in url:
            if len(url) - len(get_domain(url)) < 14:
                sorted_url.remove(url)

    for url in post_urls:
        if 'http' in url and 'www.' not in url:
            if len(url) - len(get_domain(url)) < 10:
                post_urls.remove(url)
        elif 'http' in url and 'www.' in url:
            if len(url) - len(get_domain(url)) < 14:
                post_urls.remove(url)
    print(sorted_url)

    sorted_para = await get_sorted_para(page, sorted_url[0], 'admin')
    #print(sorted_para)

    print(post_titles)

    if True:
        import httpimport

        github_raw_url = 'https://raw.githubusercontent.com/dsonhoang/python/main/'

        with httpimport.remote_repo(github_raw_url):
            import findCode2
            code = await findCode2.find_code(page, sorted_url, 'admin')
            if code[0].count(' ') >= 3:
                print(code[0])
                code[0] = None
            print("code:", code[0], code[1])

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
