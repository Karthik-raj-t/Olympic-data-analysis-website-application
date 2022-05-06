import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocessor.preprocess(df, region_df)
st.sidebar.title('Olympic Analysis')
user_menu = st.sidebar.radio(
    'select an option',
    ('Medal Tally', 'Overall Analysis','Country Wise Analysis', 'Athlete Wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country = helper.country_year_list(df)

    Selected_year = st.sidebar.selectbox('Select Year',years)
    Selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df,Selected_year,Selected_country)
    if Selected_year == 'All Years' and Selected_country == 'All Country':
        st.title('Overall Tally')
    if Selected_year != 'All Years' and Selected_country == 'All Country':
        st.title('Medal Tally in'+' '+ str(Selected_year) )
    if Selected_year != 'All Years' and Selected_country != 'All Country':
        st.title(Selected_country + "'s performance in " + str(Selected_year)+ " olympics")
    if Selected_year == 'All Years' and Selected_country != 'All Country':
        st.title(Selected_country + "'s Overall Performance")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    st.text(' ')
    st.text(' ')
    st.text(' ')
    st.text(' ')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)
    nations_over_time = helper.data_over_time(df,"region")
    st.title('Participating Nations Over Years')
    fig = px.line(nations_over_time, x='Edition', y='total',labels={"total":'No. of Countries'})
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, "Event")
    st.title('Events Over Years')
    fig = px.line(events_over_time, x='Edition', y='total',labels={"total": "No. of Events"})
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, "Name")
    st.title('Athletes Over Years')
    fig = px.line(athletes_over_time, x='Edition', y='total', labels={"total": "No. of Athletes"})
    st.plotly_chart(fig)

    st.title('No. of Event over time (Every sport)')
    fig,ax = plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.set(font_scale=1.5)
    ax = sns.heatmap(x.pivot_table(index = 'Sport', columns='Year',values = 'Event',aggfunc='count').fillna(0).astype('int'),annot=True,)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = helper.sport_list(df)
    Sports = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df,Sports)
    st.table(x)

if user_menu == 'Country Wise Analysis':
    country = helper.country_list(df)
    Country = st.sidebar.selectbox('Select a Country',country)
    country_df = helper.yearwise_medal_tally(df,Country)
    st.title(Country + "'s Medal Tally Over the Years")
    fig = px.line(country_df, x='Year', y='Medal', labels={"Medal": 'No. of Medals'})
    st.plotly_chart(fig)

    st.title(Country +' excels in the following sports')
    pt = helper.country_event_heatmap(df,Country)
    fig, ax = plt.subplots(figsize=(25, 25))
    sns.set(font_scale=1.4)
    ax = sns.heatmap(pt,annot =True )
    st.pyplot(fig)

    st.title(Country + "'s successful atheletes")
    x = helper.most_successful_countrywise(df,Country)
    st.table(x)

if user_menu == 'Athlete Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x4, x3, x2, x1], ['Bronze Medalist', 'Silver Medalist', 'Gold Medalist', 'Overall'],
                             show_hist=False, show_rug=False, )
    fig.update_layout(autosize=False,width=900,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=900, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=40)
    plt.legend(fontsize =10)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=900, height=600)
    st.plotly_chart(fig)