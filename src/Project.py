import scraper
import lemKR
import pandas as pd

# WRITTEN IN PYTHON 3.6
# 2017.08.28 Edward Rha
# This code is written for personal educational use.

if __name__=="__main__":
    """
    NOTICE: If running this for the first time, you must manually set your starting articles at ../logs/last_update.csv
    August 28, 2017 starting locations:
    0001021525,0003090626,0002325585,0003204490,0003308799,0002749295,0002377613,0002814085,0002849023,0000230093
    """
    df = scraper.Update()
    lemKR.Create_Lem_Column(df)


    # df_temp = pd.read_json('data/Data_1_year_with_lem.json', orient='records', dtype={"articleID":'object'})


# if __name__ == '__main__':
#     df = Update()


    # Write the collected data to json
    # df.to_json(json_path)

    # df4.to_json('data/Data_1_year_with_lem_pt.5.json', orient='records', date_format="iso")
