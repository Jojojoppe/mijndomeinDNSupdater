from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time

TIMEOUT = 10

class MijnDomein:
    def __init__(self, username: str, password: str):
        self.browser = webdriver.Firefox()
        self.username = username
        self.password = password
        self.domainNameInfo = {}

    def __del__(self):
        self.browser.close()

    def login(self) -> None:
        self.browser.get('https://auth.mijndomein.nl/login')
        assert 'Mijndomein' in self.browser.title
        self.browser.find_element(By.NAME, '_username').send_keys(self.username)
        self.browser.find_element(By.NAME, '_password').send_keys(self.password)
        self.browser.find_element(By.XPATH,'//form[@action=\'/login_check\']').submit()
        WebDriverWait(self.browser, TIMEOUT).until(EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonAccept')))
        self.browser.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonAccept').click()   

    def logout(self) -> None:
        self.browser.get('https://www.mijndomein.nl/account/product')
        WebDriverWait(self.browser, TIMEOUT).until(EC.presence_of_element_located((By.LINK_TEXT, 'Uitloggen')))
        btn = self.browser.find_element(By.LINK_TEXT, 'Uitloggen')
        btn.click()

    def getDomainNameInfo(self) -> list[str]:
        self.browser.get('https://www.mijndomein.nl/account/product')
        WebDriverWait(self.browser, TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='ProductOverviewBlockTitle']")))
        productNames = self.browser.find_elements(By.CSS_SELECTOR, "div[class*='ProductOverviewBlockTitle']")
        productAccordions = self.browser.find_elements(By.CSS_SELECTOR, "span[class*='AccordionIconWrapper']")
        self.domainNameInfo = {}
        names = []

        for i in range(len(productAccordions)):
            name = productNames[i*2].text
            print("--->", name)
            names.append(name)

        for name in names:
            # Get package ID
            self.browser.get(f'https://www.mijndomein.nl/account/product/dmp/{name}')
            WebDriverWait(self.browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//span[.='DNS instellen']")))
            btn = self.browser.find_element(By.XPATH, "//span[.='DNS instellen']")
            btn.click()
            time.sleep(2) # TODO add a wait statement
            url = self.browser.current_url
            self.domainNameInfo[name] = {
                'name': name,
                'expand': productAccordions[i],
                'dns_url': url,
                'dns': [],
            }

    def getDNSRecords(self, domain: str) -> None:
        assert domain in self.domainNameInfo
        self.browser.get(self.domainNameInfo[domain]['dns_url'])
        time.sleep(4) # TODO add a wait statement
        rows = self.browser.find_elements(By.CSS_SELECTOR, "div[class*='dnseditor_row']")
        for row in rows:
            try:
                rowid = row.get_attribute('id')
                if not rowid.endswith("ROW"):
                    continue
                dns_type = Select(row.find_element(By.CSS_SELECTOR, "select[id*='_type']"))
                dns_type_txt = dns_type.first_selected_option.text
                dns_name = row.find_element(By.CSS_SELECTOR, "input[id*='_name']")
                dns_name_txt = dns_name.get_attribute('value')
                if dns_type_txt in ['A', 'AAAA', 'CNAME', 'MX']:
                    dns_content = row.find_element(By.CSS_SELECTOR, "input[id*='_content']")
                    dns_content_txt = dns_content.get_attribute('value')
                elif dns_type_txt in ['TXT']:
                    dns_content = row.find_element(By.CSS_SELECTOR, "textarea[id*='_content']")
                    dns_content_txt = dns_content.get_attribute('value')
                else:
                    continue
                self.domainNameInfo[domain]['dns'].append([dns_type_txt, dns_name_txt, dns_content_txt, rowid])
            except Exception as e:
                print("...", str(e))

    def updateDNSRecords(self, domain: str) -> None:
        assert domain in self.domainNameInfo
        self.browser.get(self.domainNameInfo[domain]['dns_url'])
        time.sleep(4) # TODO add a wait statement
        for entry in self.domainNameInfo[domain]['dns']:
            dns_type_txt = entry[0]
            dns_name_txt = entry[1]
            dns_content_txt = entry[2]
            rowid = entry[3]
            row = self.browser.find_element(By.CSS_SELECTOR, f"div[id='{rowid}']")
            if dns_type_txt in ['A', 'AAAA', 'CNAME', 'MX']:
                dns_content = row.find_element(By.CSS_SELECTOR, "input[id*='_content']")
            elif dns_type_txt in ['TXT']:
                dns_content = row.find_element(By.CSS_SELECTOR, "textarea[id*='_content']")
            else:
                continue
            dns_name = row.find_element(By.CSS_SELECTOR, "input[id*='_name']")
            dns_name.send_keys(Keys.CONTROL + 'a')
            dns_name.send_keys(Keys.DELETE)
            dns_name.send_keys(dns_name_txt)
            dns_content.send_keys(Keys.CONTROL + 'a')
            dns_content.send_keys(Keys.DELETE)
            dns_content.send_keys(dns_content_txt)

        self.browser.find_element(By.ID, "dnsedit_submit").click()
        WebDriverWait(self.browser, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//p[.='Je wijzigingen zijn opgeslagen.']")))

    def update(self, domain: str, dns_type: str, dns_name: str, dns_content: str) -> None:
        assert domain in self.domainNameInfo
        for entry in self.domainNameInfo[domain]['dns']:
            dns_type_txt = entry[0]
            dns_name_txt = entry[1]
            if dns_type_txt == dns_type and dns_name_txt == dns_name:
                entry[2] = dns_content