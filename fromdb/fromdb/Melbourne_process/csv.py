__author__ = 'team18'
# This program is used to extract education level from a csv file. The csv is manually downloaded from Aurin
import xlrd,json


data = xlrd.open_workbook('education.xlsx')

table = data.sheet_by_name(u'Sheet1')
fp = open("education.txt", "w")


dict2 = {}
for i in range(1, table.nrows):
    row_content = table.row_values(i, 0, table.ncols)
    
    dict2[row_content[0]] = round(row_content[1],2)
    
print(dict2)
fp.write(json.dumps(dict2))
fp.close
