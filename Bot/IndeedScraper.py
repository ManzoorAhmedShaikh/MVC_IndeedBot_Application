from Utilities._Selenium import SeleniumUtils
from Utilities._Logs import *
from Utilities._Time import *
import os
from bs4 import BeautifulSoup

class IndeedScraperBot:

    def __init__(self,views, FilterValue : dict):
        self.view = views
        self.Filter = FilterValue
        self.Sel = SeleniumUtils()

    def StartScraping(self, FinalData_Dict : dict):
        '''
        It will execute all the scraping operations
        :param FinalData_Dict: (dict) -> The Empty dictionary which will be filled with Scrapped data from Web
        :return: FinalData_Dict : (dict) -> The Dictionary of multiple list represeting different columns for the excel sheet
        '''

        try:
            URL = 'https://pk.indeed.com/'
            self.Sel.NavigateToPage(URL)
            WaitOne()
            self.UpdateStatusText(StatusText = Status.STATUS7)
            TotalJobs = self.SearchJob()

            if TotalJobs != 0:
                self.UpdateStatusText(StatusText = Status.STATUS11.format(TotalJobs))
                self.ScrapByFilter(Filter = self.Filter, Data_dict = FinalData_Dict)
                self.UpdateStatusText(StatusText = Status.STATUS19, FontColor = 'green', Seconds = 3)

            else:
                self.UpdateStatusText(StatusText = Warning.WARNING1, FontColor = 'red', Seconds = 2)

            self.ResetStatus()
            os.system("taskkill /f /im chromedriver.exe /T")

        except Exception as error:
            self.UpdateErrorStatus(Error.ERROR1)
            os.system("taskkill /f /im chromedriver.exe /T")
            print(f"Error -> {error}")

    def SearchJob(self):
        '''
        It will search the jobs on the given location
        :return: TotalJobs (int) -> Number of jobs found in the search results
        '''

        TotalJobs = 0
        try:
            SearchField_path = '//form[@id="jobsearch"]//input[contains(@aria-label,"Job title")]'
            SearchLoc_path = '//form[@id="jobsearch"]//input[contains(@aria-label,"Edit location")]'
            TotalJobs_path = "//div[contains(@class,'jobCount')]/span[1]"
            SearchButton_path = '//button[.="Find jobs"]'
            JobTitle = self.Filter.get('Job Title')
            JobLoc = self.Filter.get('Job Location')

            self.Sel.InsertKeys(JobTitle,SearchField_path)
            self.UpdateStatusText(StatusText = Status.STATUS8.format(JobTitle))
            self.Sel.InsertKeys(JobLoc,SearchLoc_path)
            self.UpdateStatusText(StatusText = Status.STATUS9.format(JobLoc))
            self.UpdateStatusText(StatusText = Status.STATUS10)
            self.Sel.ClickElement(SearchButton_path)

            if self.Sel.IsElementPresent(TotalJobs_path):
                TotalJobs = self.Sel.GetElement(TotalJobs_path).text.split()[0].replace('"','').replace("'","").replace(',','')
            return TotalJobs

        except Exception as error:
            print(f"Error in SearchJob() -> '{error}'")
            return TotalJobs

    def ScrapByFilter(self, Filter : dict, Data_dict : dict):
        '''
        It will execute the Scraping of Jobs and merge the data in the dictionary (Data_dict)
        :param Filter: (dict) -> The filter obtain from the Front End widgets, and it will be responsible to extract values accordingly
        :param Data_dict: (dict) -> An empty dictionary that will be filled with the data that our Bot Scrap
        :return: None
        '''

        Content_path = "(//div[contains(@id,'jobResults')]//ul)[1]"
        NextPageButton_path = '//a[@aria-label="Next Page"]'
        PopupCloseButton_path = "//div[@role='dialog']//button[@aria-label='close']"
        JobTitles = []
        JobLinks = []
        JobCompanies = []
        JobLocations = []
        JobSalaries = []
        JobTypes = []
        JobEasyApply = []

        while True:
            Content = self.Sel.GetElement(Content_path).get_attribute('innerHTML')
            soup = BeautifulSoup(Content,features="html.parser")

            #Mandatory Information for all Jobs
            JobTitles.extend([name.text.strip() for name in soup.find_all('a',attrs={"class":'jcs-JobTitle'})])
            JobLinks.extend(['https://pk.indeed.com' + link['href'] for link in soup.find_all('a',attrs={"class":'jcs-JobTitle'})])
            JobCompanies.extend([company.text.strip() for company in soup.find_all('span',attrs={"data-testid":'company-name'})])
            JobLocations.extend([location.text.strip() for location in soup.find_all('div',attrs={"data-testid":'text-location'})])

            #Salary and JobType Meta Data (Optional)
            JobMetaData = [x.text.strip() for x in soup.find_all('div', attrs={"class":'jobMetaDataGroup'})]
            if Filter.get("Include Salary") != 0:
                JobSalaries.extend([x.split('a month')[0].strip().upper().replace("TYPICALLY RESPONDS WITHIN 1 DAY",'') if 'a month' in x else '' for x in JobMetaData])

            if Filter.get("Include Job Type") != 0:
                Types = ['FULL-TIME',"CONTRACT","PART-TIME", "INTERNSHIP", "FRESHER", "NEW-GRAD", "TEMPORARY"]
                for data in JobMetaData:
                    if len([x for x in Types if x in data.upper()]) > 0:
                        JobTypes.extend([x for x in Types if x in data.upper()])
                    else:
                        JobTypes.append("")

            if Filter.get("Include Easy Apply") != 0:
                JobEasyApply.extend(["YES" if x.div.text.split('\n')[0].lower() == "easily apply" else "NO" for x in soup.find_all('div', attrs={"role":"presentation"})])

            self.UpdateStatusText(StatusText = Status.STATUS12.format(len(JobTitles)))
            self.HandleEmailPopup(PopupCloseButton_path)

            if Filter.get("Searches") != "ALL":
                if self.CheckJobsQuantityScrapped(Filter, JobTitles):
                    break

            if self.NextPageButtonAvailability(NextPageButton_path):
                break

        #Remove the exceeded amount of Jobs that scrapped by the Bot
        if Filter.get("Searches") != "ALL":
            JobTitles = JobTitles[:int(Filter.get("Searches"))]
            JobLinks = JobLinks[:int(Filter.get("Searches"))]
            JobLocations = JobLocations[:int(Filter.get("Searches"))]
            JobCompanies = JobCompanies[:int(Filter.get("Searches"))]

            if Filter.get("Include Salary") != 0:
                JobSalaries = JobSalaries[:int(Filter.get("Searches"))]

            if Filter.get("Include Job Type") != 0:
                JobTypes = JobTypes[:int(Filter.get("Searches"))]

            if Filter.get("Include Easy Apply") != 0:
                JobEasyApply = JobEasyApply[:int(Filter.get("Searches"))]

        Data_dict.update({
            "Job Name": JobTitles,
            "Job Location": JobLocations,
            "Job Company": JobCompanies,
            "Job Link": JobLinks,
            "Job Salary Range": JobSalaries,
            "Job Type": JobTypes,
            "Job Easy Apply (Indeed)": JobEasyApply
        })

    def HandleEmailPopup(self, PopupClose_path : str):
        '''
        It will check if there is any Email Subscription Popup appear on the web, if so then it closes it.
        :param PopupClose_path: (str) -> The Xpath of Popup close button in String
        :return: (bool) -> Based on the Availability, return True or False
        '''

        if self.Sel.IsElementPresent(PopupClose_path):
            self.Sel.ClickElement(PopupClose_path)
            WaitOne()

    def NextPageButtonAvailability(self, Button_path : str):
        '''
        It will check the Next Page Button, if it is present on the web or not, if not then give the stop indication to the Bot
        :param Button_path: (str) -> The Next Page Button Xpath which is in String
        :return: (bool) -> Based on Availability, return True or False
        '''

        if self.Sel.IsElementPresent(Button_path):
            self.UpdateStatusText(StatusText = Status.STATUS15)
            self.Sel.ClickElement(Button_path)
            WaitOne()
            return False

        else:
            self.UpdateStatusText(StatusText = Status.STATUS16)
            return True

    def CheckJobsQuantityScrapped(self, Filter : dict, Jobtitles : list):
        '''
        Check the quantity of Jobs Scrapped and Show the message on Status accordingly
        :param Filter: (dict) -> The dictionary of our input fields value which the user inserted
        :param Jobtitles: (list) -> The list of Job Titles Scrapped from the website
        :return: (bool) -> Based on number of Values, return True or False
        '''

        if int(Filter.get("Searches")) == len(Jobtitles):
            self.UpdateStatusText(StatusText=Status.STATUS13.format(len(Jobtitles), Filter.get("Searches")))
            return True

        elif int(Filter.get("Searches")) < len(Jobtitles):
            self.UpdateStatusText(StatusText=Status.STATUS14.format(len(Jobtitles), abs(len(Jobtitles) - int(Filter.get("Searches")))))
            return True

        else:
            return False

    def ResetStatus(self):
        '''
        It will reset all the widget of the Application to be able to re-use it again
        :return: None
        '''

        self.view.JobTitleENT.configure(state='normal')
        self.view.JobLocENT.configure(state='normal')
        self.view.IncludeSalary.configure(state='normal')
        self.view.IncludeJobType.configure(state='normal')
        self.view.IncludeEasyApply.configure(state='normal')
        self.view.AllSearches.configure(state='normal')
        self.view.SpecificSearchesENT.configure(state='normal')
        self.view.SearchNExportBtn.configure(state='normal')
        self.view.SearchNExportBtn.update()

    def UpdateStatusText(self, StatusText : str,FontColor = '#033C85', Seconds : int = 1):
        '''
        It will update the Status text, color, and hold that status for your desired time in seconds
        :param StatusText: (str) -> The message to show on Status section
        :param FontColor: (str) -> Color Hex code or english Alphabets color for the status text
        :param Seconds: (int) -> The amount of time to hold the Status text
        :return: None
        '''

        self.view.StatusofAll.configure(text = StatusText, text_color = FontColor)
        self.view.StatusofAll.update()
        WaitCustom(Seconds)

    def UpdateErrorStatus(self, StatusText : str):
        '''
        It will give the Error Message on Status Section and then reset it back to original position
        :param StatusText: (str) -> The message to show on the status section
        :return: None
        '''

        self.view.StatusofAll.configure(text=StatusText, text_color='red')
        self.view.StatusofAll.update()
        WaitCustom(5)
        self.view.StatusofAll.configure(text=Status.STATUS1, text_color='#033C85')
        self.view.StatusofAll.update()
        self.ResetStatus()
