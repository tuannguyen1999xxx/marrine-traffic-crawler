from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import os
import time
import datetime
import random
import json

FILE_NAME = 'save_results.json'
LINUX = False
CHROMEDRIVER_PATH_SV= '/usr/local/bin/chromedriver'
CHROMEDRIVER_PATH_LOCAL = 'C://Users//Admin//Downloads//chromedriver-win64//chromedriver.exe'

def initDriverProfile(profile, type=None):
    # Chromedriver linux path
    if LINUX:
        CHROMEDRIVER_PATH = CHROMEDRIVER_PATH_SV
    # Chromedriver windows path (download from https://chromedriver.chromium.org/downloads)
    else:
        CHROMEDRIVER_PATH = CHROMEDRIVER_PATH_LOCAL
    chrome_options = Options()

    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument(
    #     "user-data-dir=C://Users//Admin//AppData//Local//Google//Chrome//User Data//" + str(profile))  # Path to your chrome profile
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-gpu') if os.name == 'nt' else None  # Windows workaround
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-feature=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--ignore-certificate-error-spki-list")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControllered")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument('disable-infobars')

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              options=chrome_options
                              )
    return driver

def srcoll(driver):

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,1000);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,2500);")
    # time.sleep(2)
    # driver.execute_script("window.scrollTo(0,3000);")
    time.sleep(3)

def convert_time_to_utc0(string_time):

    # 2023-03-23 02:39 LT (UTC +8)
    string_time_first = ' '.join(string_time.split(' ')[0:2])
    off_set = int(string_time[-3:-1])
    format_time = "%Y-%m-%d %H:%M"
    dt = datetime.datetime.strptime(string_time_first, format_time) - datetime.timedelta(hours=off_set)

    return int(dt.timestamp())

def write_file(file_name, data):
    with open(file_name, 'a', encoding='utf-8') as w:
        w.write(json.dumps(data, ensure_ascii=False))
        w.write('\n')

def lastest_position_information(infor):
    infor_convert = {
        "objId": "",
        "eventTime": "",
        "longitude": 0.0,
        "latitude": 0.0,
        "name": "",
        "callSign": "",
        "eta": "",
        "destination": "",
        "imo": "",
        "dimA": 0,
        "dimB": 0,
        "dimC": 0,
        "dimD": 0,
        "draugth": 0.0,
        "rot": 0.0,
        "sog": 0.0,
        "cog": 0.0,
        "navstatus": 0,
        "trueHanding": 1,
        "mmsiMaster": "",
        "sourceId": "0",
        "sourcePort": 0,
        "destId": "0",
        "destPort": 0,
        "sourceMac": "",
        "destMac": "",
        "sourceIp": "",
        "destIp": "",
        "vesselTypeId": 0,
        "dtSource": 10000,
        "dtSourceParent": 50000
    }
    event_time = infor['Position Received']
    evt_time = str(convert_time_to_utc0(event_time))

    nav_status = infor['Navigational Status']
    if nav_status == "Active":
        nav_status = 1
    else:
        nav_status = 0

    try:
        lat_log = infor['Latitude/Longitude'].split('/')
        lat = float(lat_log[0].strip('°'))
        log = float(lat_log[1].strip('°'))
    except (ValueError, KeyError):
        lat = 0.0
        log = 0.0

    try:
        sog_cog = infor['Speed/Course'].split('/')
        sog = float(sog_cog[0].split(' ')[0])
        cog = float(sog_cog[1].split(' ')[0])
    except:
        sog = 0.0
        cog = 0.0

    imo = infor['IMO'].strip('-')
    name = infor['Name']
    objID = infor['MMSI']
    callsign = infor['Call Sign'].strip('-')

    try:
        dims = infor['Length Overall x Breadth Extreme'].split(' ')
        dimA = int(float(dims[0])/2)
        dimB = int(float(dims[0]) - dimA)
        dimC = int(float(dims[2])/2)
        dimD = int(float(dims[2]) - dimC)

        infor_convert['dimA'] = dimA
        infor_convert['dimB'] = dimB
        infor_convert['dimC'] = dimC
        infor_convert['dimD'] = dimD
    except ValueError:
        pass
    infor_convert['objId'] = objID
    infor_convert['eventTime'] = evt_time
    infor_convert['longitude'] = log
    infor_convert['latitude'] = lat

    infor_convert['name'] = name
    infor_convert['callSign'] = callsign
    infor_convert['imo'] = imo

    infor_convert['sog'] = sog
    infor_convert['cog'] = cog

    infor_convert['navstatus'] = nav_status
    # print(json.dumps(infor_convert, indent=4, ensure_ascii=False))

    return infor_convert

def vessel_information(raw_infor, mmsi):

    infor = {
        'imo':'',
        'vessel_name':'',
        'vessel_type_generic':'',
        'vessel_type_details':'',
        'navigational_status':'',
        'mmsi':'',
        'call_sign':'',
        'flag':'',
        'gross_tonnage':-1,
        'summer_dwt': -1,
        'length_overall': -1.0,
        'breadth_extreme': -1.0,
        'year_built': -1,
        'home_port': '',
        'image_original_url':''
    }
    try:
        imo = raw_infor['IMO'].strip('-')
    except KeyError:
        imo = ''
    try:
        name = raw_infor['Name'].strip('-')
    except KeyError:
        name = ''
    try:
        vtype_g = raw_infor['Vessel Type - Generic'].strip('-')
    except KeyError:
        vtype_g = ''
    try:
        vtype_d = raw_infor['Vessel Type - Detailed'].strip('-')
    except KeyError:
        vtype_d = ''
    try:
        callsign = raw_infor['Call Sign'].strip('-')
    except KeyError:
        callsign = ''
    try:
        flag = raw_infor['Flag'].strip('-')
    except KeyError:
        flag = ''
    infor['imo'] = imo
    infor['vessel_name'] = name
    infor['vessel_type_generic'] = vtype_g
    infor['vessel_type_details'] = vtype_d
    infor['mmsi'] = mmsi
    infor['call_sign'] = callsign
    infor['flag'] = flag
    
    try:
        gross_tonnage = raw_infor['Gross Tonnage'].strip('-')
        if gross_tonnage != '':
            gross_tonnage = int(gross_tonnage)
            infor['gross_tonnage'] = gross_tonnage
    except:
        pass
    try:
        summer_dwt = raw_infor['Summer DWT'].strip('-')
        if summer_dwt != '':
            num_summer_dwt = int(summer_dwt.split(' ')[0])
            infor['summer_dwt'] = num_summer_dwt
    except:
        pass
    try:
        len_breadth = raw_infor['Length Overall x Breadth Extreme'].strip('-')
        if len_breadth != '':
            len_z = float(len_breadth.split('x')[0].strip())
            breadth = float(len_breadth.split('x')[1].strip('m').strip())
            infor['length_overall'] = len_z
            infor['breadth_extreme'] = breadth
    except:
        infor['length_overall'] = 0.0
        infor['breadth_extreme'] = 0.0

    try:
        year = raw_infor['Year Built'].strip('-')
        if year != '':
            year = int(year)
            infor['year_built'] = year
    except:
        infor['year_built'] = -1
    infor['image_original_url'] = raw_infor['image_url']

    return infor