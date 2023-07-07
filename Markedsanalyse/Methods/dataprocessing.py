import os
import pandas as pd


def dict_to_dataframe(dict, dict_language, time):

    
    df = pd.DataFrame.from_dict(dict, orient = "index", columns = [time]).reset_index()
    df.columns = ["game", time]

    df_language = pd.DataFrame.from_dict(dict_language, orient = "index").stack().to_frame().reset_index()
    df_language.columns = ["game", "language", time]

    return df, df_language


def save_to_csv(df, df_language):

    
    df.to_csv(os.getcwd() + '\\data\\viewer_data.csv', header = True, index = False)
    df_language.to_csv(os.getcwd() + '\\data\\viewer_by_language_data.csv', header = True, index = False)


    return None 


def load_data():

    df = pd.read_csv(os.getcwd() + '\\data\\viewer_data.csv')
    df_language = pd.read_csv(os.getcwd() + '\\data\\viewer_by_language_data.csv')

    return df, df_language


def append_data(df1, df2, by_country = False):

    if not by_country:
        merged_data = df1.merge(df2, how = "outer", left_on = "game", right_on = "game")
    else:
        merged_data = df1.merge(df2, how = "outer", left_on = ["game", "language"], right_on = ["game", "language"])

    return merged_data

def dataprocessing(dict, dict_language, time):

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
