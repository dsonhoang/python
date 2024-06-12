import time
import asyncio
import pyppeteer
from pyppeteer.errors import ElementHandleError

async def find_pcode2(page, sorted_url, key):
    code_string = """
         var pcodeContainer = document.getElementById("pcode-container");
         var visitedPosts = 5
         var xhr = new XMLHttpRequest();
         xhr.open("POST", next_post_data.ajax_url, true);
         xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");

         xhr.onload = function () {
             if (xhr.status === 200) {
                 try {
                     var response = JSON.parse(xhr.responseText);
                     console.log("Server response:", response);

                     if (response.verification_success) {
                         console.log("Verification success");
                         pcodeContainer.style.display = "block";
                         var pcodeText = document.createElement("p");
                         pcodeText.style.color = "#00592a";
                         pcodeText.style.textAlign = "center";
                         pcodeText.style.fontWeight = "bold";
                         pcodeText.innerHTML = "PCODE: " + response.pcode;
                         pcodeContainer.innerHTML = "";
                         pcodeContainer.appendChild(pcodeText);
                         pcodeContainer.textValue
                     } else {
                         console.log("Verification failed");
                     }
                 } catch (error) {
                     console.error("Error parsing JSON:", error);
                 }
             } else {
                 console.error("Error in AJAX request. Status:", xhr.status);
             }
         };

         xhr.onerror = function () {
             console.error("Network error");
         };

         var data = "action=verify_visited_posts";
         console.log("Sending data:", data);
         xhr.send(data);
    """
    try:
        await page.goto(sorted_url[0])
        for i in range(5):
            await page.evaluate(code_string)
            await asyncio.sleep(2)
    
            pcode_container = await page.querySelector("#pcode-container")
            pcode_text = await page.evaluate('(element) => element.textContent', pcode_container)
            if pcode_text is not None and ':' in pcode_text:
                pcode_text = pcode_text.split(':')[1].strip()
                return [pcode_text, page.url]
            else:
                await asyncio.sleep(3)
        return ['','']
    except:
        return ['','']
