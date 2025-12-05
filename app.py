import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

if 'show_main_page' not in st.session_state:
    st.session_state.show_main_page = True

df = pd.read_csv('modeled_dataset.csv')

topic_colorschemes = {
    'Honey and Daylight': 'gold',
    'My Heart in Your Palms': 'mediumvioletred',
    'Ghosts of You': 'tomato',
    'Rain or Shine': 'deepskyblue',
    'Unapologetically ME!': 'limegreen',
    'Beginning\'s Butterflies': 'orchid',
    'Hearts on the Edge': 'crimson',
    'POV': 'cyan',
    'Echoes of Betrayal': 'orange',
}

topic_names = [
    'Honey and Daylight',
    'My Heart in Your Palms',
    'Ghosts of You',
    'Rain or Shine',
    'Unapologetically ME!',
    'Beginning\'s Butterflies',
    'Hearts on the Edge',
    'POV',
    'Echoes of Betrayal'
]

topic_descriptions = [
    'When love makes life feel brighter than ever',
    'A love that burns alone',
    'Hoping you feel as much as I do',
    'Choices that lingeres for a lifetime',
    "I dont't need to be choosen to know my worth",
    'The innocent thrill, rush, and chaos of young love',
    'I want the heartbreaks and sadness',
    'Revisiting and Rretelling stories from the past',
    'Every hurt remembered, every grudge alive'
]

topic_words = [
    "york, hold, lights, feel, time, rains, floor, waitin, babe, called",
    "red, girl, wanna, gotta, lost, night, blue, lucky, walk, boy",
    "baby, bad, blood, grow, feel, smile, time, fly, belong, wanna",
    "live, time, wait, list, white, afraid, follow, god, wild, style",
    "gonna, shake, hate, break, play, fake, baby, friends, mind, nice",
    "stay, time, woods, trouble, mad, daylight, remember, finally, hard, wanna",
    "love, beautiful, time, life, leave, loved, hands, bad, dancin, dark",
    "remember, night, talk, starlight, forget, dreams, day, hair, lips, karma",
    "dress, car, story, dance, night, tonight, happy, summer, town, gonna"
]

if st.sidebar.button("Main Page", type="primary"):
    st.session_state.show_main_page = True
    st.rerun()

st.sidebar.header("Dataset Summary")
st.sidebar.write(f"**Total albums:** {df['album_name'].nunique()}")
st.sidebar.write(f"**Total number songs:** {len(df)}")
st.sidebar.write(f"**Topics identified:** {len(topic_names)}")

form = st.sidebar.form(key='topic_form')

selected_topic = form.selectbox(
    'Select a topic to explore:',
    options=topic_names
)

if selected_topic:
    topic_songs = df[df['top_topic'] == topic_names.index(selected_topic)]
    topic_songs = topic_songs.sort_values('top_prob', ascending=False)
    song_list = topic_songs['song_name'].tolist()

submit_button = form.form_submit_button(label='Show Results')

