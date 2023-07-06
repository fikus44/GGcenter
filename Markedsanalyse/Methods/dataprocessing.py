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



# Funktion som gemmer ved at appende til eksisterende data -- i starten bliver det på drive, men det skal op i skyen på et tidspunkt. Det bliver raw data jeg gemmer
# herefter skal jeg så have et nyt ark med transformeret data f.eks. daily average. 

# Der er lidt en udfordring ved at gøre det idet at de spil jeg får ud 1) ikke vil være de samme hver gang og 2) rækkefølgen på dem vil være anderledes og 3) der kan være nye spil.
# Jeg tror måske den bedste måde, selvom den måske er lidt dum, er at loade raw data ind hver gang (det bliver bare større og større) og så merge med det datasæt. Tror ikke den bliver
# stor nok til det bliver et issue dog. Jeg får 200 entries om dagen, på et år er det 200 * 365 = 73000, hvilket jeg har regnet mig frem til er ca 87 MB (før downcasting)

# Det ville være federe at gøre det uden at loade data, men jeg skal have det loaded alligevel når jeg skal transfomere (til f.eks. averages) og så arbejde med det; måske kan linket
# her bruges: https://stackoverflow.com/questions/76345249/pandas-to-csv-method-in-append-mode-with-dataframes-with-different-columns


