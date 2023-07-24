import pandas as pd
import os
#import matplotlib as pyplot 
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# Load viewer data from which output is created
# Parse dates, and transpose to get dates in index column (Pandas prefers this)
data = pd.read_csv(os.getcwd() + '\\data\\viewer_data.csv', index_col= "game")
data.columns = pd.to_datetime(data.columns, format = '%Y-%m-%d %H:%M:%S').date # Remove timestamp with .date
data = data.transpose()

# Load viewer per country data from which output is created
data_ctry = pd.read_csv(os.getcwd() + '\\data\\viewer_by_language_data.csv', index_col= "game")



def avg_daily_viewers(data):
    
    # For each day and game if the # of NaN observations is greater than 67% -> False, i.e.
    # if at least 17/24 hours were unrecorded (NaN) due to low viewership --> False
    # if at lest 8/24 (16/24) hours were recorded --> True
    data_bool_67 = data.groupby(data.index).apply(lambda x: pd.isnull(x).mean() < .67)
    
    # Compute average daily viewers
    daily_viewers = data.groupby(data.index).mean().round(2)

    # For each day and game, set average daily viewers of "volatile big streamer games" to 0
    # and not NaN to have them count toward the averages
    daily_viewers = daily_viewers.mask(~data_bool_67).fillna(0)

    return daily_viewers



def table(data):

    # Daily, weekly, biweekly, monthly, 3 months, 6 months, 1 year, and 2 year filter. 
    yesterday = date.today() - timedelta(days = 1)
    last_week = date.today() - timedelta(weeks = 1)
    two_weeks = date.today() - timedelta(weeks = 2)
    last_month = date.today() - relativedelta(months = 1)
    two_months = date.today() - relativedelta(months = 2)
    three_months = date.today() - relativedelta(months = 3)
    six_months = date.today() - relativedelta(months = 6)
    last_year = date.today() - relativedelta(year = 2022)
    two_years = date.today() - relativedelta(year = 2021)


    # Create empty DataFrame
    table = pd.DataFrame(columns = ["2 weeks", "24 hours", "1 week", "1 month", "2 months", 
                                    "3 months", "6 months", "1 year", "2 years"])
    
    # Create startdate and enddate values
    start_date = [two_weeks, yesterday, last_week, last_month, two_months, three_months, six_months,
                  last_year, two_years]
    end_date = yesterday
    
    # Append average viewers to the dataframe
    for index, start in enumerate(start_date, 0):
        data_temp = data.loc[start:end_date].mean().round(2).sort_values(ascending = False)[:50]
        table[table.columns[index]] = data_temp

    return table






# Script til at producere output
# 1) tabel med spil i første søjle og så avg. daily viewers, weekly, 2 weeks, 1 month, 3 month 6 month and 1 year. Sorteret i descending order efter en af dem. 
# 2) Tabel med 5 største procentuelle gain og loss (10 i alt) ift. sidste uge - så vi sammenligner altså weekly avg viewer tal med det samme tal for en uge siden
# 3) Figur der viser 10 største spils avg daily viewers -- måske to mere på lidt længere baner; en helt kort, en mellem og en lang
# 4) Tabel der lister nye spil, der er kommet på top 50 som ikke er set før med deres viewers sidste dag (de har ikke været på listen længere så kan ikke vise andet)
# 5) Samme tabel som 4'eren bare med seneste 3 dage -- på den måde kan vi se trends der begynder at forme sig
# Nu hvor vi bruger sproget:
# 5) Tabel med spil ad y-akse og sprog ad x-akse hvor de er sorteret i descending order efter engelske viewers. En tabel med daily, en med weekly, 2 weeks, 1 month 3 months etc. 

# Jeg forestiller mig output er en PDF med relevante figurer og tabeller. PDF'en genereres hver dag. 