if st.session_state.show_main_page and not submit_button:
    st.header("Lyrical Topic Modeling (Taylor's Version)")
    st.write("Experimenting how accurate topic modeling using LDA is at capturing the themes in Taylor Swift's music.")
   
    st.subheader("Number of Songs per Topic")
    topic_counts = df['top_topic'].value_counts().sort_index()
    topic_counts_df = pd.DataFrame({
        'Topic': [topic_names[i] for i in topic_counts.index],
        'Number of Songs': topic_counts.values
    })

    topic_counts_df_sorted = topic_counts_df.sort_values('Number of Songs', ascending=True)  

    fig1 = px.bar(
        topic_counts_df_sorted,
        x='Number of Songs',  
        y='Topic', 
        color='Number of Songs',
        color_continuous_scale='pinkyl',
        orientation='h', 
        text='Number of Songs'
    )
    fig1.update_layout(
        yaxis_title="",
        xaxis_title="Number of Songs",
        showlegend=False,
        height=400
    )
    fig1.update_traces(
        texttemplate='%{text}',
        textposition='outside'  
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Topics Identified")
    st.write("""
    1. **Honey and Daylight** - When love makes life feel brighter than ever
    2. **My Heart in your Palms** - A love that burns alone
    3. **Ghosts of You** - Hoping you feel as much as I do
    4. **Rain or Shine** - Choices that lingeres for a lifetime
    5. **Unapologetically ME!** - I dont't need to be choosen to know my worth
    6. **Beginning's Butterflies** -The innocent thrill, rush, and chaos of young love
    7. **Hearts on the Edge** - I want the heartbreaks and sadness
    8. **POV** - Revisiting and Retelling stories from the past
    9. **Echoes of Betrayal** - Every hurt remembered, every grudge alive
    """)

    st.divider()

    st.subheader("How Positive are Taylor's Albums?")
    album_sentiment = df.groupby('album_name').agg({
        'sentiment_score': 'mean',
        'sentiment_label': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'neutral',
        'song_name': 'count'
        }).reset_index()
    
    album_sentiment.columns = ['Album', 'Avg_Sentiment_Score', 'Dominant_Sentiment', 'Song_Count']
    album_sentiment = album_sentiment.sort_values('Avg_Sentiment_Score', ascending=True)
    fig7 = px.bar(
        album_sentiment,
        x='Avg_Sentiment_Score',
        y='Album',
        title='Average Sentiment Score by Album (Higher = More Positive)',
        color='Avg_Sentiment_Score',
        color_continuous_scale='RdYlGn',  
        orientation='h',
        hover_data=['Dominant_Sentiment', 'Song_Count'],
        range_x=[0.7, album_sentiment['Avg_Sentiment_Score'].max() * 1.1] 
    )

    fig7.update_layout(
        yaxis_title="Album",
        xaxis_title="Average Sentiment Score (-1 to 1)",
        height=500,
        coloraxis_colorbar=dict(title="Score"),
        yaxis={'categoryorder': 'total ascending'},
        xaxis=dict(
            range=[0.7, album_sentiment['Avg_Sentiment_Score'].max() * 1.1]  
        )
    )

    st.plotly_chart(fig7, use_container_width=True)
    
elif submit_button:
    st.session_state.show_main_page = False
    
    st.header(f"Topic: {selected_topic}")
    
    topic_idx = topic_names.index(selected_topic)
    
    # Simple write statements without columns
    st.write(f"**Description:** {topic_descriptions[topic_idx]}")
    st.write(f"**Top 10 Keywords:** {topic_words[topic_idx]}")
    
    st.divider()

    topic_df = df[df['top_topic'] == topic_names.index(selected_topic)]

    st.subheader("Number of Songs in this topic by Album")

    album_counts = topic_df['album_name'].value_counts().reset_index()
    album_counts.columns = ['Album', 'Number of Songs']
    album_counts = album_counts.sort_values('Number of Songs', ascending=True)

    colorscheme = topic_colorschemes.get(selected_topic, 'lightsteelblue')

    fig2 = px.bar(
        album_counts,
        y='Album',
        x='Number of Songs',
        color_discrete_sequence=[colorscheme],
        orientation='h',
        text='Number of Songs'
    )

    fig2.update_layout(
        height=500,
        yaxis_title="",
        xaxis_title="Number of Songs",
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )

    fig2.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        width=0.6
    )

    st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader(f"Songs list:")
    
    display_cols = ['song_name', 'album_name', 'track_no', 'top_prob', 'sentiment_label', 'link']
    display_df = topic_df[display_cols].sort_values('top_prob', ascending=False)

    display_df_display = pd.DataFrame({
        'Song Name': display_df['song_name'],
        'Album': display_df['album_name'],
        'Track': display_df['track_no'],
        'Topic Prob': (display_df['top_prob'] * 100).round(2).astype(str) + '%',
        'Sentiment': display_df['sentiment_label'],
        'Link': display_df['link'].apply(lambda x: f'<a href="{x}" target="_blank">Listen</a>')
        })  

    st.write(display_df_display.to_html(escape=False, index=True), unsafe_allow_html=True)
    st.divider()

    st.subheader(f"Topic vs Sentiment Score: {selected_topic}")

    if len(topic_df) > 1:  
        fig3 = px.scatter(topic_df, 
                         x='top_prob', 
                         y='sentiment_score',
                         color='sentiment_label',  
                         color_discrete_map={
                             'positive': 'blue',
                             'neutral': 'gray',
                             'negative': 'yellow'
                         },
        hover_data=['album_name', 'song_name', 'top_prob', 'sentiment_score', 'sentiment_label'],
        labels={
                'top_prob': 'Topic Probability',
                'sentiment_score': 'Sentiment Score',
                'sentiment_label': 'Sentiment'
                })

        fig3.update_layout(
            height=500,
            title_font_size=20,
            title_x=0.5,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            legend_title_font_size=14,
            legend_font_size=11,
            hoverlabel=dict(
                font_size=12,
                font_family="Arial"
            )
        )

        fig3.update_traces(
            marker=dict(size=12, opacity=0.8, line=dict(width=1, color='DarkSlateGrey')),
            selector=dict(mode='markers')
        )

        mean_sentiment = topic_df['sentiment_score'].mean()

        correlation = topic_df['top_prob'].corr(topic_df['sentiment_score'])


        fig3.add_annotation(
            x=0.05,
            y=0.95,
            xref="paper",
            yref="paper",
            text=f"Correlation: {correlation:.3f}",
            showarrow=False,
            font=dict(size=12, color="black"),
            bgcolor="white",
            bordercolor="black",
            borderwidth=1,
            borderpad=4
        )

        st.plotly_chart(fig3, use_container_width=True)

        st.subheader(f"Statistics Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Number of Songs", len(topic_df))
        with col2:
            st.metric("Avg Topic Probability", f"{topic_df['top_prob'].mean():.3f}")
        with col3:
            st.metric("Avg Sentiment", f"{mean_sentiment:.3f}")
        with col4:
            st.metric("Correlation", f"{correlation:.3f}")
        
        st.subheader(f"Sentiment Distribution: {selected_topic}")
        sentiment_counts = topic_df['sentiment_label'].value_counts()
        fig4 = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            color=sentiment_counts.index,
            color_discrete_map={
                'positive': 'blue',
                'neutral': 'gray',
                'negative': 'yellow'
            }
        )
        st.plotly_chart(fig4, use_container_width=True)
        
    else:
        st.info(f"Only {len(topic_df)} song(s) in this topic. Scatter plot requires multiple data points.")


st.sidebar.header("Data Export")
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download dataset as CSV",
    data=csv,
    file_name="taylor_swift_topics.csv",
    mime="text/csv"
)