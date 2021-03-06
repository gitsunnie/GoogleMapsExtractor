import time
import datetime
import csv
import re

# import schedule

# from bs4 import BeautifulSoup
# import urllib.request as req

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# map_url = 'https://www.google.com/maps/?authuser=1'
"""Parameter 解説
authuser
: そのブラウザに入っている Google アカウントの番号
今回は Trial Sunnie のアカウントを使いたかったので 1 番 (Sunnie は 0 番)

"""


def job_flow():
    # Chromeを起動
    driver = start_chrome()

    # Googleにログイン
    login_google(driver)

    # Google Map でいろいろサーチ
    search_map(driver)


def start_chrome():
    opt = webdriver.ChromeOptions()
    # opt.binary_location = chrome_binary_path
    opt.binary_location = '/app/.apt/usr/bin/google-chrome'
    driver_path = '/app/.chromedriver/bin/chromedriver'
    opt.add_argument('--headless')
    # driver = webdriver.Chrome('./chromedriver-73.exe', options=opt)
    # driver = webdriver.Chrome('./chromedriver-73.exe')
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=opt)

    # Google ログイン画面
    login_url = 'https://www.google.com/accounts?hl=ja-JP'
    driver.get(login_url)

    return driver


def login_google(driver):
    # Google Account 情報
    login_id = 'trialsunnie@gmail.com'
    login_pw = 'trialaccount'

    # 最大待機時間 (sec)
    wait_time = 10

    # ID の入力
    login_id_xpath = '//*[@id="identifierNext"] | //*[@id="Email"]'
    # xpathの要素が見つかるまで待機します。
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, login_id_xpath)))
    # driver.find_element_by_name("identifier").send_keys(login_id)
    driver.find_element_by_name('Email').send_keys(login_id)
    # driver.find_element_by_xpath(login_id_xpath).click()
    next_button_xpath = '//*[@id="next"]'
    driver.find_element_by_xpath(next_button_xpath).click()

    # パスワードを入力
    login_pw_xpath = '//*[@id="passwordNext"] | //*[@id="Passwd"]'
    # xpathの要素が見つかるまで待機します。
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, login_pw_xpath)))
    # driver.find_element_by_name("password").send_keys(login_pw)
    driver.find_element_by_name("Passwd").send_keys(login_pw)
    time.sleep(1)  # クリックされずに処理が終わるのを防ぐために追加。
    driver.find_element_by_xpath(login_pw_xpath).click()


def search_map(driver):
    map_url = 'https://www.google.com/maps/?hl=ja'
    # map_url = 'https://www.google.com/maps/@33.5863372,130.369886,14.23z?hl=ja'

    driver.execute_script("window.open()")  # make new tab
    driver.switch_to.window(driver.window_handles[1])  # switch new tab
    driver.get(map_url)

    """
    time.sleep(5)
    # driver.find_element_by_id('#widget-mylocation')
    driver.find_element_by_xpath('//*[@id="widget-mylocation"]').click()
    """

    try:
        # 現在地を探索するボタンが出てくるまで待機
        current_location_xpath = '//*[@id="widget-mylocation"]'
        wait_time = 30
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, current_location_xpath)))

        # driver.find_element_by_id('#widget-mylocation')
        driver.find_element_by_xpath('//*[@id="widget-mylocation"]').click()

        time.sleep(5)

        print(driver.current_url)
        location_url = driver.current_url

        # 現在位置 (座標を探索)
        # a = re.search('[.+]' + '@' + '(.+)' + ', ' + '(.+)' + '[.+]', str(location_url))'
        pattern = '@' + '([0-9.]*)' + ',' + '([0-9.]*)'
        a = re.search(pattern, location_url)
        # print('latitude: ' + a.group(1))
        # print('longitude: ' + a.group(2))
        latitude = a.group(1)
        longitude = a.group(2)
    except:
        latitude = 'error'
        longitude = 'error'
        location_url = 'error'

    # 現在時間を取得
    dt_now = datetime.datetime.now()
    present_year = dt_now.year
    present_month = dt_now.month
    present_day = dt_now.day
    present_time = dt_now.time()

    # csv に書き込み
    with open('MapsLocationHistory.csv', mode='a') as f:
        writer = csv.writer(f)
        writing_list = [present_year, present_month, present_day, present_time, latitude, longitude, location_url]
        writer.writerow(writing_list)

    driver.quit()


if __name__ == '__main__':
    """
    schedule.every(1).minutes.do(job_flow)

    while True:
        schedule.run_pending()
        time.sleep(1)
    """

    job_flow()
    time.sleep(300)  # 5分待つ
    # time.sleep(30)
    job_flow()





