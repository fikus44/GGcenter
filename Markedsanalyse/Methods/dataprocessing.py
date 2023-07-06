import os
import pandas as pd
import datetime as dt


def to_dataframe(dict, columns, by_country = False):

    if not by_country:
        dataframe = pd.DataFrame.from_dict(dict, orient = "index", columns = [columns])
    else:
        dataframe = pd.DataFrame.from_dict(dict, orient = "index").stack().to_frame()
        dataframe.columns = [columns]
    
    return dataframe


def to_csv(dataframe):


    return None 



# Funktion som gemmer ved at appende til eksisterende data -- i starten bliver det på drive, men det skal op i skyen på et tidspunkt. 
# Der er lidt en udfordring ved at gøre det idet at de spil jeg får ud 1) ikke vil være de samme hver gang og 2) rækkefølgen på dem vil være anderledes og 3) der kan være nye spil 


