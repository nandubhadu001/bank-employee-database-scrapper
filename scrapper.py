from  io import BytesIO
from time import time
from requests import get,post
from bs4 import BeautifulSoup
from pandas import read_html

import re

# used constants
urls = {
    "HOME_URL" : "https://sbi.co.in/web/corporate-governance/directory-and-gross-emoluments-of-state-bank-of-india-staff",
    "FEILDS_URL" : "https://sbi.co.in/web/corporate-governance/directory-and-gross-emoluments-of-state-bank-of-india-staff?p_p_id=salarydetails_INSTANCE_wUW5Jpkx9Xm1&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=findDesignation&p_p_cacheability=cacheLevelPage",
    "CAPTCH_URL" : "https://sbi.co.in/web/corporate-governance/directory-and-gross-emoluments-of-state-bank-of-india-staff?p_p_id=salarydetails_INSTANCE_wUW5Jpkx9Xm1&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=captcha&p_p_cacheability=cacheLevelPage",
    "DATA_URL" : "https://sbi.co.in/web/corporate-governance/directory-and-gross-emoluments-of-state-bank-of-india-staff?p_p_id=salarydetails_INSTANCE_wUW5Jpkx9Xm1&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_salarydetails_INSTANCE_wUW5Jpkx9Xm1_javax.portlet.action=searchRtiSalary",
    "PRIMARY_FIELD_URL" : "https://sbi.co.in/web/corporate-governance/directory-and-gross-emoluments-of-state-bank-of-india-staff?p_p_id=salarydetails_INSTANCE_wUW5Jpkx9Xm1&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=findDesignation&p_p_cacheability=cacheLevelPage"
}

headers = {
    "GENERAL_HEADERS" : {
        "Accept"                    : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding"           : "gzip, deflate",
        "Accept-Language"           : "en-US,en;q=0.9",
        "Cache-Control"             : "no-cache",
        "Pragma"                    : "no-cache",
        "Upgrade-Insecure-Requests" : "0",
        "User-Agent"                : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        },
    "XHR_HEADERS" : {
        "Accept"                    : "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding"           : "gzip, deflate, br",
        "Accept-Language"           : "en-US,en;q=0.9",
        "Cache-Control"             : "no-cache",
        "Connection"                : "keep-alive",
        "Content-Type"              : "application/x-www-form-urlencoded; charset=UTF-8",
        "Host"                      : "sbi.co.in",
        "Origin"                    : "https://sbi.co.in",
        "Pragma"                    : "no-cache",
        "Referer"                   : "https://sbi.co.in/web/corporate-governance/directory-and-gross-emoluments-of-state-bank-of-india-staff",
        "Sec-Fetch-Dest"            : "empty",
        "Sec-Fetch-Mode"            : "cors",
        "Sec-Fetch-Site"            : "same-origin",
        "User-Agent"                : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        "X-Requested-With"          : "XMLHttpRequest"
        },
    "IMAGE_HEADERS" : {
        "Accept"                    : "image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Encoding"           : "gzip, deflate, br",
        "Accept-Language"           : "en-US,en;q=0.9",
        "Cache-Control"             : "no-cache",
        "Connection"                : "keep-alive",
        "Host"                      : "sbi.co.in",
        "Pragma"                    : "no-cache",
        "Referer"                   : "https://sbi.co.in/web/corporate-governance/directory-and-gross-emoluments-of-state-bank-of-india-staff",
        "Sec-Fetch-Dest"            : "image",
        "Sec-Fetch-Mode"            : "no-cors",
        "Sec-Fetch-Site"            : "same-origin",
        "User-Agent"                : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        },
    "DATA_HEADERS" : {
        "Accept" :"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding" :"gzip, deflate, br",
        "Accept-Language" :"en-GB,en-US;q=0.9,en;q=0.8,my;q=0.7",
        "Cache-Control" :"max-age=0",
        "Connection" :"keep-alive",
        "Content-Type" :"application/x-www-form-urlencoded",
        "Host" :"sbi.co.in",
        "Origin" :"https://sbi.co.in",
        "Referer" :"https://sbi.co.in/web/corporate-governance/directory-and-gross-emoluments-of-state-bank-of-india-staff?p_p_id=salarydetails_INSTANCE_wUW5Jpkx9Xm1&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_salarydetails_INSTANCE_wUW5Jpkx9Xm1_javax.portlet.action=searchRtiSalary",
        "Sec-Fetch-Dest" :"document",
        "Sec-Fetch-Mode" :"navigate",
        "Sec-Fetch-Site" :"same-origin",
        "Sec-Fetch-User" :"?1",
        "Upgrade-Insecure-Requests" :"1",
        "User-Agent" :"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
        },
    "PRIMARY_FIELD_HEADERS" : {
        "Accept"           :"application/json, text/javascript, */*; q=0.01",
        "Accept-Encing"    :"gzip, deflate, br",
        "Accept-Language"  :"en-GB,en-US;q=0.9,en;q=0.8,my;q=0.7",
        "Connection"       :"keep-alive",
        "Content-Type"     :"application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie"           :"JSESSIONID=0000Q72oIFpV-c_5ZQvcDZNDMhV:1doiub4uc; COOKIE_SUPPORT=true; TS01f781cf=0137799b1923cbf55033f3d3e5afe875b874d8c1f68161dd08cae11b9403ab0ceed8452d96b282c1fc123f0e962bbd9c177292fbebde35bf75ef759571b9376eff8d6bf26db55b102ca348c270f238271712f491e399bcc65626057c858cc5afe3d73852ed; LFR_SESSION_STATE_104=1605190143491; TS69e3fdbd029=08b90ded0cab2800afeda11f27a5db3f6d4222ad9bb8a19a99c5937f4e214df9e0b3250a2bbe8cd2f4162e0df6c413b4; TSd934945e027=08b90ded0cab20005209b3aa627c7c4da4eb32383f07c4c3e4c6a173865263f0c5fd22833d7a562d087efa0dd411300009f00f37136be274d1849d4f6eece1066ef02467b18602fe2fb497dc549e65e59b581beae666ea69e621ac3a53a63ae2",
        "Host"             :"sbi.co.in",
        "Origin"           :"https://sbi.co.in",
        "Referer"          :"https://sbi.co.in/web/corporate-governance/directory-and-gross-emoluments-of-state-bank-of-india-staff",
        "Sec-Fetch-Dest"   :"empty",
        "Sec-Fetch-Mode"   :"cors",
        "Sec-Fetch-Site"   :"same-origin",
        "User-Agent"       :"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        "X-Requested-With" :"XMLHttpRequest"
        }
    }

