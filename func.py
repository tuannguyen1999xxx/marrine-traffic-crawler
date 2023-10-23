from utils import *

def get_infor_a_ship(driver):
    '''
    driver: selenium driver
    return: information of a ship
    '''
    time.sleep(5)
    srcoll(driver)
    time.sleep(1)
    ### 4 lines of code to pass cookies 

    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[1]'))).click()
    # time.sleep(1)
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[3]/div[2]/button'))).click()
    
    try:
        WebDriverWait(driver,10).until(EC.visibility_of_element_located(
            (By.XPATH,'//*[@id="app"]/div/header/div/div/div[6]/div/div[2]')))

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located
                                        ((By.XPATH, '//*[@id="vesselDetails_latestPositionSection"]')))
    except TimeoutException:
        driver.refresh()
        
    full_infor = {}
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located
                                    ((By.XPATH, '//*[@id="vesselDetails_latestPositionSection"]')))

    lastest_pos_el = driver.find_element(By.XPATH, '//*[@id="vesselDetails_latestPositionSection"]')
    texts = lastest_pos_el.text
    list_texts = texts.split('\n')

    for i, text in enumerate(list_texts):
        if ': ' in text:
            key_val = text.split(': ')
            key = key_val[0]
            val = ' '.join(key_val[1:])
            if "Vessel's Local Time" in key:
                val = list_texts[i+1]
            full_infor[key] = val
    # driver.execute_script("window.scrollTo(0,1200);")

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located
                                        ((By.XPATH, '//*[@id="vesselDetails_vesselInfoSection"]')))
    vessels_infor_el = driver.find_element(By.XPATH,'//*[@id="vesselDetails_vesselInfoSection"]')
    list_vessels_infor_text = vessels_infor_el.text.split('\n')

    for text in list_vessels_infor_text:
        if ': ' in text:
            key_val = text.split(': ')
            key = key_val[0]
            val = ' '.join(key_val[1:])
            full_infor[key] = val

    # Get url image of the vessel if exist
    try:
        img_url = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="vesselDetails_photosSection"]/div[2]/div/div/div/div[1]/div/div/div[1]/a/div'))).value_of_css_property("background-image").split('"')[1]
    except:
        img_url = ''
    full_infor['image_url'] = img_url

    return full_infor

def extract_infor(driver, mmsi: str):
    raw_information = get_infor_a_ship(driver)
    lastest_pos = lastest_position_information(raw_information)
    vessel_info = vessel_information(raw_information, mmsi)

    results = {'lastest_position':lastest_pos, 'vessel_information': vessel_info}
    # Write result to a file
    write_file(FILE_NAME, results)

def get_infor_by_mmsi(driver, mmsi: str):
    
    '''
    driver: selenium driver
    mmsi: MMSI (Maritime Mobile Service Identities)
    return: information of a ship    
    '''
    url_ship = f'https://www.marinetraffic.com/en/ais/details/ships/mmsi:{mmsi}'
    driver.get(url_ship)

    # Check page 
    if "404 - Page Not Found" in driver.title:
        return False
    
    try:
    # Check if one MMSI have many links
        time.sleep(3)
        WebDriverWait(driver,10).until(EC.visibility_of_element_located(
            (By.ID,"reporting_ag_grid")))
        time.sleep(1)

        table = driver.find_element(By.XPATH,'//*[@id="reporting_ag_grid"]/div/div[2]/div[2]/div/div[1]/div[2]/div[3]')
        left_table = table.find_element(By.XPATH,'//*[@id="reporting_ag_grid"]/div/div[2]/div[2]/div/div[1]/div[2]/div[3]/div[1]/div/div[1]')
        print("Have many vessels/MMSI")
        vessel_links = left_table.find_elements(By.CLASS_NAME,'ag-cell-content-link')

        links = []
        for vessel_link in vessel_links:
            # print(vessel_link)
            link = vessel_link.get_attribute('href')
            links.append(link)
        # print(len(links))
        # time.sleep(1)
        for link in links:
            driver.get(link)
            extract_infor(driver, mmsi=mmsi)

    except TimeoutException:
        print("Have 1 vessel/MMSI")
        extract_infor(driver, mmsi=mmsi)

    time.sleep(2)
    
    
    