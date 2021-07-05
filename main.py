import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import os

shape_dir = 'data'
shape_files = [os.path.join(shape_dir, filename) for filename in os.listdir(shape_dir) if '.shp' in filename]

@st.cache
def get_clean_data_map():
    years = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    month_possibilities = {'JAN': ['JAN', 'JNR'],
                           'FEB': ['FEB'],
                           'MAR': ['MAR', 'MARET', 'MARE'],
                           'APR': ['APR', 'APRIL', 'APRI'],
                           'MAY': ['MAY', 'MEI'],
                           'JUN': ['JUN'],
                           'JUL': ['JUL'],
                           'AUG': ['AGU', 'AGS', 'AGT'],
                           'SEP': ['SEP', 'SEPT'],
                           'OCT': ['OCT', 'OKT', 'OKTOBER'],
                           'NOV': ['NOV'],
                           'DEC': ['DES']}


    clean_map = {

    }

    for year in years:
        shp = gpd.read_file([x for x in shape_files if str(year) in x][0])

        fields = list(shp.columns)
        mapping = {}

        for month in months:
            for month_possibility in month_possibilities[month]:
                field_possibilities = [f'BANJIR_{month_possibility}', f'{month_possibility}_{year}',
                                       f'{month_possibility}{year}',
                                       f'flood_{month_possibility}', f'{month_possibility}_{year % 100}',
                                       f'{month_possibility}', f'{month_possibility}{year % 100}',
                                       ] + [f'{month_possibility}_{str(year)[:i]}' for i in range(5)]
                field_possibilities = [x.upper() for x in field_possibilities] + [x.lower() for x in
                                                                                  field_possibilities]
                for field_poss in field_possibilities:
                    if field_poss in fields:
                        mapping[month] = field_poss
                        fields.remove(field_poss)
                        break
                if month in mapping: break
            if month not in mapping:
                clean_map[str(year)] = mapping

    return clean_map


st.title('Jakarta Flood Explorer')


clean_map = get_clean_data_map()

'### Select a Time'
year = st.select_slider(options=sorted(clean_map.keys()), label='Year')
month = st.select_slider(options=list(clean_map[year].keys()), label='Month')


shp = gpd.read_file([x for x in shape_files if str(year) in x][0])

fig, ax = plt.subplots()
shp.plot(clean_map[year][month], ax=ax, legend=True)
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
st.pyplot(fig)
