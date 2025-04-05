import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "YourNewPassword"
DB_NAME = "Scrapping"
TABLE_NAME = "Imdbmovies"

def load_data_from_sql():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        query = f"SELECT Title, Rating, Views, Genre, Duration FROM {TABLE_NAME}"
        df = pd.read_sql(query, conn)
        conn.close()

        df.columns = [col.lower() for col in df.columns]
        return df
    except Exception as e:
        st.error(f"Error loading data from MySQL: {e}")
        return None

def top_movies(df, rating_col='rating', votes_col='views', top_n=10):
    df_sorted = df.sort_values(by=[rating_col, votes_col], ascending=[False, False])
    return df_sorted.head(top_n)

def plot_genre_distribution(df):
    st.subheader("Genre Distribution")
    genre_series = df['genre'].dropna().str.split(',').explode().str.strip()
    genre_counts = genre_series.value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    genre_counts.plot(kind='bar', color='salmon', ax=ax)
    ax.set_title("Number of Movies by Genre")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Number of Movies")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_average_duration_by_genre(df):
    st.subheader("Average Movie Duration by Genre")
    df = df.dropna(subset=['genre', 'duration'])
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
    genre_duration = df.copy()
    genre_duration['genre'] = genre_duration['genre'].str.split(',').explode().str.strip()
    avg_duration = genre_duration.groupby('genre')['duration'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_duration.plot(kind='barh', color='mediumseagreen', ax=ax)
    ax.set_title("Average Duration by Genre")
    ax.set_xlabel("Average Duration (minutes)")
    ax.set_ylabel("Genre")
    st.pyplot(fig)

def plot_voting_trends_by_genre(df):
    st.subheader("Voting Trends by Genre")
    df = df.dropna(subset=['genre', 'views'])
    df['views'] = pd.to_numeric(df['views'], errors='coerce')
    genre_views = df.copy()
    genre_views['genre'] = genre_views['genre'].str.split(',').explode().str.strip()
    avg_votes = genre_views.groupby('genre')['views'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_votes.plot(kind='barh', color='dodgerblue', ax=ax)
    ax.set_title("Average Votes by Genre")
    ax.set_xlabel("Average Votes (Views)")
    ax.set_ylabel("Genre")
    st.pyplot(fig)

def plot_rating_distribution(df):
    st.subheader("Rating Distribution")
    df = df.dropna(subset=['rating'])
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.histplot(df['rating'], bins=10, kde=True, color='coral', ax=ax)
    ax.set_title("Histogram of Movie Ratings")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

def genre_based_rating_leaders(df):
    st.subheader("Top-Rated Movie for Each Genre")
    df = df.dropna(subset=['genre', 'rating', 'title'])
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    exploded = df.copy()
    exploded['genre'] = exploded['genre'].str.split(',').explode().str.strip()

    top_per_genre = exploded.sort_values('rating', ascending=False).groupby('genre').first().reset_index()
    top_per_genre = top_per_genre[['genre', 'title', 'rating']]

    st.dataframe(top_per_genre, use_container_width=True)

def most_popular_genres_by_voting(df):
    st.subheader("Most Popular Genres by Voting (Pie Chart)")
    df = df.dropna(subset=['genre', 'views'])
    df['views'] = pd.to_numeric(df['views'], errors='coerce')

    exploded = df.copy()
    exploded['genre'] = exploded['genre'].str.split(',').explode().str.strip()

    genre_votes = exploded.groupby('genre')['views'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 8))
    genre_votes.plot.pie(ax=ax, autopct='%1.1f%%', startangle=140, cmap='Set3', wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
    ax.set_ylabel('')
    ax.set_title("Most Popular Genres by Total Votes")
    st.pyplot(fig)

def duration_extremes(df):
    st.subheader("Duration Extremes (Shortest & Longest Movies)")
    df = df.dropna(subset=['title', 'duration'])
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')

    shortest = df.loc[df['duration'].idxmin()]
    longest = df.loc[df['duration'].idxmax()]

    extremes = pd.DataFrame([
        {"Type": "Shortest", "Title": shortest['title'], "Duration (min)": shortest['duration']},
        {"Type": "Longest", "Title": longest['title'], "Duration (min)": longest['duration']}
    ])
    st.table(extremes)

def ratings_by_genre_heatmap(df):
    st.subheader("Ratings by Genre (Heatmap)")
    df = df.dropna(subset=['genre', 'rating'])
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    exploded = df.copy()
    exploded['genre'] = exploded['genre'].str.split(',').explode().str.strip()

    genre_ratings = exploded.groupby('genre')['rating'].mean().sort_values()
    genre_ratings_df = pd.DataFrame(genre_ratings).T 

    fig, ax = plt.subplots(figsize=(12, 1.5))
    sns.heatmap(genre_ratings_df, cmap="YlGnBu", annot=True, fmt=".2f", cbar=False, ax=ax)
    ax.set_title("Average Rating per Genre", pad=20)
    st.pyplot(fig)

def correlation_analysis(df):
    st.subheader("Correlation: Ratings vs Voting Counts")
    df = df.dropna(subset=['rating', 'views'])
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['views'] = pd.to_numeric(df['views'], errors='coerce')

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x='views', y='rating', alpha=0.6, color='teal', ax=ax)
    ax.set_title("Scatter Plot: Ratings vs Voting Counts")
    ax.set_xlabel("Views (Voting Count)")
    ax.set_ylabel("Rating")
    st.pyplot(fig)

def filter_by_all_criteria(df):
    st.sidebar.header("Filters")

    
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
    df['views'] = pd.to_numeric(df['views'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    
    duration_option = st.sidebar.selectbox(
        "Select Duration Range:",
        ("Show All", "< 2 hours", "2–3 hours", "> 3 hours")
    )
    if duration_option == "< 2 hours":
        df = df[df['duration'] < 120]
    elif duration_option == "2–3 hours":
        df = df[(df['duration'] >= 120) & (df['duration'] <= 180)]
    elif duration_option == "> 3 hours":
        df = df[df['duration'] > 180]

   
    if 'genre' in df.columns:
        genre_series = df['genre'].dropna().str.split(',').explode().str.strip()
        unique_genres = sorted(genre_series.unique())

        selected_genres = st.sidebar.multiselect(
            "Select Genres:",
            options=unique_genres,
            default=unique_genres
        )

        if selected_genres:
            df = df[df['genre'].apply(
                lambda g: any(genre.strip() in selected_genres for genre in str(g).split(','))
            )]

    vote_option = st.sidebar.selectbox(
        "Select Voting Count Range:",
        ("Show All", "< 1,000", "1,000 – 10,000", "10,000 – 100,000", "> 100,000")
    )
    if vote_option == "< 1,000":
        df = df[df['views'] < 1000]
    elif vote_option == "1,000 – 10,000":
        df = df[(df['views'] >= 1000) & (df['views'] <= 10000)]
    elif vote_option == "10,000 – 100,000":
        df = df[(df['views'] > 10000) & (df['views'] <= 100000)]
    elif vote_option == "> 100,000":
        df = df[df['views'] > 100000]

    rating_option = st.sidebar.selectbox(
        "Select Rating Range:",
        ("Show All", "8.0 and above", "7.0 – 8.0", "6.0 – 7.0", "Less than 6.0")
    )
    if rating_option == "8.0 and above":
        df = df[df['rating'] >= 8.0]
    elif rating_option == "7.0 – 8.0":
        df = df[(df['rating'] >= 7.0) & (df['rating'] < 8.0)]
    elif rating_option == "6.0 – 7.0":
        df = df[(df['rating'] >= 6.0) & (df['rating'] < 7.0)]
    elif rating_option == "Less than 6.0":
        df = df[df['rating'] < 6.0]

    return df


def main():
    st.title("Movie Dashboard (MySQL)")

    df = load_data_from_sql()

    if df is not None:
      
        filtered_df = filter_by_all_criteria(df)
        st.subheader("Filtered Movies by Duration")
        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("---") 

        
        if all(col in df.columns for col in ['title', 'rating', 'views']):
            top_movies_df = top_movies(df)
            st.subheader("Top 10 Movies by Rating and Views")
            st.write(top_movies_df)

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.barh(top_movies_df['title'], top_movies_df['rating'], color='skyblue')
            ax.set_xlabel("Rating")
            ax.set_ylabel("Movie Title")
            ax.set_title("Top 10 Movies by Rating")
            ax.invert_yaxis()
            st.pyplot(fig)

       
        if 'genre' in df.columns:
            plot_genre_distribution(df)

        
        if all(col in df.columns for col in ['genre', 'duration']):
            plot_average_duration_by_genre(df)

        
        if all(col in df.columns for col in ['genre', 'views']):
            plot_voting_trends_by_genre(df)

        
        if 'rating' in df.columns:
            plot_rating_distribution(df)

        
        if all(col in df.columns for col in ['genre', 'rating', 'title']):
            genre_based_rating_leaders(df)

        
        if all(col in df.columns for col in ['genre', 'views']):
            most_popular_genres_by_voting(df)

        
        if all(col in df.columns for col in ['title', 'duration']):
            duration_extremes(df)

        
        if all(col in df.columns for col in ['genre', 'rating']):
            ratings_by_genre_heatmap(df)

       
        if all(col in df.columns for col in ['rating', 'views']):
            correlation_analysis(df)

    else:
        st.error("Failed to load data from the database.")

if __name__ == "__main__":
    main()
