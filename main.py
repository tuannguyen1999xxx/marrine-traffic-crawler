from func import get_infor_by_mmsi
from utils import initDriverProfile

if __name__ == "__main__":
    driver = initDriverProfile('tmp')

    mmsi = '431005138'
    get_infor_by_mmsi(driver, mmsi)
    driver.quit()