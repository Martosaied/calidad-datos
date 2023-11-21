import openpyxl
import pandas as pd

color_dict = {
    18: 'headers',
    47: 'tan',
    42: 'green',
    43: 'yellow',
    8: 'orange',
    44: 'blue',
    53: 'orange',
}

color_to_type = {
    'tan': 'Unprovoked',
    'orange': 'Provoked',
    'green': 'Watercraft',
    'yellow': 'Sea Disaster',
    'blue': 'Invalid',
}

# Load the Excel file
file_path = "data/GSAF5.xlsx"
workbook = openpyxl.load_workbook(file_path)

worksheet = workbook.active 

# Define a function to get the background color of a cell
def get_cell_background_color(cell):
    fill = cell.fill
    if fill.start_color.index is not None:
        return fill.start_color.index
    return None

colors_by_cell = {}
for row in worksheet.iter_rows(min_row=1, max_row=6913, min_col=3, max_col=3):
    for cell in row:
        color = get_cell_background_color(cell)
        colors_by_cell[cell.coordinate.replace('C', '')] = color_dict[color]
colors = list(colors_by_cell.values())[1:]

# Close the workbook when you're done
workbook.close()

df = pd.read_excel('GSAF5.xlsx', engine='openpyxl')
df.drop(df.index[6912:], inplace=True)
df.insert(3, "Color", colors)
df.insert(4, "Colored Type", list(map(lambda x: color_to_type[x], colors)))

df.to_excel('data/GSAF5-withcolors.xlsx', index=False)