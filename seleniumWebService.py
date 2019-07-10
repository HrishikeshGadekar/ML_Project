from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
opts = Options()
opts.set_headless()
assert  opts.headless
class seleniumWebService:
    def __int__(self):
        pass
    def openBrowser( self , Url ):
        try:
            self.Browser = Chrome(options=opts)
        except:
            self.Browser = Chrome (options = opts ,  executable_path = '/home/busportal/Downloads/googMapsProjV2/chromedriver' )
        self.Browser.implicitly_wait(100)
        self.Browser.get(Url)

    def closeBrowser(self):
        self.Browser.quit()


