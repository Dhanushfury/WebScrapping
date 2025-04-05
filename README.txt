# IMDb Movie Scraper (2024)

This Jupyter Notebook automates the process of scraping **IMDb's top-rated movies of 2024** by genre using **Selenium**, saving each genre's data as a CSV file, merging them into a single dataset, and uploading the final data to a **MySQL database**.

## Features

- Scrapes movies from IMDb by genre:
  - Action
  - Adventure
  - Animation
  - Comedy
  - Crime

- Captures movie details:
  - Title
  - Rating
  - Views
  - Duration
  - Genre

- Saves each genre to a separate CSV file
- Merges all CSVs into one DataFrame
- Uploads merged data into a MySQL database table

##Tech Stack

- Python 3
- Selenium
- Pandas
- MySQL Connector
- Jupyter Notebook


IMDb Movie Dashboard (Streamlit + MySQL)

##Features:

Filter movies by genre, duration, rating, and views

##Visualizations:

Top-rated movies
Genre distribution
Average movie duration by genre
Voting trends by genre
Rating distribution
Heatmap of average ratings per genre
Most popular genres (pie chart)
Correlation: Ratings vs Voting Count
Identify the shortest and longest movies
Find the top-rated movie in each genre


##Tech Stack

Python
Streamlit – Web App Framework
Pandas – Data Processing
Matplotlib / Seaborn – Data Visualization
MySQL Connector – Database Access

##MySQL command line

# Step 1-create the database named "Scrapping" in Mysql 8.0 Command line client
# Step 2-create table named "Imdbmovies" with the columns given bellow:
# CREATE TABLE Imdbmovies(Title VARCHAR(255),Rating FLOAT,Views INT,Duration INT,Genre VARCHAR(255));