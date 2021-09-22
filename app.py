import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import helper
import preprocessor


df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df= preprocessor.preprocess(df,region_df)

st.sidebar.title("Olaympics Analysis")
st.sidebar.image('https://cdn.wallpapersafari.com/0/72/S307o5.jpg')
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)



if(user_menu=='Medal Tally'):
    st.sidebar.header('Medal Tally')
    year,country=helper.country_year_list(df)
    selcted_year=st.sidebar.selectbox('Select Year',year)
    selcted_Country = st.sidebar.selectbox('Select Country', country)
    medal_tally=helper.fetch_year_country(df,selcted_year,selcted_Country)
    if selcted_year=='Overall' and selcted_Country=='Overall':
        st.title('Overall Tally')
    if selcted_year != 'Overall' and selcted_Country == 'Overall':
        st.title("Medal Tally in "+str(selcted_year)+" Olympics")
    if selcted_year == 'Overall' and selcted_Country != 'Overall':
        st.title("Overall Performance of "+str(selcted_Country)+" In Olympics")
    if selcted_year != 'Overall' and selcted_Country != 'Overall':
        st.title( str(selcted_Country) + " Performance In "+str(selcted_year)+" Olympics")

    st.table(medal_tally)

if (user_menu=='Overall Analysis'):
    st.title('Top Statistics')
    no_of_years = df.Year.nunique() - 1
    no_of_nations = df.region.nunique()
    no_of_events = df.Event.nunique()
    no_of_cites = df.City.nunique()
    no_of_sports = df.Sport.nunique()
    no_of_athelets = df.Name.nunique()

    col1,col2,col3=st.columns(3)

    with col1:
        st.header('Editions')
        st.title(no_of_years)

    with col2:
        st.header('Countries')
        st.title(no_of_nations)

    with col3:
        st.header('Cites')
        st.title(no_of_cites)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.header('Events')
        st.title(no_of_events)

    with col5:
        st.header('Sports')
        st.title(no_of_sports)

    with col6:
        st.header('Athelits')
        st.title(no_of_athelets)

    st.title('Participating Nation Over Years')
    nations_over_time=helper.nations_over_time(df)
    fig1=px.line(nations_over_time,x='Edition',y='No. of Countries')
    fig1.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig1)

    st.title('Events Over Years')
    events_over_time=helper.events_over_time(df)
    fig2 = px.line(events_over_time, x='Edition', y='No. of Event')
    fig2.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig2)

    st.title('Athlete Over Years')
    athlete_over_time = helper.athlete_over_time(df)
    fig3=px.line(athlete_over_time,x='Edition',y='No. of Athlete')
    fig3.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig3)

    st.title('No. of Events Over time (Every sport)')
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values="Event", aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title('Best Athelets of Every Sport')
    all_sport =sorted(df.Sport.unique().tolist())
    all_sport.insert(0, "Overall")
    sport=st.selectbox('Selcect a Sport', all_sport)
    temp_df=helper.most_successful(df,sport)
    st.table(temp_df)


if (user_menu=="Country-wise Analysis"):
    st.sidebar.title('Country-wise Analysis')

    all_country = sorted(df.dropna(subset=["Medal"]).region.dropna().unique().tolist())
    country= st.sidebar.selectbox('Selcect a Country', all_country)
    temp_df= helper.yearwise_medal_tally(df,country)

    fig = px.line(temp_df,x='Year',y='Medal')
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title(country+' Medal Tally Over the Years')
    st.plotly_chart(fig)

    st.title(country + ' excels in the following Sports ')
    pt=helper.country_event_heatmap(df,country)
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title('Top 10 athelets of '+country)
    temp_df=helper.country_wise_most_successful(df,country)
    st.table(temp_df)

if (user_menu=='Athlete wise Analysis'):
    st.title('Athlete wise Analysis')
    all,gold,silver,bronze=helper.Athelete_age_distribution(df)
    fig = ff.create_distplot([all, gold, silver, bronze],
                             ['Age Distriburton', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Age distribution of Athletes')
    st.plotly_chart(fig)

    x=[]
    name=[]
    famous_sports=['Basketball', 'Judo', 'Boxing', 'Wrestling', 'Swimming',
               'Softball', 'Hockey', 'Archery', 'Triathlon', 'Football',
               'Rhythmic Gymnastics', 'Athletics', 'Badminton', 'Fencing',
               'Gymnastics', 'Baseball', 'Shooting','Weightlifting', 'Cycling',
               'Rowing','Sailing', 'Diving', 'Art Competitions',
               'Synchronized Swimming','Handball', 'Table Tennis', 'Tennis',
               'Taekwondo','Beach Volleyball','Golf', 'Tug-Of-War', 'Rugby',
               'Cricket', 'Polo', 'Ice Hockey']

    ath_df = df.drop_duplicates(['Name', 'region'])
    for sport in famous_sports:
        temp_df=ath_df[ath_df['Sport']==sport]
        x.append(temp_df[temp_df['Gold'] == 1]['Age'].dropna())
        name.append(sport)
    fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Age distribution wrt Sport (Gold Medalist)')
    st.plotly_chart (fig)

    st.title('Height vs Weight')
    all_sport = sorted(df.dropna(subset=["Medal",'Age','Weight']).Sport.unique().tolist())
    sport = st.selectbox('Selcect a Sport', all_sport)
    fig,ax=plt.subplots()
    temp_df=helper.weight_v_height(df,sport)
    ax=sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)

    st.pyplot(fig)

    st.title('Men_vs_Women Participating over years')
    final=helper.men_v_women(df)
    fig=px.line(final,x='Year',y=['Male',"Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)



















