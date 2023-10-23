# This project use Selenium to extract information of a vessel from [Marrine Traffic](marrinetraffic.com)

## Install

- Download ChromeDriver from (https://chromedriver.chromium.org/downloads)
- Change path of CHROMEDRIVER_PATH to your path 
- Requirement ```pip install selenium==4.2.0 ```
- Python >=3.8

## Run
- ``` python main.py ```

## Sample result

```json
{
  "lastest_position": {
    "objId": "431005138",
    "eventTime": "1698030540",
    "longitude": 0,
    "latitude": 0,
    "name": "MIKASA",
    "callSign": "JD3633",
    "eta": "",
    "destination": "",
    "imo": "9701580",
    "dimA": 32,
    "dimB": 32,
    "dimC": 5,
    "dimD": 5,
    "draugth": 0,
    "rot": 0,
    "sog": 0,
    "cog": 0,
    "navstatus": 1,
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
  },
  "vessel_information": {
    "imo": "9701580",
    "vessel_name": "MIKASA",
    "vessel_type_generic": "Tanker",
    "vessel_type_details": "Oil Products Tanker",
    "navigational_status": "",
    "mmsi": "431005138",
    "call_sign": "JD3633",
    "flag": "Japan [JP]",
    "gross_tonnage": 499,
    "summer_dwt": 1142,
    "length_overall": 64.5,
    "breadth_extreme": 10,
    "year_built": 2014,
    "home_port": "",
    "image_original_url": "https://photos.marinetraffic.com/ais/showphoto.aspx?photoid=3079660"
  }
}
```