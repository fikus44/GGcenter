import os
import pandas as pd

'''
dataprocessing.py encloses all methods pertaining to
merging each data query with the existing data

'''

def dict_to_dataframe(dict, dict_language, time):

    '''
    dict_to_dataframe() transforms the raw data from 
    Twitch storted in dictionaries to pandas dataframes
    using the from_dict() method.

    Parameters
    ----------
    dict : Dictionary
        Dictionary enclosing # of viewers per game. 

    dict_language : Dictionary
        Dictionary enclosing the # of viewers per language
        per game

    time : Datetime object
        Datetime object enclosing the date and hour
        of the data

    '''

    # Dict to dataframe
    df = pd.DataFrame.from_dict(dict, orient = "index", columns = [time]).reset_index()
    df.columns = ["game", time]

    # Language dict to dataframe
    df_language = pd.DataFrame.from_dict(dict_language, orient = "index").stack().to_frame().reset_index()
    df_language.columns = ["game", "language", time]

    return df, df_language


def save_to_csv(df, df_language):

    '''
    save_to_csv() saves the dataframe to csv
    locally on a pre-specified path.

    Parameters
    ----------
    df : DataFrame
        Dataframe with # of viewers per game to save

    df_language: DataFrame
        Dataframe with # of viewers per language
        per game to save

    '''
    
    df.to_csv(os.getcwd() + '\\data\\viewer_data.csv', header = True, index = False)
    df_language.to_csv(os.getcwd() + '\\data\\viewer_by_language_data.csv', header = True, index = False)


    return None 


def load_data():

    '''
    load_data() loads the CSV files enclosing the # 
    of viewers per game and # of viewers per language
    per game

    '''

    df = pd.read_csv(os.getcwd() + '\\data\\viewer_data.csv')
    df_language = pd.read_csv(os.getcwd() + '\\data\\viewer_by_language_data.csv')

    return df, df_language


def append_data(df1, df2, by_country = False):

    '''
    append_data() appends data from the most recent
    query to the existing raw data. 

    Parameters
    ----------
    df1 : DataFrame
        Dataframe with # of viewers per game to save

    df2 : DataFrame
        Dataframe with # of viewers per language
        per game to save

    by_country : Boolean
        by_country indicates whether we are dealing
        with the game or game + language level data

    '''

    if not by_country:
        merged_data = df1.merge(df2, how = "outer", left_on = "game", right_on = "game")
    else:
        merged_data = df1.merge(df2, how = "outer", left_on = ["game", "language"], right_on = ["game", "language"])

    return merged_data


def dataprocessing(dict, dict_language, time):

    '''
    dataprocessing() combines all the previous
    methods into one function. It takes the raw
    data and appends it to the existing data set
    which it saves locally. 

    Parameters
    ----------
    dict : Dictionary
        Dictionary with # of viewers per game. 

    dict_language: Dictionary
        Dictionary with # of viewers per language
        per game

    '''

    # Dict to pd.DataFrame
    df, df_language = dict_to_dataframe(dict = dict, dict_language = dict_language, time = time)

    # Load raw library data 
    df_lib, df_language_lib = load_data()

    # Append new data to existing raw data
    merged_data = append_data(df1 = df_lib, df2 = df, by_country = False)
    merged_data_language = append_data(df1 = df_language_lib, df2 = df_language, by_country = True)

    # Save consolidated data
    save_to_csv(merged_data, merged_data_language)

    return merged_data, merged_data_language
