import pandas as pd
from tkinter import filedialog

class Model:

    def PrepareAndExportData(self, Data_Dict : dict = {}):
        '''
        It will export the file with your desired name and to your desired location
        :param Data_Dict: (dict) -> The Data Dictionary that have data scrapped from the website
        :return: (str) -> Message if the file saved or not
        '''

        if len(Data_Dict) > 0:
            Headers = ['Job Name', 'Job Location', 'Job Company', 'Job Link',
                       'Job Salary Range', 'Job Type', 'Job Easy Apply (Indeed)']

            if len(Data_Dict.get('Job Salary Range')) == 0:
                Headers.remove('Job Salary Range')

            if len(Data_Dict.get('Job Type')) == 0:
                Headers.remove('Job Type')

            if len(Data_Dict.get('Job Easy Apply (Indeed)')) == 0:
                Headers.remove('Job Easy Apply (Indeed)')

            Dataframe = pd.DataFrame(Data_Dict,columns = Headers)
            Dataframe.style.set_table_styles(
                [
                    {
                        'selector': 'th',
                        'props': [('font-weight', 'bold'), ('background-color', '#ADD8E6')]
                    }
                ]
            )

            # Open the save file dialog
            file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     initialfile="MyJobsList",
                                                     filetypes=[("EXCEL files", "*.xlsx")])

            if len(file_path.strip()) == 0:
                return "FILEPATH EMPTY"

            else:
                Dataframe.to_excel(file_path)
                return "FILE SAVED"