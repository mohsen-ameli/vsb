import requests, html
from bs4 import BeautifulSoup

import requests

url = "https://schedulebuilder.yorku.ca/vsb/getclassdata.jsp"
params = {
    "term": "2023102119",
    "course_0_0": "LE-EECS-2030-3.00-EN-",
    "course_1_0": "SC-MATH-2030-3.00-EN-",
    "course_2_0": "SC-MATH-2310-3.00-EN-",
    "course_3_0": "SC-CHEM-1001-3.00-EN-",
    "course_4_0": "AP-ECON-1000-3.00-EN-",
    "course_5_0": "AP-ECON-1010-3.00-EN-",
    "course_6_0": "LE-EECS-2021-4.00-EN-",
    "course_7_0": "SC-MATH-1090-3.00-EN-",
    "course_8_0": "LE-EECS-2001-3.00-EN-",
    "course_9_0": "LE-EECS-2031-3.00-EN-",
    "course_10_0": "LE-EECS-2101-3.00-EN-",
    "t": "285",
    "e": "33",
    "nouser": "1",
    "_": "1688957135957"
}

headers = {
    "accept": "application/xml, text/xml, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
}

cookies = {
    "1P_JAR": "2023-07-09-22",
    "pyauth": "qm27p/opexlYbZ7CPbTHejfBBOkDrlekVUhG4l1PwWL8hAj%2BDdG/wicx9FhwMgbHDkDqw%2Bsyi8%2BHOVBZOWUH4VI2lOb69tTCEX3YN5FWWyCdugmTqVRyyOLZRZAc6JuWPZX/ZFe1nF/i6Wim6GBH7Q%3D%3D",
    "mayaauth": "CJWOR04/Rx3XVXRVoawDg2CW%2Bcq/%2BQuaCuSGcVmlPJumqI1H%2Bivv48Tpi/9/K0/wdw2vo6/sfRGCT5x4YeDnY0HMXdw%2BcZqqBLdpL/Ir93VapurIydFXgiGidb3lbxYyRSofiiqawMMyQT1/GRCBVg%3D%3D",
    "JSESSIONID": "1914512C8F4D09D69338725404D5CCDE"
}

response = requests.get(url, params=params, headers=headers, cookies=cookies)

print(response.text)  # Use the response as desired
