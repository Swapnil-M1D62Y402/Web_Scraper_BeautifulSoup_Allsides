"""

Website Doc - https://www.learndatasci.com/tutorials/ultimate-guide-web-scraping-w-python-requests-and-beautifulsoup/

First Go the any website, Say "https://www.youtube.com/robots.txt" and see which are allowed and disallowed by the bots

In case of youtube, you will see the Following: 

# robots.txt file for YouTube
# Created in the distant future (the year 2000) after
# the robotic uprising of the mid 90's which wiped out all humans.

User-agent: Mediapartners-Google*
Disallow:

User-agent: *
Disallow: /api/
Disallow: /comment
Disallow: /feeds/videos.xml
Disallow: /get_video
Disallow: /get_video_info
Disallow: /get_midroll_info
Disallow: /live_chat
Disallow: /login
Disallow: /qr
Disallow: /results
Disallow: /signup
Disallow: /t/terms
Disallow: /timedtext_video
Disallow: /verify_age
Disallow: /watch_ajax
Disallow: /watch_fragments_ajax
Disallow: /watch_popup
Disallow: /watch_queue_ajax
Disallow: /youtubei/

Sitemap: https://www.youtube.com/sitemaps/sitemap.xml
Sitemap: https://www.youtube.com/product/sitemap.xml


Here * means all the bots (us), and what we are disallowed. 


Step 1: 

>>pip install requests

We will use requests library to send a GET request and get the html, as feedback from the website

Note: 

    You might want to use proxy to mask your IP, as website might think you are doing 
    illegal activity (Denial-Of-Service DDos attack). Proxy acts as a middle man 
    and lets you safely mine data. 

    The Crawl-delay tells us the number of seconds to wait before requests, 
    so in this example we need to wait 10 seconds before making another request

Step 2:

    Use BeautifulSoup to get page from AllSides server to parse HTML and XML

    >> pip install beautifulsoup4
    >> soup = BeautifulSoup(r.content, 'html-parser')

    Here soup Object defines a bunch of methods that we can use to extract data from the HTML 

Step 3:

    `select_one` - returns a single element 
    `select` - returns a list of elements

    to refresh on CSS selector - https://www.w3schools.com/cssref/css_selectors.php


Step 4:

    By inspecting the target website, to get the table values, 
    CSS selector is
    >>#block-views-list-of-ratings-block > div > div.view-content > table > tbody

    >> pip install lxml ---> better parser

Step 5:

    To extract the specific of each row data 
    [News source name and link, 
    Bias data
    Agreement buttons
    Community feedback data]

    First, take a look at News Source name "Associated Press"

    <td class="views-field views-field-title">
            <a href="/news-source/associated-press-media-bias">Associated Press
            </a>          
    </td>

    >> CSS selector: #block-views-list-of-ratings-block > div > div.view-content > table > tbody > tr.odd.views-row-first > td.views-field.views-field-title > a
    >> ..views-field-title

    Notice we dont need to worry about anchor tag, we can just use "text" to extract
    the text between the tags 

    `.strip()` ensures that all whitespaces surrounding the name is removed

Step 6:

    Getting the link to one of the News Outlets 
    Getting the link was a bit different than just selecting an element.
    We had to access an attribute (href) of the element, 
    which is done using brackets, like how we would access a Python dictionary.
    This will be the same for other attributes of elements, like src in images and videos

Step 7:
    
    <img typeof="foaf:Image" 
    src="https://www.allsides.com/sites/default/files/styles/bias120x20/public/bias-right.png?itok=ANql_Ox9" 
    width="120" 
    height="20" 
    alt="AllSides Media Bias Rating: Right" 
    title="AllSides Media Bias Rating: Right">

    <td class="views-field views-field-field-bias-image">
        <a href="/media-bias/right"><img typeof="foaf:Image" 
        src="https://www.allsides.com/sites/default/files/styles/bias120x20/public/bias-right.png?itok=ANql_Ox9"
        width="120" height="20" alt="AllSides Media Bias Rating: Right"
        title="AllSides Media Bias Rating: Right">
        </a>          
    </td>

Step 8:

    <div class="rate-widget-4 rate-widget clear-block rate-average rate-widget-yesno rate-c1839f412d43f34ad588d9ac367a9b99 rate-node-3515-4-1 rate-processed" id="rate-node-3515-4-1">
    <div class="item-list"><ul><li class="first"><a class="rate-button rate-btn btn" id="rate-button-3" rel="nofollow" href="/media-bias?rate=-SGBqO8D5hZUwgHbyb16LBBpOR-4JO5INn78Tu4Od0g" title="agree">agree</a></li>
    <li class="last"><a class="rate-button rate-btn btn" id="rate-button-4" rel="nofollow" href="/media-bias?rate=zuEcSEGQjDEy5fvUNtdpVFffTEvd9p9RD_HS5ffRYuE" title="disagree">disagree</a></li>
    </ul></div>

    <div class="rate-details green4">

---><span class="agree">39474</span>/<span class="disagree">32072</span>
    <br>

    </div>
    </div>

    Out of all these lines we want this specific line 
    >><span class="agree">39474</span>/<span class="disagree">32072</span>

Step 9:
    Get the Community rating 

Step 10:

    
"""

