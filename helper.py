def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Year', "City", 'Sport', 'Event', 'Medal'])
    medal_tally= medal_tally.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index()
    medal_tally['total']=medal_tally["Gold"] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally[['Gold', 'Silver', 'Bronze', 'total']] = medal_tally[['Gold', 'Silver', 'Bronze', 'total']].astype(int)


    return medal_tally

def country_year_list(df):
    df1 = df.drop_duplicates(subset=['Team', 'NOC', 'Year', "City", 'Sport', 'Event', 'Medal'])
    years = sorted(df1['Year'].value_counts().index)
    years.insert(0, "Overall")

    country = sorted(df1['region'].value_counts().index)
    country.insert(0, "Overall")

    return years,country


def fetch_year_country(df, year='Overall', country='Overall'):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Year', "City", 'Sport', 'Event', 'Medal'])
    flag = 0
    if country == 'Overall' and year == "Overall":
        temp_df = medal_df

    if country != 'Overall' and year == "Overall":
        temp_df = medal_df[medal_df['region'] == country]
        flag = 1

    if country == 'Overall' and year != "Overall":
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if country != 'Overall' and year != "Overall":
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        temp_df = temp_df.groupby(['Year'])[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year').reset_index()

    else:
        temp_df = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold',
                                                                                            ascending=False).reset_index()
    temp_df['total'] = temp_df["Gold"] + temp_df['Silver'] + temp_df['Bronze']
    temp_df[['Gold', 'Silver', 'Bronze', 'total']] = temp_df[['Gold', 'Silver', 'Bronze', 'total']].astype(int)
    return(temp_df)

def nations_over_time(df):
    nations_over_time = df.groupby('Year')['region'].nunique().reset_index()
    nations_over_time.rename(columns={"Year": "Edition",
                                       'region': "No. of Countries"}, inplace=True)
    return nations_over_time

def events_over_time(df):
    events_over_time = df.groupby('Year')['Event'].nunique().reset_index()
    events_over_time.rename(columns={"Year": "Edition",
                                     "Event": 'No. of Event'}, inplace=True)
    return events_over_time

def athlete_over_time(df):
    athlete_over_time = df.groupby('Year')['Name'].nunique().reset_index()
    athlete_over_time.rename(columns={"Year": "Edition",
                                      "Name": 'No. of Athlete'}, inplace=True)
    return athlete_over_time


def most_successful(df, sport):
    temp_df = df[~df['Medal'].isnull()]
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    temp_df = temp_df.groupby(['Name', 'Sport', 'region'])['Gold', 'Silver', 'Bronze'].sum().sort_values('Gold',
                                                                                                         ascending=False)
    temp_df['Total'] = temp_df[["Gold", "Silver", "Bronze"]].sum(axis=1)
    temp_df = temp_df.sort_values('Total', ascending=False).reset_index()
    temp_df = temp_df[['Name', 'Gold', 'Silver', 'Bronze', 'Total', 'Sport', 'region']]
    return temp_df.head(15)

def yearwise_medal_tally(df,country):
    new_df = df.dropna(subset=['Medal'])
    new_df.drop_duplicates(subset=['Team', 'NOC', 'Year', "City", 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df = new_df[new_df['region'] == country]
    temp_df = temp_df.groupby(['Year'])['Medal'].count().reset_index()
    return temp_df

def country_event_heatmap(df,country):
    new_df = df.dropna(subset=['Medal'])
    new_df.drop_duplicates(subset=['Team', 'NOC', 'Year', "City", 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df = new_df[new_df['region'] == country]
    pt=temp_df.pivot_table(index='Sport',columns='Year',values="Medal",aggfunc='count').fillna(0).astype('int')
    return pt


def country_wise_most_successful(df, country):
    temp_df = df[~df['Medal'].isnull()]
    temp_df = temp_df[temp_df['region'] == country]

    temp_df = temp_df.groupby(['Name', 'Sport'])['Gold', 'Silver', 'Bronze'].sum()
    temp_df['Total'] = temp_df[["Gold", "Silver", "Bronze"]].sum(axis=1)
    temp_df = temp_df.sort_values('Total', ascending=False).reset_index()
    temp_df = temp_df[['Name', 'Gold', 'Silver', 'Bronze', 'Total', 'Sport']]
    return temp_df.head(10)

def Athelete_age_distribution(df):
    ath_df = df.drop_duplicates(['Name', 'region'])
    all = ath_df['Age'].dropna()
    gold = ath_df[ath_df['Gold'] == 1]['Age'].dropna()
    silver = ath_df[ath_df['Silver'] == 1]['Age'].dropna()
    bronze = ath_df[ath_df['Bronze'] == 1]['Age'].dropna()
    return all,gold,silver,bronze

def weight_v_height(df,sport):
    ath_df = df.drop_duplicates(['Name', 'region'])
    ath_df["Medal"].fillna("No Medal", inplace=True)
    temp_df = ath_df[ath_df['Sport'] == sport]
    return temp_df

def men_v_women(df):
    ath_df = df.drop_duplicates(['Name', 'region'])
    temp = ath_df.groupby(['Sex', 'Year'])['Sex'].count()
    women = temp.loc['F'].reset_index().sort_values('Year')
    men = temp.loc['M'].reset_index().sort_values('Year')
    final = men.merge(women, on="Year")
    final = final.rename(columns={'Sex_x': "Male", "Sex_y": "Female"})
    return final