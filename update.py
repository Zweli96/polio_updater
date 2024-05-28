import pygsheets
import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from io import StringIO


# authorization
gc = pygsheets.authorize(service_file='./polio-420606-4ac871a4a05b.json')


def pull_direct():

    url = "http://206.225.84.201/r4h_polio2/polio_collection_summaries_export.php"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    headers["Accept-Language"] = "en-GB,en-US;q=0.9,en;q=0.8"
    headers["Cache-Control"] = "max-age=0"
    headers["Connection"] = "keep-alive"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Cookie"] = "username=riders; password=health; s1709095705=06c487d7ef00a0cbcbc06150e8c48db1"
    headers["Origin"] = "http://206.225.84.201"
    headers["Referer"] = "http://206.225.84.201/r4h_polio2/polio_collection_summaries_export.php"
    headers["Sec-GPC"] = "1"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"

    data = "type=csv&records=all&rndVal=0.7765982629967911"

    print("Downloading reported polio volumes")
    resp = requests.post(url, headers=headers, data=data)
    print("Download completed")

    print(resp.status_code)

    # To save to an absolute path.
    # using datetime module

    now = datetime.now()  # current date and time
    date_time_stamp = now.strftime("%Y%m%d%H%M%S")

    # with open(f'/home/routeopt-user/st_optimization/reported_volumes/sample_collection-{date_time_stamp}.csv', 'wb') as f:
    # with open(f'./downloaded/sample_collection-{date_time_stamp}.csv', 'wb') as f:
    #     f.write(resp.content)
    # return

    data = StringIO(resp.text)
    df = pd.read_csv(data)

    # open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('Polio Sample Tracker R4H_VILLAGE_REACH_USSD')

    # select the first sheet
    wks = sh[1]

    # update the first sheet with df, starting at cell B2.
    wks.set_dataframe(df, (1, 1))

    update_df = pd.DataFrame()
    update_df['Time Updated'] = [datetime.now()]
    updatesheet = sh[2]
    updatesheet.set_dataframe(update_df, (1, 1))


# # Create empty dataframe
# df = pd.DataFrame()

# # Create a column
# df['name'] = ['Zweli', 'Rich', 'Steve']

# # open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
# sh = gc.open('Polio Sample Tracker R4H_VILLAGE_REACH_USSD')

# # select the first sheet
# wks = sh[1]

# # update the first sheet with df, starting at cell B2.
# wks.set_dataframe(df, (1, 1))
pull_direct()