import requests
from bs4 import BeautifulSoup
import tqdm._tqdm

url = 'https://www.allsides.com/media-bias/media-bias-ratings'
r = requests.get(url)
#print(r.content[:100]) # to check is get request is successfull or not

soup = BeautifulSoup(r.content, 'lxml')



#To get each row, we select <tr> inside <tbody> ie tr is the child tag of tbody parent tag
rows = soup.select('tbody tr')
print(f"Table rows length: {len(rows)}")



#Getting the News outlet name 
row = rows[0]
name = row.select_one('.views-field-title').text.strip()
print(name)


#In order to get the link of the News outlet too, we will consider the anchor tag too
allsides_page = row.select_one('.views-field-title a')['href']
allsides_page = 'https://www.allsides.com' + allsides_page
print(allsides_page)


#To get the rating in text 
bias = row.select_one('.views-field-field-bias-image a')['href']
bias = bias.split('/')[-1] #<a href="/media-bias/right"> -->right
print(bias)


#to get the agree and disagree from each row
agree = row.select_one('.agree').text 
agree = int(agree)

disagree = row.select_one('.disagree').text 
disagree = int(disagree)

agree_ratio = agree / disagree

print(f"Agree: {agree} | Disagree: {disagree} | Agree-Ratio: {agree_ratio:.2f}")


#To get the Community Agreeance text 
#agreeance_text = row.select_one('.community-feedback-rating-page span')
#print(agreeance_text)
#the above will not work as it is rendered by javascript 

def get_agreeance_text(ratio):
    if ratio > 3: return "absolutely agrees"
    elif 2 < ratio <= 3: return "strongly agrees"
    elif 1.5 < ratio <= 2: return "agrees"
    elif 1 < ratio <= 1.5: return "somewhat agrees"
    elif ratio == 1: return "neutral"
    elif 0.67 < ratio < 1: return "somewhat disagrees"
    elif 0.5 < ratio <= 0.67: return "disagrees"
    elif 0.33 < ratio <= 0.5: return "strongly disagrees"
    elif ratio <= 0.33: return "absolutely disagrees"
    else: return None


pages = [
    'https://www.allsides.com/media-bias/media-bias-ratings',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=1',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=2'
]

from time import sleep 

data = []

for page in pages:
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'lxml')

    rows = soup.select('tbody tr')

    for row in rows:
        d = dict()

        d['name'] = row.select_one('.views-field-title').text.strip()
        d['allsides_page'] = 'https://www.allsides.com' + row.select_one('.views-field-title a')['href']
        d['bias'] = row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1]
        d['agree'] = int(row.select_one('.agree').text)
        d['disagree'] = int(row.select_one('.disagree').text)
        d['agree_ratio'] = d['agree'] / d['disagree']
        d['agreeance_text'] = get_agreeance_text(d['agree_ratio'])
        data.append(d)
    
    sleep(10)

#to get all the website links

from copy import deepcopy
import tqdm

for d in tqdm.tqdm(data):
    r = requests.get(d['allsides_page'])
    soup = BeautifulSoup(r.content, 'lxml')

    try:
        website = soup.select_one('.www')['href']
        d['website'] = website
    except TypeError:
        pass
    sleep(10)

import json 
with open('allsides.json', 'w') as f:
    json.dump(data, f)

