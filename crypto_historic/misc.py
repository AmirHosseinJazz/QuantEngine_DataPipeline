from datetime import datetime, timedelta
import json
import requests
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from lxml import html


# FG Index
def fear_greed():
    """
    Fetches fear and greed index data from alternative.me API.

    Returns:
    - DataFrame: DataFrame containing fear and greed index data.
    """
    headers = {
        # Headers for the API request
    }

    json_data = {
        # JSON data for the API request
    }

    response = requests.post(
        "https://alternative.me/api/crypto/fear-and-greed-index/history",
        headers=headers,
        json=json_data,
    )

    d = json.loads(response.text)
    DF = pd.DataFrame(columns=["Date", "Value"])
    DF["Date"] = d["data"]["labels"]
    DF["Value"] = d["data"]["datasets"][0]["data"]
    DF["Date2"] = DF["Date"].apply(
        lambda x: (
            x.split(" ")[0] if int(x.split(" ")[0]) >= 10 else "0" + x.split(" ")[0]
        )
    )
    DF["Rest"] = DF["Date"].apply(lambda x: (x[2:]))
    DF["Again2"] = DF["Date2"] + " " + DF["Rest"] + " " + "01:00:00"
    DF["DateTime"] = DF["Again2"].apply(
        lambda x: datetime.strptime(x, "%d %b, %Y %H:%M:%S")
    )
    DF["Item"] = "FearGreed"
    DF = DF[["Item", "DateTime", "Value"]]
    return DF


# On Chain
def read_lookintobitcoin(indicator):
    """
    Fetches data from lookintobitcoin.com API for a specific indicator.

    Args:
    - indicator (str): Indicator name.

    Returns:
    - dict: JSON response from the API.
    """
    headers = {
        # Headers for the API request
    }

    json_data = {
        # JSON data for the API request
    }

    response = requests.post(
        "https://www.lookintobitcoin.com/django_plotly_dash/app/{}/_dash-update-component".format(
            indicator
        ),
        headers=headers,
        json=json_data,
    )

    try:
        f = json.loads(response.text)
    except:
        f = None
    return f


def read_lookintobitcoin2(indicator):
    """
    Fetches data from lookintobitcoin.com API for a specific indicator.

    Args:
    - indicator (str): Indicator name.

    Returns:
    - dict: JSON response from the API.
    """
    headers = {
        # Headers for the API request
    }

    json_data = {
        # JSON data for the API request
    }

    response = requests.post(
        "https://www.lookintobitcoin.com/django_plotly_dash/app/{}/_dash-update-component".format(
            indicator
        ),
        headers=headers,
        json=json_data,
    )
    try:
        f = json.loads(response.text)
    except:
        f = None
    return f


def read_lookintobitcoin3(indicator):
    """
    Fetches data from lookintobitcoin.com API for a specific indicator.

    Args:
    - indicator (str): Indicator name.

    Returns:
    - dict: JSON response from the API.
    """
    headers = {
        # Headers for the API request
    }

    json_data = {
        # JSON data for the API request
    }

    response = requests.post(
        "https://www.lookintobitcoin.com/django_plotly_dash/app/{}/_dash-update-component".format(
            indicator
        ),
        headers=headers,
        json=json_data,
    )
    try:
        f = json.loads(response.text)
    except:
        f = None
    return f


def onchain_indicators():
    """
    Fetches on-chain indicators data from lookintobitcoin.com API.

    Returns:
    - DataFrame: DataFrame containing on-chain indicators data.
    """
    Items = {
        # Dictionary of indicators and their corresponding API endpoints
    }
    All = []
    for key, value in tqdm(Items.items()):
        DF = pd.DataFrame()
        data = read_lookintobitcoin(value[0])
        if data is None:
            data = read_lookintobitcoin2(value[0])
            if data is None:
                data = read_lookintobitcoin3(value[0])
                if data is None:
                    print(value[0])
                    continue
        DF["TimeStamp"] = data["response"]["chart"]["figure"]["data"][value[1]]["x"][
            : len(data["response"]["chart"]["figure"]["data"][value[1]]["y"])
        ]
        DF["Value"] = data["response"]["chart"]["figure"]["data"][value[1]]["y"]
        DF["Item"] = key
        DF = DF.dropna(subset=["Value"])
        All.append(DF)
    all_df = pd.concat([x for x in All], ignore_index=True)
    all_df["TimeStamp"] = all_df["TimeStamp"].apply(lambda x: str(x).split("T")[0])
    all_df.columns = ["DateTime", "Value", "Item"]
    all_df = all_df[["Item", "DateTime", "Value"]]
    return all_df


## Money Index
def money_index_indicators(item):
    """
    Fetches money index data from WSJ API.

    Args:
    - item (str): Money index item.

    Returns:
    - dict: JSON response from the API.
    """
    headers = {
        # Headers for the API request
    }

    response = requests.get(
        item,
        headers=headers,
    )

    return json.loads(response.text)