async def find_pcode(page, sorted_url, key):
    if len(sorted_url) > 0:
        await page.goto(sorted_url[0])
        try:
            from urllib.parse import urlparse
            def get_domain(url):
               if '/kuismedia.id' in url:
                   return 'kuismedia.id/en'
               if '/ekonomiupri.id' in url:
                   return 'ekonomiupri.id/en'
               parsed_url = urlparse(url)
               domain = parsed_url.netloc
               if domain.startswith("www."):
                  domain = domain[4:]
               return domain
            domain = get_domain(sorted_url[0])
            js_code1 = f"""
               jQuery.ajax({{
                    type: "POST",
                    url: "https://{domain}/wp-admin/admin-ajax.php",
                    data: {{
                        action: "klik_iklan",
                        masuk: 'gass',
                    }},
                    dataType: 'json',
                    complete: function (response) {{
                    }},
               }});
            """

            await page.evaluate(js_code1)
            await asyncio.sleep(30)

            js_code2 = f"""
               jQuery.ajax({{
                    type: "POST",
                    url: "https://{domain}/wp-admin/admin-ajax.php",
                    data: {{
                        action: "validasi_iklan",
                        masuk: 'gass',
                    }},
                    dataType: 'json',
                    complete: function (response) {{
                        let hasil = JSON.parse(response.responseText);
                        if (hasil.status == 'isi') {{
                            var elem = document.querySelector('#pcode');
                            elem.innerHTML = "<strong>Pcode: " + hasil.pcode + "</strong>";
                        }} else {{
                            var elem = document.querySelector('#pcode');
                            elem.innerHTML = "<strong>Pcode will appear after do the&nbsp;step5</strong>";
                        }}
                    }},
               }});
            """

            ans = await page.evaluate(js_code2)
            if 'pcode' in ans:
                result = ans['pcode']
                return [result, page.url]
            else:
                return ['','']
            await asyncio.sleep(5)
        except ElementHandleError as e:
            if key == 'admin':
                print("ElementHandleError")
                return ['','']
        except Exception as e:
            if key == 'admin':
                print("Exception at find_pcode ", e)
                import traceback
                traceback.print_exc()
            return ['','']
    else:
        return ['', '']
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
                if 'frankenstein' in i:
                    i = 'https://frankenstein45.com/inter/nine-guilt-free-donate-car-tips/'
                elif 'cpstesters' in i:
                    i = 'https://cpstesters.com/tap-counter/'
                elif 'unidosenoracion.org' in i:
                    i = 'https://unidosenoracion.org/united-in-prayer/'
                await page.goto(i)
                await asyncio.sleep(1)
                await page.evaluate('() => window.scrollTo(0, document.documentElement.scrollHeight)')
            except:
                continue

            if await page.querySelector('#countdownContainer'):
                try:
                    await page.goto('view-source:'+post_urls[0])
                    await asyncio.sleep(2)
                    page_content = await page.content()
                    index = page_content.find('codeElement.textContent')
        
                    sub_string = page_content[index:]
        
                    first_index = sub_string.find("'")
                    second_index = sub_string.find("'", first_index + 5)
        
                    # Extract the desired text between the two spaces
                    code_text = sub_string[first_index + 1:second_index].split(':')[1].strip()
                    text_value[0] = code_text
                    text_value[1] = page.url
                    return text_value
                except:
                    return ['', '']

            if await page.querySelectorAll('.arpw-random-post'):
                digits_code = ''
                for c in range(5):
                    arpw_random_post = await page.querySelector('.arpw-random-post')
                    links = await arpw_random_post.querySelectorAllEval('a', 'nodes => nodes.map(a => a.href)')
                    first_link = links[0] if links else None
                    if first_link:
                        if c == 4:
                            text_value[1] = first_link
                        await page.goto(first_link)
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

            if await page.querySelectorAll('.has-base-2-color'):
                code_span = await page.querySelector('.has-base-2-color')
                code_span_text = await page.evaluate('(element) => element.textContent', code_span)
                code_span_text = code_span_text.strip()
                
                if 'code:' in code_span_text.lower():
                    code_span_text = code_span_text.split(':')[1].strip()
                    
                text_value[0] = code_span_text
                text_value[1] = page.url
                return text_value

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
            if await page.querySelectorAll('#hid'):
                html = await page.content()
                html_lines = html.split('\n')
                for line in html_lines:
                    if 'code:' in line.lower():
                        line = line.split(':')[1].replace('"', '').strip()
                        return [line, page.url]
            if await page.querySelectorAll('#loading'):
                await asyncio.sleep(25)
                if await page.querySelectorAll('#generated-code'):
                    code_span = await page.querySelector('#generated-code')
                    code_span_text = await page.evaluate('(element) => element.textContent', code_span)
                    code_span_text = code_span_text.strip()
                    text_value[0] = code_span_text
                    text_value[1] = page.url
                    return text_value
            elif await page.querySelectorAll('#pcode'):
                ans = await find_pcode(page, sorted_url, key)
                return ans

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
                    
            elif await page.querySelectorAll('.detail_lagi'):
                current_page_num = await page.evaluate('(element) => element.textContent', await page.querySelector('.info_page'))
                try:
                    current_page_num = int(current_page_num.strip())
                except:
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
                        text_value[0] = s.split(':')[1].strip()
                    else:
                        text_value[0] = s
                    text_value[1] = page.url

                    return text_value
            timer_code = await page.querySelector('.hurrytimer-campaign-message')
            if timer_code:
                s = await page.evaluate('(element) => element.textContent', timer_code)
                if ':' in s:
                    if 'Worker' in s:
                        s = s.split('Worker')[1]
                    text_value[0] = s.split(':')[1].strip()
                elif '-' in s:
                    text_value[0] = s.split('-')[1].strip()
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
                                        text_value[0] = tmp_text_.split(':')[1].strip()
                                        if len(text_value[0]) >= 2 and text_value[0][0] == '{' and text_value[0][-1] == '}':
                                            text_value[0] = text_value[0][1:-1]
                                        text_value[1] = page.url
                                        return text_value
                            if 'https' in text_lower:
                                continue
                            if len(text_lower_) > 0:
                                if ':' in text_lower_:
                                    text_value[0] = text_lower_.split(':')[1].strip()
                                else:
                                    text_value[0] = text_lower_.strip()
                                if len(text_value[0]) >= 2 and text_value[0][0] == '{' and text_value[0][-1] == '}':
                                    text_value[0] = text_value[0][1:-1]
                                text_value[1] = page.url
                                return text_value
                            else:
                                return None
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
            else:
                await find_code_by_p(page, text_value)
                if text_value[0] is not None and text_value[0] != '':
                    return text_value
                
        return text_value
    except Exception as e:
        if key == 'admin':
            print("Exception at find_code ", e)
            import traceback
            traceback.print_exc()
    return ['', '']
