import pandas as pd



def preprocess(df,region_df):
    # filtering for summer olympics
    df=df[df['Season']=='Summer']
    # merging with region_df
    df=df.merge(region_df,on='NOC')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # joining one hot encoding medal
    df = df.join(pd.get_dummies(df['Medal']))
    return df