def money_index_data():
    """
    Fetches money index data from WSJ API.

    Returns:
    - DataFrame: DataFrame containing money index data.
    """
    Items = {
        # Dictionary of money index items and their corresponding API endpoints
    }
    All = []
    for key, value in Items.items():
        try:
            data = money_index_indicators(value)
            DF = pd.DataFrame()
            DF["Timestamp"] = data["TimeInfo"]["Ticks"]
            DF["Value"] = data["Series"][0]["DataPoints"]
            DF["Value"] = DF["Value"].apply(lambda x: x[0])
            DF["Item"] = key
            DF["DateTime"] = pd.to_datetime(DF["Timestamp"], unit="ms")
            DF.drop(["Timestamp"], axis=1, inplace=True)
            DF = DF[["Item", "DateTime", "Value"]]
            All.append(DF)
        except Exception as E:
            print(E)
            continue
    all_df = pd.concat([x for x in All], ignore_index=True)
    return all_df


## Events


def all_crypto_calendar(
    startDate="2007-01-01",
    endDate=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
):
    """
    Fetches crypto events data from cryptocraft.com.
    Input:
    - startDate (str): Start date for the events.
    - endDate (str): End date for the events.
    Output:
    - DataFrame: DataFrame containing crypto events data.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    )
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    driver.maximize_window()
    events = []
    for specific_date in tqdm(
        list(pd.date_range(start=startDate, end=endDate, freq="D"))[:]
    ):
        driver.get(
            "https://www.cryptocraft.com/calendar?day="
            + specific_date.strftime("%b%-d.%Y").lower()
        )
        time_temp = ""
        for item in driver.find_elements(By.XPATH, "//tr[@data-event-id]"):
            calendar_event = {}
            calendar_event["date"] = specific_date.strftime("%Y-%m-%d")
            calendar_event["event_id"] = item.get_attribute("data-event-id")
            try:
                t1 = item.find_element(
                    By.XPATH, "./td[@class='calendar__cell calendar__time']"
                ).text
                if t1 == "":
                    raise Exception
                calendar_event["time"] = t1
                time_temp = t1
            except:
                calendar_event["time"] = time_temp

            try:
                calendar_event["Impact"] = item.find_element(
                    By.XPATH, "./td[@class='calendar__cell calendar__impact']/span"
                ).get_attribute("title")
            except:
                calendar_event["Impact"] = ""

            try:
                calendar_event["title"] = item.find_element(
                    By.XPATH, ".//span[@class='calendar__event-title']"
                ).text
            except:
                calendar_event["title"] = ""

            try:
                calendar_event["details"] = item.find_element(
                    By.XPATH, "./td[@class='calendar__cell calendar__detail']/a"
                ).get_attribute("title")
            except:
                calendar_event["details"] = "No Details"

            try:
                calendar_event["actual"] = item.find_element(
                    By.XPATH, "./td[@class='calendar__cell calendar__actual']"
                ).text
            except:
                calendar_event["actual"] = ""

            try:
                calendar_event["forecast"] = item.find_element(
                    By.XPATH, "./td[@class='calendar__cell calendar__forecast']"
                ).text
            except:
                calendar_event["forecast"] = ""

            try:
                calendar_event["previous"] = item.find_element(
                    By.XPATH, "./td[@class='calendar__cell calendar__previous']"
                ).text
            except:
                calendar_event["previous"] = ""

            events.append(calendar_event)
        time.sleep(1.5)
    driver.quit()
    df = pd.DataFrame(events)
    print("Getting the crypto events with # of events:", df.shape[0])
    return df


def update_crypto_calendar():
    """ "
    calling the event calendar function to update the crypto events for the past week to the next 30 days
    """
    recent = all_crypto_calendar(
        startDate=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        endDate=(datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"),
    )
    print("Updating the crypto events with # of events:", recent.shape[0])
    return recent


########### FIX IT ###########
# def save_news(df):
#     with open(utility.parent_dir() + "/config.json") as json_data_file:
#         try:
#             cred = json.load(json_data_file)["postgres"]
#             conn = db.connect(cred)
#         except Exception as E:
#             print(E)
#             print("Error while Connecting to DB")
#         try:
#             cur = conn.cursor()
#             query = """
#             INSERT INTO news.cryptofactory_news(
#             title, href,datetime)
#             VALUES ( %s, %s, %s)
#             ON CONFLICT (datetime) DO NOTHING;

#             """
#             df = df.drop_duplicates()
#             tuples = [tuple(x) for x in df.to_numpy()]
#             cur.executemany(query, tuples)
#             conn.commit()
#             return 0
#         except Exception as E:
#             print(E)
#             traceback.print_exc()
#             print("Error while saving model")
#             conn.rollback()
#             cur.close()
#             return 1


# def save_news_details(df):
#     with open(utility.parent_dir() + "/config.json") as json_data_file:
#         try:
#             cred = json.load(json_data_file)["postgres"]
#             conn = db.connect(cred)
#         except Exception as E:
#             print(E)
#             print("Error while Connecting to DB")
#         try:
#             cur = conn.cursor()
#             query = """
#             INSERT INTO news.cryptofactory_news_detailed(
#             datetime, text)
#             VALUES (%s, %s)
#             ON CONFLICT (datetime) DO NOTHING;

