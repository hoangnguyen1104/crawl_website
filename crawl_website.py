import requests
from bs4 import BeautifulSoup

def get_name_from(url):
    chars = ['.', '/', ':', '|', '*', '?', '<', '>']
    for c in chars:
        url = url.replace(c, '')
    return url

def get_text(html_selector):
    soup = BeautifulSoup(html_selector, 'html.parser')
    text = soup.get_text()
    return text.strip()


def get_tag_class(html_selector):
    soup = BeautifulSoup(html_selector, 'html.parser')
    root_tag = soup.find().name
    root_class = soup.find().get('class')
    return root_tag, root_class


def find_element_by_text(soup, text_selector):
    return soup.find(text=str(text_selector)).parent


def get_soup(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def get_element(soup, _tag, _class):
    return soup.find(_tag, class_=_class)


def remove_scripts_tag(soup):
    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        script_tag.extract()
    return soup


def remove_form_tag(soup):
    form_tags = soup.find_all('form')
    for form_tag in form_tags:
        form_tag.extract()
    return soup


def unwrap_noscript_tag(soup):
    noscript_tags = soup.find_all('noscript')
    for noscript_tag in noscript_tags:
        noscript_tag.unwrap()
    return soup

def crawl_website(url, post, title, content):
    soup = get_soup(url)
    html_selector = post
    target_element = find_element_by_text(soup, get_text(html_selector))
    parent_element = target_element.parent
    parent_tag = parent_element.name
    parent_class = parent_element.get('class')
    posts = soup.find_all(parent_tag, class_=parent_class)
    for post in posts:
        link = post.find('a')['href']
        print(post, link)
        p_soup = get_soup(link)

        _tag, _class = get_tag_class(title)
        title_soup = get_element(p_soup, _tag, _class)
        title_soup = remove_scripts_tag(title_soup)
        title_soup = remove_form_tag(title_soup)
        title_soup = unwrap_noscript_tag(title_soup)
        print(title_soup)

        _tag, _class = get_tag_class(content)
        content_soup = get_element(p_soup, _tag, _class)
        content_soup = remove_scripts_tag(content_soup)
        content_soup = remove_form_tag(content_soup)
        content_soup = unwrap_noscript_tag(content_soup)

        with open("info_link.txt", 'a', encoding="utf-8") as file:
            file.write(link + "\n")
        print(content_soup)

        file_name_txt = get_name_from(link) + '.txt'
        file_name_html = get_name_from(link) + '.html'
        with open(file_name_txt, 'w', encoding="utf-8") as file:
            file.write(f"{title_soup.prettify()}\n{content_soup.prettify()}")
        # Đổi tên file thành .html
        import os
        os.rename(file_name_txt, file_name_html)


# url = 'https://sportswiftly.com/'
# soup = get_soup(url)
# # print(soup.prettify())
# html_selector = '''<a href="https://sportswiftly.com/2024/01/in-the-chiefs-latest-injury-report-its-been-confirmed-that-four-players-will-be-unavailable-for-week-18/">In the Chiefs’ latest injury report, it’s been confirmed that four players will be unavailable for Week 18</a>'''
# target_element = find_element_by_text(soup, get_text(html_selector))
# parent_element = target_element.parent
# parent_tag = parent_element.name
# parent_class = parent_element.get('class')
# posts = soup.find_all(parent_tag, class_=parent_class)
#
# for post in posts:
#     link = post.find('a')['href']
#     print(post, link)
#     p_soup = get_soup(link)
#     title = '''<header class="entry-header">
#
# 		<h1 class="entry-title">Report: Dolphins Offensive Lineman Robert Hunt Opens Up About Injury sidelining Him for Four Weeks</h1>
# 		<div class="entry-meta">
#
# 	<span class="entry-category"><a href="https://sportswiftly.com/category/nfl/miami-dolphins/">Miami Dolphins</a> </span>
# 	<span class="entry-author"><a href="https://sportswiftly.com/author/tranchi/" title="Posts by tranchi" rel="author">tranchi</a></span>
# 	<span class="sep author-sep">·</span>
# 	<span class="entry-date">January 6, 2024</span>
# 	<span class="sep">·</span>
# 	<span class="entry-comment"><span class="comments-link">Comments off</span></span>
#
# </div>
#
# 	</header>'''
#
#     _tag, _class = get_tag_class(title)
#     title_soup = get_element(p_soup, _tag, _class)
#     title_soup = remove_scripts_tag(title_soup)
#     title_soup = remove_form_tag(title_soup)
#     title_soup = unwrap_noscript_tag(title_soup)
#     print(title_soup)
#
#     content = '''<div class="entry-content">
#
# 		<div class="code-block code-block-1" style="margin: 8px 0; clear: both;">
# <!-- Composite Start -->
#  <div id="M926730ScriptRootC1568896_1168a">
#  </div>
#  <script src="https://jsc.mgid.com/s/p/sportswiftly.com.1568896.js" async="">
#  </script>
#  <!-- Composite End --> </div>
# <div class="td_block_wrap tdb_single_featured_image tdi_42 tdb-content-horiz-left td-pb-border-top td_block_template_1" data-td-block-uid="tdi_42">
# <div class="tdb-block-inner td-fix-index">
# <figure><img fetchpriority="high" decoding="async" class="entry-thumb" title="Dolphins Offensive Lineman Robert Hunt Opens Up About Injury sidelining Him for Four Weeks" src="https://i0.wp.com/fanrecap.com/wp-content/uploads/2024/01/article-341518.jpg?resize=696%2C392&amp;ssl=1" sizes="(max-width: 696px) 100vw, 696px" srcset="https://i0.wp.com/fanrecap.com/wp-content/uploads/2024/01/article-341518.jpg?w=1024&amp;ssl=1 1024w, https://i0.wp.com/fanrecap.com/wp-content/uploads/2024/01/article-341518.jpg?resize=300%2C169&amp;ssl=1 300w, https://i0.wp.com/fanrecap.com/wp-content/uploads/2024/01/article-341518.jpg?resize=768%2C432&amp;ssl=1 768w, https://i0.wp.com/fanrecap.com/wp-content/uploads/2024/01/article-341518.jpg?resize=696%2C392&amp;ssl=1 696w" alt="Featured picture for " width="696" height="392"></figure>
# </div>
# </div>
# <div class="wpb_wrapper td_block_wrap td_block_wrap tdb_single_current_post tdi_43  td-pb-border-top td_block_template_1">
# <div class="td-fix-index">
# <div id="featured_video"></div>
# </div>
# </div>
# <div class="td_block_wrap tdb_single_content tdi_44 td-pb-border-top td_block_template_1 td-post-content tagdiv-type" data-td-block-uid="tdi_44">
# <div class="tdb-block-inner td-fix-index">
# <ul>
# <li>Miami Dolphins have experienced numerous injuries to their offensive line, using 11 different combinations of starters this season, including right guard Robert Hunt.</li>
# <li>In Week 18 against the Buffalo Bills, there’s a possibility that Hunt will make a return to the field, a crucial game that will determine the division winner and the AFC playoffs’ No. 2 seed.</li>
# <li>Hunt expressed frustration regarding his absence, praising his teammates for stepping up, and is eager to play with them again, comparing his current injury to a previous one and underlining its severity. He believes his fellow linemen have done an excellent job in his absence and looks forward to contributing himself.</li>
# </ul>
# <p>The Miami Dolphins have been dealing with injuries to their offensive line throughout the 2023 season. They have had to use 11 different combinations of starters this year. Right guard Robert Hunt is one of the players who has been in and out of the lineup. This is new territory for him as he had played in every game from 2020-2022 but has already missed six games this season and played just one snap on special teams in another game.</p>
# <p>However, there is a possibility that Hunt will return to the field in Week 18 against the Buffalo Bills. This is a crucial game that will determine the division winner and the No. 2 seed in the AFC playoffs. Hunt expressed his frustration with his absence and praised his teammates who have stepped up in his absence. He is eager to play with them again.</p>
# <p>This is the second time Hunt has missed games this season. He compared it to his previous absence and said it was similar in severity. He emphasized that he wouldn’t sit out if it was not a serious issue.</p>
# <p>During his time off, Hunt has been impressed with the performance of his fellow offensive linemen. He believes they have done a fantastic job despite the injuries. He is excited to get back on the field and contribute to the team’s success.</p>
# <p>If Hunt does return for the upcoming game, it will be a significant boost for the Dolphins’ offensive line, which could benefit from the presence of more experienced players.</p>
# </div>
# </div>
# <div class="td_block_wrap td_flex_block_1 tdi_45 td-pb-border-top td_block_template_2 td_flex_block" data-td-block-uid="tdi_45">
# <div class="td-block-title-wrap"></div>
# </div>
# <div class="code-block code-block-3" style="margin: 8px 0; clear: both;">
# <!-- Composite Start -->
# <div id="M926730ScriptRootC1555572_0af11"></div>
# <script src="https://jsc.mgid.com/s/p/sportswiftly.com.1555572.js" async=""></script>
# <!-- Composite End --></div>
# <!-- AI CONTENT END 1 -->
# 	</div>'''
#
#     _tag, _class = get_tag_class(content)
#     content_soup = get_element(p_soup, _tag, _class)
#     content_soup = remove_scripts_tag(content_soup)
#     content_soup = remove_form_tag(content_soup)
#     content_soup = unwrap_noscript_tag(content_soup)
#
#     with open("info_link.txt", 'a') as file:
#         file.write(link + "\n")
#     print(content_soup)
#     file_name_txt = str(link).split('/')[-2] + '.txt'
#     file_name_html = str(link).split('/')[-2] + '.html'
#     with open(file_name_txt, 'w') as file:
#         file.write(f"{title_soup.prettify()}\n{content_soup.prettify()}")
#     # Đổi tên file thành .html
#     import os
#     os.rename(file_name_txt, file_name_html)