class Scraper():
    def __init__(self):
        self.SESSION_COOKIES = None
        self.secondary_fields = []
        self.headers = headers
        self.urls = urls
        self.jstime = lambda : int(time()*1000)
        
    def get_primary_fields(self):

        index_page = get(self.urls["HOME_URL"],headers=self.headers["GENERAL_HEADERS"])

        parser = BeautifulSoup(index_page.content,features="lxml")
        
        self.SESSION_COOKIES = index_page.cookies

        #get all form elements from parserd html document
        form = parser.find_all("form")[2]
        
        #get all select elements from selected form element
        select = form.find_all("select")[0]
        
        #get all option elements from selected select element
        options = select.find_all("option")[1:]
        
        #get all field values from option elements
        self.primary_fields = list(map(lambda x:x.get("value"),options))

    def select_primary_field(self,primary_field):

        # data to be sent with post http request
        POST = {"_salarydetails_INSTANCE_wUW5Jpkx9Xm1_cadre":primary_field}
        
        # http post request(XHR)
        req_object = post(self.urls["FEILDS_URL"],headers=self.headers["XHR_HEADERS"],cookies=self.SESSION_COOKIES,data=POST)
        
        # update cookies
        self.SESSION_COOKIES.update(req_object.cookies)
        
        # create python object from request content
        response = eval(req_object.content)
        
        self.secondary_fields = list(map(lambda x:x["designation"],response))

    def get_Captcha(self):

        # required parameter
        parameter = {"t" : self.jstime}
        
        req_object = get(self.urls["CAPTCH_URL"],parameter,headers=self.headers["IMAGE_HEADERS"],cookies=self.SESSION_COOKIES)
        
        #update cookies associated with capcha
        self.SESSION_COOKIES.update(req_object.cookies)
        
        # here req_object.content returns 
        # b'\x89PNG\r\n\x1a\n\.......\x00\x00IEND\xaeB`\x82'
        # these are png file in raw bytes
        # we will return a file object here it is faster than second method
        
        return BytesIO(req_object.content)
        
        # second method
        # save
        with open("capcha.png","wb") as file:
            file.write(req_object.content)
            
        # return file object
        return open("capcha.png","rb")
        
    def get_data(self,PRIMARY_FILED,SECONDERY_FIELD,CAPTCHA_VALUE):
                
        # required form data
        POST = {
            "_salarydetails_INSTANCE_wUW5Jpkx9Xm1_formDate": self.jstime,
            "_salarydetails_INSTANCE_wUW5Jpkx9Xm1_cadre": PRIMARY_FILED,
            "_salarydetails_INSTANCE_wUW5Jpkx9Xm1_designation": SECONDERY_FIELD,
            "_salarydetails_INSTANCE_wUW5Jpkx9Xm1_captchaText": CAPTCHA_VALUE,
            "p_auth":""
        }
        
        req_object = post(self.urls["DATA_URL"],headers=self.headers["DATA_HEADERS"],cookies=self.SESSION_COOKIES,data=POST)

        self.SESSION_COOKIES.update(req_object.cookies)
        
        # if we got any data or failed
        if len(re.findall(b"Captcha Validation Failed",req_object.content))==1:
            # failed
            return False
        else:
            # pandas read_html function we parse html table and will return dataframe
            return read_html(req_object.content)