#             """
#             df = df.drop_duplicates()
#             tuples = [tuple(x) for x in df.to_numpy()]
#             cur.executemany(query, tuples)
#             conn.commit()
#             return 0
#         except Exception as E:
#             print(E)
#             traceback.print_exc()
#             conn.rollback()
#             cur.close()
#             return 1

# # getting request for news
# def get_news(more=0):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
#         "Accept": "application/json, text/plain, */*",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Referer": "https://www.cryptocraft.com/news",
#         "Content-Type": "multipart/form-data; boundary=---------------------------7889954334036840942638034810",
#         "Origin": "https://www.cryptocraft.com",
#         "Connection": "keep-alive",
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin",
#     }

#     params = {
#         "more": "10",
#     }

#     data = '-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="_csrf"\r\n\r\n23ef8e470a3a43e5fde98a7cfa47a98b\r\n-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="securitytoken"\r\n\r\nguest\r\n-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="do"\r\n\r\nsaveoptions\r\n-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="setdefault"\r\n\r\nno\r\n-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="ignoreinput"\r\n\r\nno\r\n-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][idSuffix]"\r\n\r\n\r\n-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][_flexForm_]"\r\n\r\nflexForm\r\n-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][modelData]"\r\n\r\neyJwYV9sYXlvdXRfaWQiOiJuZXdzIiwicGFfY29tcG9uZW50X2lkIjoiTmV3c0xlZnRPbmUiLCJwYV9jb250cm9scyI6Im5ld3N8TmV3c0xlZnRPbmUiLCJwYV9pbmplY3RyZXZlcnNlIjpmYWxzZSwicGFfaGFyZGluamVjdGlvbiI6ZmFsc2UsInBhX2luamVjdGF0IjpmYWxzZX0=\r\n-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][news]"\r\n\r\nall\r\n-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][format]"\r\n\r\nheadline\r\n-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][items]"\r\n\r\n15\r\n-----------------------------7889954334036840942638034810\r\nContent-Disposition: form-data; name="flex[News_newsLeft1][sort]"\r\n\r\nlatest\r\n-----------------------------7889954334036840942638034810--\r\n'

#     response = requests.post(
#         "https://www.cryptocraft.com/flex.php",
#         params=params,
#         headers=headers,
#         data=data,
#     )
#     tree = html.fromstring(response.content)
#     all_items = []
#     for i in tree.xpath(".//li[@data-timestamp]"):
#         items = {}
#         items["title"] = (
#             i.xpath('.//span[@class="flexposts__title title"]//a')[0]
#             .text.replace("\n", "")
#             .strip()
#             .replace("\t", "")
#         )
#         items["href"] = i.xpath('.//span[@class="flexposts__title title"]//a')[0].get(
#             "href"
#         )
#         items["datetime"] = i.get("data-timestamp")
#         all_items.append(items)
#     DF = pd.DataFrame(all_items)
#     return DF

# # details of news
# def get_news_details():
#     unread = db.fetch_todf_query(
#         "SELECT datetime, title, href FROM news.cryptofactory_news where datetime not in (Select datetime from news.cryptofactory_news_detailed);"
#     )
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     all_items = []
#     for index, row in unread.iterrows():
#         tweet = False
#         item = {}
#         headers = {
#             "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
#             "Accept": "application/json, text/plain, */*",
#             "Accept-Language": "en-US,en;q=0.5",
#             "Referer": "https://www.cryptocraft.com/news",
#             "Content-Type": "multipart/form-data; boundary=---------------------------7889954334036840942638034810",
#             "Origin": "https://www.cryptocraft.com",
#             "Connection": "keep-alive",
#             "Sec-Fetch-Dest": "empty",
#             "Sec-Fetch-Mode": "cors",
#             "Sec-Fetch-Site": "same-origin",
#         }
#         response = requests.get(
#             "https://cryptocraft.com/" + row["href"], headers=headers
#         )
#         tree = html.fromstring(response.content)
#         try:
#             news = (
#                 tree.xpath('.//p[@class="news__copy"]')[0]
#                 .text.strip()
#                 .replace("\n", "")
#                 .replace("\t", "")
#             )
#             item["text"] = news
#         except:
#             tweet = True
#         try:
#             if tweet:
#                 driver.get("https://www.cryptocraft.com/" + row["href"])
#                 news = []
#                 for _iframe in driver.find_elements(By.XPATH, ".//iframe"):
#                     driver.switch_to.frame(_iframe)
#                     try:
#                         news.append(
#                             driver.find_element(
#                                 By.XPATH, ".//div[@data-testid]//span"
#                             ).text
#                         )
#                     except:
#                         pass
#                     driver.switch_to.default_content()
#                 item["datetime"] = row["datetime"]
#                 item["text"] = " ".join(news)
#                 all_items.append(item)
#         except:
#             item["text"] = ""
#         item["datetime"] = row["datetime"]
#         all_items.append(item)

#     DF = pd.DataFrame(all_items)
#     return DF

# # last 7 days news
# def update_latest_news():
#     save_news(get_news())
#     save_news_details(get_news_details())
#     print("update latest news successfully")
