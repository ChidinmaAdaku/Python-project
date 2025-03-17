# 1) The code below is for importing libraries to Pycharm for data cleaning,
# analysis and data visualization

from pathlib import Path
import pandas as pd
import plotly.express as px

# To import plotly.express package, follow the instruction below:
# a) Click on Files
# b) On the drop-down menu Click on Settings
# c) Under "project" click on Python Interpreter (make sure to use the Python 3.9(venv))
# d) Click on the plus (+) icon
# e) Search for plotly-express and click install


# 2) The code below is to import csv file into pycharm IDE environment and protect your computer pathway security for data analysis using pandas library.

file_path = input("Please enter the file path for the CSV file: ")
file = Path(file_path)
if file.is_file():
    try:
        data = pd.read_csv(file)
        print("File successfully loaded.")
    except Exception as e:
        print("An error occurred: ", e)
else:
    print("The file path is invalid or the file does not exist.")


# 3a) The codes below are for Exploratory Data Analysis (EDA), to  inspect the csv file and generate a data summary out of the csv file.
# This will show the descriptive summary of the variables.
# 3b) data.to_string is a function for generating the entire sheet from the csv file.
# 3c) data.info(), and data.describe() perform a similar function of generating descriptive analysis.
# 3d) data.isnull().sum() generates the sum of the "null values" across the columns.

print(data.to_string())
print(data.describe())
print(data.isnull().sum())
print(data.info())

# 4a) The data variables(columns) in this csv file is large and
# I will clean the data to only work with few selected rows and columns.
# 4b) Here, to clean up the data. I declared three objects in a dictionary
# named 'new_dtypes' and also created a new list of selected variables named 'new_cols'.
# 4c) Therefore, the codes below are to select few columns and data types I will
# be working with to free up my computer memory.

new_cols = ['iso_code', 'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
            'icu_patients', 'weekly_icu_admissions', 'weekly_hosp_admissions', 'new_tests',
            'total_tests', 'positive_rate', 'total_vaccinations', 'people_vaccinated',
            'people_fully_vaccinated', 'total_boosters', 'new_vaccinations', 'population', 'life_expectancy',
            'excess_mortality']

new_dtypes = {
    'iso_code': 'object',
    'location': 'object',
    'date': 'object',
}

for col in new_cols[3:]:
    new_dtypes[col] = 'float32'

data_last = pd.read_csv(file,
                        usecols=new_cols,
                        dtype=new_dtypes)

print(data_last.head())

print(data_last.info())


# 5a) Here I have defined "location" as "country" and created a new dictionary function.
# 5b) Any country passed through the dictionary will generate all the information for that country.

dic_country = {}
for country in data_last.location.unique():
    dic_country[country] = data_last[data_last.location == country].copy()

print(dic_country['United Kingdom'])

# 6a) I intend to generate the date of first recorded covid case per country.
# 6b) This combines tuples in a for loop to parse through the dictionary. Here, I used logic ('if', 'else', 'for').
# 6c) Given that each country recorded different dates for new covid cases, I will want to pick
# the date with the first non-NaN value to represent the day one of first recorded covid case.
# 6d) Here, Plotly is used to generate a Histogram that wil
# be displayed for graphical representation of the first covid case.
begin_pan = {}
for i in dic_country.keys():
    loc = dic_country[i]['new_cases'].first_valid_index()
    if loc is not None:
        if data_last.at[loc, 'date'] not in begin_pan.keys():
            begin_pan[data_last.at[loc, 'date']] = [1]
        else:
            begin_pan[data_last.at[loc, 'date']][0] += 1
    else:
        begin_pan[dic_country[i].date.unique()[0]] = [1]

print(begin_pan)

pd_begin = pd.DataFrame.from_dict(begin_pan, orient='index', columns=['values'])

print(pd_begin)

pd_begin.index = pd.to_datetime(pd_begin.index, format='%d/%m/%Y')

pd_begin['year'] = pd.DatetimeIndex(pd_begin.index).year
pd_begin['month'] = pd.DatetimeIndex(pd_begin.index).month
pd_begin['day'] = pd.DatetimeIndex(pd_begin.index).day
pd_begin['weekday'] = pd.DatetimeIndex(pd_begin.index).weekday

print(pd_begin)

begin_data = pd_begin[(pd_begin.year == 2020) & (pd_begin.month <= 6)]

print(begin_data)

begin_data = begin_data.sort_values(['month', 'day'], ascending=True)

print(begin_data)

fig = px.histogram(begin_data, x=begin_data.index, y='values', marginal="box")
fig.update_layout(
    title="1. Beginning of COVID-19 in Europe",
    xaxis_title="Date",
    yaxis_title="Count",
    plot_bgcolor='beige',
    font=dict(
        family="Arial",
        size=14,
        color="darkblue"
    )
)
fig.show()

# 7a) There are so much missing data(null values) in the dataset
# and the codes below will replace the null values with '0'.
data_last['date'] = pd.to_datetime(data_last['date'], format='%d/%m/%Y')


