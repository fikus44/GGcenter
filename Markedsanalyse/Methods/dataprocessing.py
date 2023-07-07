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


# Når det er oppe at køre så kal dataprocessing ikke returnere noget, den slutter bare med at gemme conslidated data, ellers så skal den og så behvøer jeg ikke loade data
# for så at arbejde med det for at lave figurer og tabeller osv. 

    




# Gem til csv eller excel (hvad er bedst) med et test sæt (koden til det) -- load det bagefter (koden til det) og så append med ny tester som så gemmes (kode til det)

# Funktion som gemmer ved at appende til eksisterende data -- i starten bliver det på drive, men det skal op i skyen på et tidspunkt. Det bliver raw data jeg gemmer
# herefter skal jeg så have et nyt ark med transformeret data f.eks. daily average. 

# Der er lidt en udfordring ved at gøre det idet at de spil jeg får ud 1) ikke vil være de samme hver gang og 2) rækkefølgen på dem vil være anderledes og 3) der kan være nye spil.
# Jeg tror måske den bedste måde, selvom den måske er lidt dum, er at loade raw data ind hver gang (det bliver bare større og større) og så merge med det datasæt. Tror ikke den bliver
# stor nok til det bliver et issue dog. Jeg får 200 entries om dagen, på et år er det 200 * 365 = 73000, hvilket jeg har regnet mig frem til er ca 87 MB (før downcasting)

# Det ville være federe at gøre det uden at loade data, men jeg skal have det loaded alligevel når jeg skal transfomere (til f.eks. averages) og så arbejde med det; måske kan linket
# her bruges: https://stackoverflow.com/questions/76345249/pandas-to-csv-method-in-append-mode-with-dataframes-with-different-columns


