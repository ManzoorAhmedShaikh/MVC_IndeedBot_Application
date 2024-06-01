import customtkinter
from customtkinter import *
from tkinter import *
from PIL import Image, ImageTk

class View:
    def __init__(self, root):

        customtkinter.set_appearance_mode('light')

        self.root = root
        self.root.title("Indeed Bot")
        self.root.geometry('650x550')
        self.root.resizable(False, False)
        self.root.configure(fg_color='white')
        self.root.iconbitmap("Assets/APP_Icon.ico")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.DesignWindow()

    def DesignWindow(self):
        '''
        Design the complete Indeed Bot App with their interactive Widgets
        :return: None
        '''

        #Checkboxes Frame defining
        CheckboxesFrame = CTkFrame(self.root, border_width=0,bg_color='white', fg_color='white')
        CheckboxesFrame.grid_columnconfigure(0, weight=1)
        CheckboxesFrame.grid_columnconfigure(1, weight=1)
        CheckboxesFrame.grid_columnconfigure(2, weight=1)

        #Search Quantity Frame defining
        SearchQuantityFrame = CTkFrame(self.root, border_width=0,bg_color='white', fg_color='white')
        SearchQuantityFrame.grid_columnconfigure(0, weight=1)
        SearchQuantityFrame.grid_columnconfigure(1, weight=1)
        SearchQuantityFrame.grid_columnconfigure(2, weight=1)

        #Footer Frame Defining
        FooterFrame = CTkFrame(self.root,bg_color='white', fg_color='white')

        self.Icon = CTkLabel(self.root,text = '', fg_color='white', bg_color='white', image = PhotoImage(file = 'Assets/Logo.png'))
        self.JobTitle = CTkLabel(self.root, text = "JOB TITLE ", font = ('Arial Black', 18, 'bold'), bg_color='white', text_color='#033C85')
        self.JobLoc = CTkLabel(self.root, text = "JOB LOCATION ", font = ('Arial Black', 18, 'bold'), bg_color='white', text_color='#033C85')

        self.JobTitleENT = CTkEntry(self.root, placeholder_text='Enter Job Title', font = ('Arial', 13, 'normal'), width=200, bg_color='white', fg_color='white', border_color='#033C85')
        self.JobLocENT = CTkEntry(self.root, placeholder_text='Enter Job Location', font = ('Arial', 13, 'normal'), width=200, bg_color='white', fg_color='white', border_color='#033C85')

        self.IncludeSalary = CTkCheckBox(CheckboxesFrame,text = "INCLUDE SALARY", font = ('Arial Black', 14.5, 'bold'), bg_color='white', text_color='#033C85', border_color='#033C85')
        self.IncludeJobType = CTkCheckBox(CheckboxesFrame,text = "INCLUDE JOB TYPE", font = ('Arial Black', 14.5, 'bold'), bg_color='white', text_color='#033C85', border_color='#033C85')
        self.IncludeEasyApply = CTkCheckBox(CheckboxesFrame,text = "INCLUDE EASY APPLY", font = ('Arial Black', 14.5, 'bold'), bg_color='white', text_color='#033C85', border_color='#033C85')

        self.SearchQuantity = CTkLabel(SearchQuantityFrame,text = "SEARCH QUANTITY", font = ('Arial Black', 18, 'bold'), bg_color='white', text_color='#033C85')
        self.AllSearches = CTkCheckBox(SearchQuantityFrame,text = "ALL" , font = ('Arial Black', 14.5, 'bold'), bg_color='white', text_color='#033C85', border_color='#033C85')
        self.AllSearches.select()
        self.SpecificSearchesENT = CTkEntry(SearchQuantityFrame,placeholder_text='Enter in numbers (eg. 10 ~ 1000)', font = ('Arial', 13, 'normal'), width=200, bg_color='white', fg_color='white', border_color='#033C85')

        self.StatusofAll = CTkLabel(self.root,text = 'EXECUTION NOT STARTED YET', font = ('Arial Black', 13.5, 'bold','underline'), text_color='#033C85')
        self.SearchNExportBtn = CTkButton(self.root, text = 'SEARCH AND EXPORT JOBS', corner_radius=10,  font = ('Arial Black', 15, 'bold'), bg_color='white', fg_color='#033C85')

        self.LinkedInBtn = CTkButton(FooterFrame,text = '',width=0,hover_color = 'white', image = self.resize_image('Assets/LinkedIn_Logo.png',45,25),fg_color='white')
        self.FacebookBtn = CTkButton(FooterFrame,text = '',width=0,hover_color = 'white', image = self.resize_image('Assets/Facebook_Logo.png',45,25),fg_color='white')
        self.GithubBtn = CTkButton(FooterFrame,text = '',width=0,hover_color = 'white', image = self.resize_image('Assets/Github_Logo.png',25,25),fg_color='white')
        FooterTextL = CTkLabel(FooterFrame,text = 'Developed By:')
        FooterTextR = CTkLabel(FooterFrame,text = 'Manzoor Ahmed', font = ('Arial Black', 14.5, 'bold'))

        #Root Widgets Placement
        self.Icon.grid(row = 0, column = 0, columnspan = 2,sticky = "")
        self.JobTitle.grid(row = 1, column = 0, pady=15, sticky = 'SEW')
        self.JobLoc.grid(row = 2, column = 0, pady=5, sticky = 'SEW')
        self.JobTitleENT.grid(row = 1, column = 1, pady=15,padx = 5, sticky = 'SEW')
        self.JobLocENT.grid(row = 2, column = 1, pady=5,padx = 5 , sticky = 'SEW')
        SearchQuantityFrame.grid(row=3, column=0, columnspan = 2, pady=15, sticky = "NEW")
        CheckboxesFrame.grid(row=4, column=0, columnspan = 2,pady=10, sticky = "NEW")
        self.StatusofAll.grid(row = 5, column = 0, columnspan = 3,pady = 20, sticky="N")
        self.SearchNExportBtn.grid(row = 6, column = 0, columnspan = 3, ipadx=10,ipady = 8, pady=5, sticky="N")
        FooterFrame.grid(row=7, column=0, columnspan = 2,pady=10, sticky = "")

        #Search Quantity Widgets Placement
        self.SearchQuantity.grid(row = 0, column = 0, padx = 25, sticky = "W")
        self.AllSearches.grid(row = 0, column = 1, padx = 10, sticky = "E")

        #Additional Features Checkboxes Widgets Placement
        self.IncludeSalary.grid(row = 0, column = 0, padx=15, sticky="EW")
        self.IncludeJobType.grid(row = 0, column = 1, padx=15, sticky="EW")
        self.IncludeEasyApply.grid(row = 0, column = 2, padx=15, sticky="EW")

        #Footer Widgets Placement
        self.LinkedInBtn.grid(row = 0, column = 0,columnspan = 2,ipadx = 0,padx = 12, sticky='')
        self.FacebookBtn.grid(row = 0, column = 1,columnspan = 2,ipadx = 0,padx = 12,sticky='')
        self.GithubBtn.grid(row = 0, column = 2,columnspan = 2,ipadx = 0,padx = 12,sticky='')
        FooterTextL.grid(row = 1, column = 0,columnspan = 2, sticky='')
        FooterTextR.grid(row = 1, column = 2,columnspan = 2, sticky='')

    def resize_image(self,path : str, new_width : int, new_height : int):
        '''
        Open an image file and resize it according to given parameters
        :param path: (str) -> Relative File path where the image is present
        :param new_width: (int) -> New Width after resizing in Whole number i.e in Integers
        :param new_height: (int) -> New Height after resizing in Whole number i.e in Integers
        :return: Image object
        '''
        img = Image.open(path)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)