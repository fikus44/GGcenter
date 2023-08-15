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
data_ctry = pd.read_csv(os.getcwd() + '\\data\\viewer_by_language_data.csv', index_col = [0,1])
data_ctry.columns = pd.to_datetime(data_ctry.columns, format = '%Y-%m-%d %H:%M:%S').date 
data_ctry = data_ctry.transpose()


def daily_viewer(data):

    return data.groupby(data.index).mean().round(2)


def viewer_filter(data):

    # Compute daily viewers
    viewers = daily_viewers(data)

    # Yesteday and two weeks back as dates
    yesterday = date.today() - timedelta(days = 1)
    two_weeks = date.today() - timedelta(weeks = 2)

    # Truncate data and compute 2 week avg. viewers
    two_week_avg = viewers.loc[two_weeks:yesterday].mean().round(2)

    # Return titles with more than 400 avg daily viewers in the last 2 weeks
    two_week_avg_titles = list(two_week_avg[two_week_avg > 400].index)
    
    return two_week_avg_titles


def coverage_filter(data):

    # Yesteday and two weeks back as dates
    yesterday = date.today() - timedelta(days = 1)
    two_weeks = date.today() - timedelta(weeks = 2)

    covered_data = data.loc[two_weeks:yesterday].apply(lambda x: pd.isnull(x).mean() < .35)
    covered_data_titles = list(covered_data[covered_data == True].index)

    return covered_data_titles
    

def std_dev_filter(data):

    # Compute daily viewers
    viewers = daily_viewers(data)

     # Yesteday and two weeks back as dates
    yesterday = date.today() - timedelta(days = 1)
    two_weeks = date.today() - timedelta(weeks = 2)

    # Compute 2 week std. deviation
    std_dev = viewers[two_weeks:yesterday].std()

    # Compute 2 week average viewers
    two_week_avg = viewers.loc[two_weeks:yesterday].mean().round(2)

    # Keep games with std dev lower than avg number of viewers
    non_volatile = two_week_avg > std_dev
    non_volatile_titels = list(non_volatile[non_volatile == True].index)

    return non_volatile_titels

def language_filter(data):

    daily_viewers_lang = daily_viewers(data)

    # Yesteday and two weeks back as dates
    yesterday = date.today() - timedelta(days = 1)
    two_weeks = date.today() - timedelta(weeks = 2)

    # Truncate data
    daily_viewers_lang = daily_viewers_lang.loc[two_weeks:yesterday]

    titles = list(daily_viewers_lang.columns.get_level_values(0).unique())
    pct_dict = {}

    for title in titles:

        if daily_viewers_lang.loc[:, title].apply(lambda x:pd.isnull(x)).en.mean() > 0.85:
            pass
        else:
            en = daily_viewers_lang.loc[:, title].en.sum()
            all = daily_viewers_lang.loc[:, title].sum().sum() # sum for each language then across languages
            #other = ctry.loc[:, "Dota 2"].loc[:, ctry.loc[:, "Dota 2"].columns!= "en"]
            pct = en / all

            pct_dict[title] = pct
        
    filter = [k for (k,v) in pct_dict.items() if v > 0.3]


    return filter


def  filter_titles(data, ctry_data, output = False, timehorizon = {"weeks": 2}):

    # Compute daily viewers
    daily_viewers = daily_viewer(data)

    # Yesterday and the timehorizon specified amount of time back in time as dates
    yesterday = date.today() - timedelta(days = 1)
    start_date = date.today() - timedelta(**timehorizon)

    # Viewer filter
    # Truncate data and compute avg. daily viewers consistent with timehorizon
    avg_viewers = daily_viewers.loc[start_date:yesterday].mean().round(2)

    # Return titles with more than 400 avg daily viewers in the specified period
    viewer_titles = list(avg_viewers[avg_viewers > 400].index)


    # Coverage filter
    # Truncate data and determine if the coverage rate of each game in the
    # specified timehorizon is greater than 65%. Note this is raw hourly data
    covered_data = data.loc[start_date:yesterday].apply(lambda x: pd.isnull(x).mean() < .35)
    
    # Return titles with more than 65% coverage in hourly observations
    covered_titles = list(covered_data[covered_data == True].index)


    # Standard deviation filter
    # Compute standard deviation consistent with specified timehorizon
    std_dev = daily_viewers[start_date:yesterday].std()

    # Return titles with standard deviation lower than daily. avg # of viewers
    non_volatile = avg_viewers > std_dev
    non_volatile_titels = list(non_volatile[non_volatile == True].index)

    
    # Language filter
    # Compute daily viewers for ctry data
    daily_viewers_ctry = daily_viewer(ctry_data)
    titles = list(daily_viewers_ctry.columns.get_level_values(0).unique())

    # Initiate empty dict for percentage of english viewership
    pct_en = {}

    for title in titles:

        # If more than 95% of daily observations have 0 english viewers pass
        # The if statement avoids 0 in the numerator 
        if daily_viewers_ctry.loc[:, title].apply(lambda x:pd.isnull(x)).en.mean() > 0.95:
            pass

        # If there are 0 non-english viewers (= 0 in denominator) set the english percentage
        # viewship for the specific title to 1
        elif daily_viewers_ctry.loc[:, title].loc[:, daily_viewers_ctry.loc[:, title].columns!= "en"].apply(lambda x:pd.isnull(x).mean()).sum() == 1.0:
            pct_en[title] = 1

        else:
            en_viewers = daily_viewers_ctry.loc[:, title].en.sum()
            all_viewers = daily_viewers_ctry.loc[:, title].sum().sum() # sum for each language then across
            pct = en_viewers / all_viewers
            pct_en[title] = pct

        english_titles = [k for (k,v) in pct_en.items() if v > 0.3]

    # Match filters
    filter = set(viewer_titles).intersection(covered_titles).intersection(non_volatile_titels).intersection(english_titles)

    if output == True:
        print(f'Titles passing 400 viewers: {len(viewer_titles)}, \n Titles with 65% coverage: {len(covered_titles)}')
        print(f'Non-volatile titles: {len(non_volatile_titels)} \n English titles: {len(english_titles)}')
        return filter
    

    return filter