data_last = data_last.fillna(0)

data_last.fillna(0)

print(data_last.info())

# 8a) Once the missing data(null values)have been replaced with '0'.
# Each county information can be generated with the codes below with zero null values.
dic_country = {}
for country in data_last.location.unique():
    dic_country[country] = data_last[data_last.location == country].copy()

print(dic_country['Germany'])

# 9a) concatenate function will be used to merge France,
# Germany and United Kingdom data together in a table with displayed variables
# After generating the table of comparison, Plotly will be used
# to generate a line graph showing the trend of the data across the 3 countries.

result = pd.concat([dic_country['United Kingdom'].set_index('date'), dic_country['France'].set_index('date'),
                    dic_country['Germany'].set_index('date')], axis=1, join="inner")

print(result)

# 10a) The codes below are to analyze covid "total_cases" across the 3 countries(United Kingdom, France and Germany).

t_cases = result['total_cases']

print(t_cases)

t_cases.columns = ['United Kingdom', 'France', 'Germany']

print(t_cases)

fig = px.line(t_cases, title='2. Total Cases in United Kingdom, France and Germany',
              color_discrete_sequence=["aquamarine", "cornflowerblue", "goldenrod"],)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Cases",
    plot_bgcolor='MintCream',
    font=dict(
        family="Arial",
        size=14,
        color="darkblue"
    )
)
fig.show()

# 11a) The code below generates line graphs using Plotly to analyze
# new cases in United Kingdom, France and Germany.

new_cases = result['new_cases']
new_cases.columns = ['United Kingdom', 'France', 'Germany']

fig2 = px.bar(new_cases, title='3. New Cases in United Kingdom, France and Germany',
              color_discrete_sequence=["Gold", "IndianRed", "MediumTurquoise"],)

fig2.update_layout(
    xaxis_title="Date",
    yaxis_title="New Cases",
    plot_bgcolor='SeaShell',
    font=dict(
        family="Arial",
        size=14,
        color="darkblue"
    )
)

fig2.show()

uk_data = dic_country['United Kingdom']

# 12a) This generates a scatter plot for Covid patients admitted in ICU in the UK
fig = px.scatter(uk_data, x="date", y="icu_patients", size='people_vaccinated', title='4. ICU cases in UK')
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="ICU Patients",
    plot_bgcolor='Gold',
    font=dict(
        family="Arial",
        size=14,
        color="darkblue"
        )
)
fig.show()

# 13a) This generates a scatter plot for weekly Covid patients hospitalized weekly in the UK

fig = px.scatter(uk_data[uk_data['weekly_hosp_admissions'] != 0],
                 x="date",
                 y="weekly_hosp_admissions",
                 size='people_vaccinated',
                 title='5. Weekly hospitalisation cases in UK',
                 color_discrete_sequence=['magenta']
                 )
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Weekly Hospitalisations",
    plot_bgcolor='lightblue',
    font=dict(
         family="Arial",
         size=14,
         color="darkblue"
    )
)
fig.show()

# 14a) This generates a line graph for people fully vaccinated in the UK

fig = px.line(uk_data[uk_data['people_fully_vaccinated'] != 0],
              x='date',
              y='people_fully_vaccinated',
              title='6. Full vaccinated people in UK'
              )
fig.update_layout(
         xaxis_title='Date',
         yaxis_title='Number of people fully vaccinated',
         plot_bgcolor='lightblue',
         font=dict(family="Arial", size=14, color="darkblue")

)
fig.show()

# Full vaccinated people in UK

uk_data = dic_country['United Kingdom']
deu_data = dic_country['Germany']
fra_data = dic_country['France']

print(uk_data[['new_cases', 'new_deaths', 'population']]. describe)

print(deu_data[['new_cases', 'new_deaths', 'population']]. describe)

print(fra_data[['new_cases', 'new_deaths', 'population']]. describe)

fig = px.line(uk_data[uk_data['people_fully_vaccinated'] != 0],
              x='date',
              y='people_fully_vaccinated',
              title='7. Full vaccinated people in UK'

              )
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Number of people fully vaccinated',
    plot_bgcolor='lightblue',
    font=dict(
        family="Arial",
        size=14,
        color="darkblue"
    )

)
fig.show()

# Full vaccinated people in France
fig = px.line(fra_data[fra_data['people_fully_vaccinated'] != 0],
              x='date',
              y='people_fully_vaccinated',
              title='8. Full vaccinated people in France'

              )
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Number of people fully vaccinated',
    plot_bgcolor='lightblue',
    font=dict(
        family="Arial",
        size=14,
        color="darkblue"
    )

)
fig.show()

# Full vaccinated people in Germany
fig = px.line(deu_data[deu_data['people_fully_vaccinated'] != 0],
              x='date',
              y='people_fully_vaccinated',
              title='9. Full vaccinated people in Germany'

              )
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Number of people fully vaccinated',
    plot_bgcolor='lightblue',
    font=dict(
        family="Arial",
        size=14,
        color="darkblue"
    )

)
fig.show()
