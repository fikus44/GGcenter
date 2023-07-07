from methods import twitch as tw
from methods import dataprocessing as dp

print("Getting fresh data")

# Request data from Twitch's API
time, twitch_viewers, twitch_viewers_by_country = tw.loop_through_games()

# Dataprocessing
tester, tester_lang = dp.dataprocessing(dict = twitch_viewers, dict_language = twitch_viewers_by_country, time = time)

print("done getting fresh data")


# Hvad er steps herfra? Nu skal jeg automatisere scriptet således det bare kan køre uden mig og så skal jeg begynde at arbejde med data 