import tkinter

from Utilities._Time import *
from Utilities._Logs import *
import webbrowser
import threading
from Bot.IndeedScraper import IndeedScraperBot

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.UpdateFooterLinks()
        self.view.SearchNExportBtn.configure(command=self.SearchAndExportJobs)
        self.view.AllSearches.configure(command=self.CheckAllSearchStatus)

    def SearchAndExportJobs(self):
        '''
        It will collect the data and validate it, if the data is accurate, it will start running the BOT
        :return: None
        '''

        FinalizedData = {}
        Filter = self.GetDataFromAllFields()
        JobTitle = Filter.get("Job Title").strip()
        Searches = Filter.get("Searches").strip()

        if len(JobTitle) == 0 or JobTitle.isdigit(): # Warning:1
            self.UpdateStatusByTitle(JobTitle)

        elif (len(Searches) == 0 or Searches.isalpha()) and Searches != "ALL": # Warning:2
            self.UpdateStatusBySearches(Searches)

        else: # No Warning, It will RUN Here!
            self.UpdateStatusByExecution()
            threading.Thread(target=IndeedScraperBot(views = self.view,FilterValue = Filter).StartScraping(FinalizedData)).start()

            if len(FinalizedData) > 0:
                if len(FinalizedData.get("Job Name")) > 0:
                    self.UpdateStatusText(StatusText=Status.STATUS20)
                    Final_Message = self.model.PrepareAndExportData(Data_Dict = FinalizedData)

                    if Final_Message == "FILEPATH EMPTY":
                        self.UpdateStatusText(StatusText=Error.ERROR3, Seconds = 2)

                    elif Final_Message == "FILE SAVED":
                        self.UpdateStatusText(StatusText=Status.STATUS18, Seconds = 2)

                else:
                    self.UpdateStatusText(StatusText=Status.STATUS17)

            else:
                self.UpdateStatusText(StatusText = Error.ERROR2,FontColor = 'red')

            self.UpdateStatusText(StatusText=Status.STATUS1)
            self.view.JobTitleENT.delete(0, tkinter.END)
            self.view.JobLocENT.delete(0, tkinter.END)

    def UpdateStatusByExecution(self):
        '''
        It will update the status of Button and StatusText after the Search Button Pressed
        :return: None
        '''

        self.view.JobTitleENT.configure(state='disabled')
        self.view.JobLocENT.configure(state='disabled')
        self.view.IncludeSalary.configure(state='disabled')
        self.view.IncludeJobType.configure(state='disabled')
        self.view.IncludeEasyApply.configure(state='disabled')
        self.view.AllSearches.configure(state='disabled')
        self.view.SpecificSearchesENT.configure(state='disabled')
        self.view.SearchNExportBtn.configure(state='disabled')
        self.view.StatusofAll.configure(text=Status.STATUS6)

        self.view.SearchNExportBtn.update()

    def UpdateStatusBySearches(self, Searches : str):
        '''
        It will Validate if the Searches Quantity inserted correctly or not, and change status accordingly
        :param Searches: (str) -> Search Quantity the user will enter either by checkbox or entry field
        :return: None
        '''

        self.view.SpecificSearchesENT.configure(border_color='red', border_width=3)
        self.view.SearchNExportBtn.configure(fg_color='red')
        if len(Searches.strip()) == 0:
            self.view.StatusofAll.configure(text = Status.STATUS4 , text_color='red')
        elif Searches.isalpha() and not(Searches == "ALL"):
            self.view.StatusofAll.configure(text = Status.STATUS5, text_color='red')
        self.view.SpecificSearchesENT.update()

        WaitOne()
        self.view.SpecificSearchesENT.configure(border_color='#033C85', border_width=2)
        self.view.SearchNExportBtn.configure(fg_color='#033C85')
        self.view.StatusofAll.configure(text=Status.STATUS1, text_color='#033C85')

    def UpdateStatusByTitle(self, JobTitle : str):
        '''
        It will Validate if the Job Title inserted correctly or not, and change status accordingly
        :param JobTitle: (str) -> Job Title the user will enter in the entry box
        :return: None
        '''

        self.view.JobTitleENT.configure(border_color='red', border_width=3)
        self.view.SearchNExportBtn.configure(fg_color='red')
        self.view.StatusofAll.configure(text = Warning.WARNING3, text_color='red') if JobTitle.isdigit()\
        else self.view.StatusofAll.configure(text = Warning.WARNING2, text_color='red')
        self.view.JobTitleENT.update()

        WaitOne()
        self.view.JobTitleENT.configure(border_color='#033C85', border_width=2)
        self.view.SearchNExportBtn.configure(fg_color='#033C85')
        self.view.StatusofAll.configure(text= Status.STATUS1, text_color='#033C85')

    def GetDataFromAllFields(self):
        '''
        Get all the data from Entry boxes and Checkboxes widgets that will be used for Scraping
        :return: (dict) -> A single dimensional Dictionary containing the Widgets value in order
        '''

        JobTitleValue = self.view.JobTitleENT.get()
        JobLocationValue = self.view.JobLocENT.get()
        IncludeEasyApplyValue = self.view.IncludeEasyApply.get()
        IncludeSalaryValue = self.view.IncludeSalary.get()
        IncludeJobTypeValue = self.view.IncludeJobType.get()
        SearchesValue = "ALL" if self.view.AllSearches.get() == 1 else self.view.SpecificSearchesENT.get()

        Filter = {"Job Title" : JobTitleValue,
                "Job Location" : JobLocationValue,
                "Include Salary" : IncludeSalaryValue,
                "Include Job Type": IncludeJobTypeValue,
                "Include Easy Apply" : IncludeEasyApplyValue,
                "Searches": SearchesValue}
        return Filter

    def UpdateFooterLinks(self):
        '''
        It will update the footer Icons with their respective Links
        :return: None
        '''

        self.view.LinkedInBtn.configure(command=lambda: self.open_link("https://www.linkedin.com/in/manzoorahmedshaikh/"))
        self.view.FacebookBtn.configure(command=lambda: self.open_link("https://www.facebook.com/manzoorahmedshaikh234"))
        self.view.GithubBtn.configure(command=lambda: self.open_link("https://github.com/ManzoorAhmedShaikh"))

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

    def CheckAllSearchStatus(self):
        '''
        Dynamically hide or unhide the Search Quantity entry field based on "ALL" checkboxes value
        :return: None
        '''

        if self.view.AllSearches.get() == 1:
            self.view.SpecificSearchesENT.grid_remove()

        else:
            self.view.SpecificSearchesENT.grid(row=0, column=2, padx=5, sticky="EW")

    def open_link(self,url : str):
        '''
        Function to open a given URL in the web browser
        :param url: (str) -> The url link to redirect to
        :return: None
        '''

        webbrowser.open_new_tab(url)