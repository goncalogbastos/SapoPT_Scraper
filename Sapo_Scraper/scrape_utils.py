# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import re

#Adapted from https://stackoverflow.com/questions/65469973/write-dictionaries-with-different-keys-to-csv-file/65470172
class CsvDictWriter:
    def __init__(self):
        self.dicts = []
        self.fields = set()

    def add_dict(self, obj: dict):
        self.dicts.append(obj)
        self.fields.update(obj.keys())

    def write(self, file_name: str):
        with open(file_name, 'w+',encoding="utf-8",newline='') as fp:
            dw = csv.DictWriter(fp, self.fields, restval='')
            dw.writeheader()
            for obj in self.dicts:
                dw.writerow(obj)

class utils():

    def __init__(self):

        self.driverPath = r"C:\Users\Goncalo\Documents\#IMS\PDS\#PROJETO\SCRAPING\chromedriver.exe"
        #self.driverPath = r"C:\edsa\pds\v0\phantomjs.exe"

        chrome_options = Options()  
        
        chrome_options.add_argument("--headless")

        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')

        self.browser = webdriver.Chrome(self.driverPath,chrome_options=chrome_options)
        #self.browser = webdriver.PhantomJS(self.driverPath)


        self.browser.set_window_size(1920, 1080)

    def wait_for_element(self,elementIdentifier,browser,by=By.ID):
        """
        elementIdentifier is a class or id name

        browser is the webdriver object

        by defaults to By.ID, with By.Classname being commonly used. See https://selenium-python.readthedocs.io/locating-elements.html

        """
        timeout = 3
        try:
            element_present = EC.presence_of_element_located((by, elementIdentifier))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            pass
        finally:
            pass

    def get_num_listings(self, url_concelho):

        self.browser.get(url_concelho)

        self.wait_for_element("divSearchPageResults", self.browser)

        #Obtém titulo no formato: "Casas para Venda, 14928 Apartamentos em Lisboa"
        headerTitle = self.browser.find_element_by_class_name("searchHeaderTitle").find_element_by_tag_name("a").get_attribute("title")

        #Isola o número
        num_listings = int(headerTitle.split(' ')[0])
        
        return num_listings
    
    def get_listings(self, url_concelho,page_num):

        self.browser.get(url_concelho+"?pn="+str(page_num))

        self.wait_for_element("divSearchPageResults", self.browser)

        try:

            results_container = self.browser.find_element_by_id("divSearchPageResults")
        
        except NoSuchElementException:

            return None

        results = results_container.find_elements_by_class_name("searchResultProperty")

        results_list = [{} for r in results]

        for c,r in enumerate(results):

            try:
                results_list[c]['link'] = r.find_element_by_id("MC_PropertyInList_repProperties_hlRealestateDetail_"+str(c)).get_attribute("href")
            except:
                results_list[c]['link'] = ''

            try:
                results_list[c]['title'] = r.find_element_by_class_name("searchPropertyTitle").find_element_by_tag_name("span").get_attribute("innerText")
            except:
                results_list[c]['title'] = ''

            try:
                results_list[c]['price'] = r.find_element_by_class_name("searchPropertyPrice").find_element_by_tag_name("span").get_attribute("innerText")
            except:
                results_list[c]['price'] = ''

            try:
                results_list[c]['estate_agent'] = r.find_element_by_id("MC_PropertyInList_repProperties_aClientLink_"+str(c)).get_attribute("title").split('Veja todos os imóveis do anunciante ')[1]
            except:
                results_list[c]['estate_agent'] = ''

            try:

                container = r.find_element_by_class_name("searchPropertyInfo").find_elements_by_tag_name("div")
            
            except:

                container = []

            for div in container:

                try:

                    results_list[c][div.find_elements_by_tag_name("p")[0].get_attribute("innerText")] = div.find_elements_by_tag_name("p")[1].get_attribute("innerText")
                
                except:

                    pass

        return results_list

    def process_and_save_result(self, listing_results,concelho,page_num):

        tochange_m2 = ['área útil', 'área bruta', 'área terreno']

        for c,lr in enumerate(listing_results):

            lr = dict((k.lower(), v) for k, v in lr.items()) # {'TESTE':'AbCd1'} -> {'teste':'AbCd1'}

            listing_results[c] = lr

            for tc_t in tochange_m2:#change meters squared to nothing
                try:
                    lr[tc_t] = ''.join([n for n in lr[tc_t] if n.isdigit()])
                    lr[tc_t] = lr[tc_t].replace("²","")
                except:
                    pass

        concelho = dict((k.lower(), v) for k, v in concelho.items())

        from_concelho = dict()

        from_concelho['municipality_id'] = concelho['id']
        from_concelho['municipality'] = concelho['name']
        from_concelho['municipality_url'] = concelho['url']
        from_concelho['district'] = concelho['group']
        from_concelho['district_id'] = concelho['groupid']

        
        csv_file = './scraped_data/D'+str(from_concelho['district_id']) + '_C' + str(from_concelho['municipality_id']) + '_P' + str(page_num) + '.csv' #filename

        for c,lr in enumerate(listing_results): #build final dataset
            lr.update(from_concelho)

            lr['page_num'] = page_num
            try:
                lr['price'] = round(float(lr['price'].replace("€","").replace('\xa0','')),2)
            except:
                lr['price'] = ''

            try:
                lr['type'] = re.findall(r"T\d\S*",lr['title'])[0].replace(",","")
            except:
                lr['type'] = ''
            del lr['title']

            try:
                lr['condition'] = lr['estado']
                del lr['estado']
            except:
                pass

            try:
                lr['construction_area'] = lr['área terreno']
                del lr['área terreno']
            except:
                pass

            try:
                lr['net_area'] = lr['área útil']
                del lr['área útil']
            except:
                pass

            try:
                lr['floor_area'] = lr['área bruta']
                del lr['área bruta']
            except:
                pass

        cdw = CsvDictWriter()

        for lr in listing_results:
            cdw.add_dict(lr)

        cdw.write(csv_file)