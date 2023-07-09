import zipfile
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
from sorter import sort_key


class ReadOds:

    def __init__(self, filename, sheets_name):
        print(f"opening ods")
        # get content xml data from OpenDocument file
        ziparchive = zipfile.ZipFile(filename, "r")
        xmldata = ziparchive.read("content.xml")
        ziparchive.close()
        
        #find bold styles
        self.soup = BeautifulSoup(xmldata, 'xml')
        self.sheets_name = sheets_name
        self.df = {}
        self.bold_names = self.get_bold_styles()
        
        if isinstance(sheets_name, str):
            self.sheets_name = [sheets_name]
            
        for sheet_name in sheets_name:
            sheet_rows = self.get_rows_in_sheet(sheet_name)
            header = self.get_columns_in_row(sheet_rows[0])
            header = [it for it in header if it]
            
            n_row = len(header)
            data = [dict(zip(header, (self.get_columns_in_row(row)[:n_row]))) for row in sheet_rows[1:]]
        
            self.df[sheet_name] = pd.DataFrame(data)
        

    def save_csv(self):
        print(f"saving csvs")
        for sheet_name in self.df:
            
            self.df[sheet_name].sort_values(by = ['pali_1'], ignore_index=True, inplace=True, key=lambda x: x.map(sort_key))
            filter = self.df[sheet_name]['pali_1'] != ""
            self.df[sheet_name] = self.df[sheet_name][filter]

            rows = self.df[sheet_name].shape[0]
            columns = self.df[sheet_name].shape[1]
            self.df[sheet_name].to_csv(f'{file_path}-{sheet_name.lower()}-s.csv', sep='\t', index=False, quoting=1)
            print(f" {file_path}-{sheet_name.lower()}-s.csv {rows} rows {columns} columns")

    def get_bold_styles(self):
        ''' 
        in xml has office:automatic-styles to configure automatic styles for document
        each style name is under style:style > style:text-properties [@fo:font-weight="bold"]
        '''
        all_auto_styles = self.soup.find_all('office:automatic-styles')
        all_text_properties = all_auto_styles[0].find_all('style:text-properties')
        all_bolds = [item for item in all_text_properties if item.has_attr('fo:font-weight') and item['fo:font-weight'] == 'bold']
        bold_names = [item.parent['style:name'] for item in all_bolds]
        return bold_names


    def get_rows_in_sheet(self, sheet_name):
        print(f"processing cell data for sheet {sheet_name.lower()}")
        current_sheet = self.soup.find('table:table', {'table:name':sheet_name})
        if current_sheet == None:
            print('could not find sheet', sheet_name)
            return None
        rows = current_sheet.find_all('table:table-row')
        #not ignore first row
        return rows[0:]


    def get_columns_in_row(self, row):
        ret_cells = []
        cells = row.find_all('table:table-cell')
        for cell in cells:
            cell_value = self.process_text(cell)

            if cell.has_attr('table:number-columns-repeated'):
                num_repeate = 0
                try:
                    num_repeate = int(cell['table:number-columns-repeated'])
                except ValueError:
                    print('failed to parse repeated cell under', cell)
                for _ in range(num_repeate - 1):
                    ret_cells.append(cell_value)
            ret_cells.append(cell_value)
        return ret_cells


    def process_text(self, cell):
        '''tex process for each column go here'''

        p_texts = cell.find_all('text:p')
        if p_texts == None:
            return ''

        ret_str = ''
        for p_text in p_texts:
            styled_texts = p_text.find_all('text:span')
            for styled_text in styled_texts:
                # Check if styled_text.string is not None
                if styled_text.string is not None:  
                #find bold styles and replace with b tag
                    if styled_text.has_attr('text:style-name'):
                        if styled_text['text:style-name'] in self.bold_names:
                            new_b_tag = self.soup.new_tag('b')
                            new_b_tag.string = styled_text.string
                            styled_text.replace_with(new_b_tag)
                        else:
                            styled_text.replace_with(styled_text.string)
                    else:
                        styled_text.replace_with(styled_text.string)

            #implement for <text:s text:c="5"> //5 spaces
            styled_texts = p_text.find_all('text:s')
            for styled_text in styled_texts:
                if styled_text.has_attr('text:c'):
                    styled_text.replace_with(' '*int(styled_text['text:c']))
                else:
                    styled_text.replace_with(' ')

            #convert tags to text
            ret_str += ''.join([str(it) for it in p_text.contents]) + '<br/>'

        return ret_str.removesuffix('<br/>')


if __name__ == '__main__':

    file_path = sys.argv[1]
    sheet_name = sys.argv[2]

    print(f"converting {file_path} to csv")
    a = ReadOds(f"{file_path}", {sheet_name})
    a.save_csv()
