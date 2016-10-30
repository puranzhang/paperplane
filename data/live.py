import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import urllib
import re
#from IPython.display import display, HTML
import HTMLParser

for num in range(200):

    link = urllib.urlopen('https://www.kickstarter.com/discover/advanced?woe_id=0&sort=magic&seed=2462842&page='+str(num+1)).read()
    soup = BeautifulSoup(link, 'html.parser')

    proj_title = soup.find_all("h6", class_="project-title")

    # project descriptions
    title_str = HTMLParser.HTMLParser().unescape(str(proj_title)) # remove the &quot
    proj_title_link = re.findall('href="(/projects/.*?)"', title_str)
    proj_title_title = [s.string for s in proj_title]
    proj_byline = soup.find_all("p", class_="project-byline")
    proj_byline_title = [s.string for s in proj_byline]
    proj_blurb = soup.find_all("p", class_="project-blurb")
    proj_blurb_title = [s.string for s in proj_blurb]


    # project location
    proj_location = soup.find_all("div", class_="project-location")
    proj_location_str = HTMLParser.HTMLParser().unescape(str(proj_location)) # remove the &quot
    proj_location_shortname = re.findall('"displayable_name":"(.*?)"', proj_location_str)
    proj_location_country = re.findall('"country":"(.*?)"', proj_location_str)
    proj_location_state = re.findall('"state":"(.*?)"', proj_location_str)
    proj_location_type = re.findall('"type":"(.*?)"', proj_location_str)

    # project stat
    proj_stat = soup.find_all("ul", class_="project-stats")

    percent_funded_list=[]
    currency_type_list = []
    amt_pledged_list = []
    end_time_list = []

    for i_string in proj_stat:
        proj_stat_str = HTMLParser.HTMLParser().unescape(str(i_string))
        percent_funded = re.findall('<div class="project-stats-value">(.*?)%</div>', proj_stat_str)
        percent_funded_list.append(percent_funded[0])
        currency_type = re.findall('<span class="money (.*?) no-code">', proj_stat_str)
        currency_type_list.append(currency_type[0])

        amt_pledged = re.findall('no-code">\D+(.*?)</span>', proj_stat_str)
        amt_pledged_str = str(amt_pledged[0])
        amt_pledged_list.append(float(re.sub(',','',amt_pledged_str)))

        end_time = re.findall('data-end_time="(.*?)">', proj_stat_str)
        end_time_list.append(end_time[0])



# for debugging
#     print proj_location_str
#     print len(proj_title_title)
#     print proj_title_title
#     print len(proj_title_link)
#     print proj_location_shortname
#     print len(proj_location_shortname)
#     print len(proj_blurb_title)
#     print len(proj_location_country)
#     print len(proj_location_state)

#     print len(proj_location_type)
#     print len(percent_funded_list)
#     print len(currency_type_list)
#     print len(amt_pledged_list)

    # put them into data frame
    try:
        df = pd.DataFrame({'title':proj_title_title, 'url':proj_title_link,\
                           'by':proj_byline_title, 'blurb':proj_blurb_title,\
                           'location':proj_location_shortname, 'country': proj_location_country,\
                          'state': proj_location_state, 'type':proj_location_type, \
                          'percentage.funded':percent_funded_list,\
                          'currency': currency_type_list, 'amt.pledged':amt_pledged_list, 'end.time':end_time_list})
    except:
        print 'Page #'+str(num+1)+' has an exception.'
        break

    if num==0:
        df2 = df
    else:
        df2 = pd.concat([df2,df])


# reset index such that it is monotonic
df2 = df2.reset_index(drop=True)

# display dataframe
#df2.info()
#display(df2)
df2.to_csv('live.csv',encoding = 'UTF-8')
