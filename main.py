from func import get_infor_by_mmsi
from utils import initDriverProfile, LINUX
from pyvirtualdisplay import Display

if __name__ == "__main__":
    if LINUX:
        display = Display(size=(1920, 1080))
        display.start()

    else:
        driver = initDriverProfile('tmp')
        mmsi = '431005138'
        get_infor_by_mmsi(driver, mmsi)
        driver.quit()

    if LINUX:
        display.stop()