def table_1(data):

    viewer_filter = viewer_filter(data)
    coverage_filter = coverage_filter(data)
    std_dev_filter = std_dev_filter(data)
    lang_filter = language_filter(data)

    filter = set(viewer_filter).intersection(coverage_filter).intersection(std_dev_filter).intersection(lang_filter)

    data_filtered = data[filter]
    daily_viewers = daily_viewers(data_filtered)

    
    # Daily, weekly, biweekly, monthly, 3 months, 6 months, 1 year, and 2 year filter. 
    yesterday = date.today() - timedelta(days = 1)
    last_week = date.today() - timedelta(weeks = 1)
    two_weeks = date.today() - timedelta(weeks = 2)
    last_month = date.today() - relativedelta(months = 1)
    two_months = date.today() - relativedelta(months = 2)
    three_months = date.today() - relativedelta(months = 3)
    six_months = date.today() - relativedelta(months = 6)






    return None


# Nu skal jeg regne metrics ud på de games som er gået igennem, dvs. for forskellige perioder skal der regnes, avg viewers, coverage, std_dev og sprog 
# Tænker at lave en tabel med metrics for 2 uger, 1 måned, 2 måender og 3 måneder. 

# Den næste tabel med nye trending spil bliver så på 24 timer, 3 dage og 1 uge basis 










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


# For hver tabel / figur kan jeg filtrere data ned, så jeg får det vi skal bruge 


# 1) tabel med spil i første søjle og så avg. daily viewers, weekly, 2 weeks, 1 month, 3 month 6 month and 1 year. Sorteret i descending order efter en af dem. 
    # Jeg kan ikke have 5000 rækker, så jeg filtrerer data ned her. I denne tabel vil vi have spil der har vist konsistens, lav std. dev, højt viewership og 
    # det primære sprog er engelsk, i.e. spil vi kunne vælge

# 2) tabel med nye trending spil -- jeg skal gerne undgå at have de samme som i tabel 1 


# Script til at producere output
# 1) tabel med spil i første søjle og så avg. daily viewers, weekly, 2 weeks, 1 month, 3 month 6 month and 1 year. Sorteret i descending order efter en af dem. 
# 2) Tabel med 5 største procentuelle gain og loss (10 i alt) ift. sidste uge - så vi sammenligner altså weekly avg viewer tal med det samme tal for en uge siden
# 3) Figur der viser 10 største spils avg daily viewers -- måske to mere på lidt længere baner; en helt kort, en mellem og en lang
# 4) Tabel der lister nye spil, der er kommet på top 50 som ikke er set før med deres viewers sidste dag (de har ikke været på listen længere så kan ikke vise andet)
# 5) Samme tabel som 4'eren bare med seneste 3 dage -- på den måde kan vi se trends der begynder at forme sig
# Nu hvor vi bruger sproget:
# 5) Tabel med spil ad y-akse og sprog ad x-akse hvor de er sorteret i descending order efter engelske viewers. En tabel med daily, en med weekly, 2 weeks, 1 month 3 months etc. 

# Jeg forestiller mig output er en PDF med relevante figurer og tabeller. PDF'en genereres hver dag. 

# To features ved tabeller som skal med; std. dev. og coverage, i.e. hvor mange observationer vi har som procent af samtlige obs. 

# Overvej i twitch.py at hvis jeg få error 500 (Se task log på pythnanywhere) så skal jeg prøve at køre koden igen 