import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display


pd.set_option("display.max_colwidth", 200)
pd.set_option('display.max_columns', 50)

df = pd.read_csv("netflix_titles.csv")

print("Shape (rows, cols):", df.shape)
print("\nInfo:", df.info())
print("\nDescribe:", df.describe())

#Data preparation and cleaning
missing_count = df.isna().sum()
missing_percentage = (df.isna().sum()/len(df)) * 100
missing_summary = (
    pd.DataFrame({"missing_count" : missing_count , "missing_percentage": missing_percentage}).sort_values(by="missing_count", ascending=False)
)
# missing_summary = df.isna().sum().sort_values(ascending=False)
# print(pd.DataFrame({"missing_count": missing_summary}))
dupe_count = df.duplicated().sum()
print("Total duplicates:", dupe_count)
# display(missing_summary.to_frame("missing_count"))
print(missing_summary)


#The dataset contains missing values, especially in the director, country, and cast field, while germane columns like show_id, title, and release year indicate non-missing values. 

#unique values for object fields

unique_counts = df.select_dtypes(include=['object']).nunique().sort_values(ascending=False)
display(unique_counts.to_frame("n_unique"))

#The unique counts verifies that columns like show_id, title, description have a unique distinctness to them, while categorical labels such as type and rating have quite a limited distinction. This translates to a wide variety of films, but very few standard categories

df = df.copy()

# 1) Strip whitespace in all string columns
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].astype(str).str.strip().replace({'nan': np.nan})

#Removed extra spaces from the string column and replaced every nan strings into regular NaN values, allowing consistency in my dataset and eliminating errors in my aggregrate functions.

df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

#Parsed the date_added column into a standard datetime format so a time-based analysis can be conducted. Extracting both year_added and month_added allows helps me understand trends over 
#time, such as how Netflix adds content with respect to time or seasons

def parse_duration(x):
    if pd.isna(x):
        return np.nan, np.nan
    parts = str(x).split()
    if len(parts) >= 2:
        try:
            val = int(parts[0])
        except:
            val = np.nan
        typ = parts[1].lower()
        # normalize types
        if "min" in typ:
            typ = "min"
        elif "season" in typ:
            typ = "season"
        return val, typ
    return np.nan, np.nan

d_parsed = df['duration'].apply(parse_duration)
df['duration_int'] = d_parsed.apply(lambda t: t[0])
df['duration_type'] = d_parsed.apply(lambda t: t[1])

#Here, I am splitting the duration column into two parts: a numeric value (duration_int) and a category (duration_type). Example: "90 min" → (90, "min"), "2 Seasons" → (2, "season"). This makes it easier to analyse movies (in minutes) and TV shows (in seasons) separately.

#OR
# def parse_duration(x):
#     if pd.isna(x):
#         return pd.Series([np.nan, np.nan], index=["duration_int", "duration_type"])
#     parts = str(x).split()
#     if len(parts) >= 2:
#         try:
#             val = parts[0]
#         except:
#             val = np.nan
#         type = parts[1].lower()
#         if "min" in type:
#             type = "min"
#         elif "seasons" in type:
#             type = "seasons"
#         return pd.Series([val, type], index=["duration_int", "duration_type"])
#     return pd.Series([np.nan, np.nan], index=["duration_int", "duration_type"])
# df[["duration_int", "duration_type"]] = df["duration"].apply(parse_duration)

def get_main_genre(x):
    if isinstance(x, str):
        return x.split(',')[0]
    
df['main_genre'] = df['listed_in'].apply(get_main_genre)

def count_genres(x):
    if isinstance(x, str):
        y = x.split(',')
        for i in y:
            i.strip()
        return len(y)
    return 0

df["n_genres"] = df['listed_in'].apply(count_genres)

#I parsed the listed_in column to extract a primary (main) genre and count the total number of genres per title. This makes it easier to analyze content by genre distribution and measure how diverse each title is in terms of categories.

df['country'] = df['country'].replace(np.nan, 'None')
def get_countries(x):
    if isinstance(x, str):
        y = x.split(',')
        for i in y:
            i.strip()
        return len(y)
    return 0
df["n_country"] = df['country'].apply(get_countries)
#Parsed the country column to handle multiple entries listed in one row by splitting on comma and creating a new column to display that. This helps in understanding the geographical diversity of content, and also, films that might have involved a co-production

# print(df[df["n_country"] == 2])
# print(df.loc[df["n_country"] == 2, "title"])

rating_map = {
    'UR':'NR', 'NR':'NR', 'NA':'NR', 'UNRATED':'NR', 'NOT RATED':'NR'
}
df['rating_clean'] = df['rating'].astype(str).str.upper().replace(rating_map)
#Rating values are normalized to reduce duplicates caused by inconsistent labels (e.g., 'UR', 'Unrated', 'Not Rated') so that all such variations map to a single category 'NR'. This ensures cleaner analysis when grouping by rating.

print("Post-cleaning shape:", df.shape)


#VISUALIZATION

num_cols = ['duration_int', 'year_added', 'month_added']
display(df.loc[:,'duration_int'])

#The descriptive stats here summarize these numeric fields(duration, year and month added). This shows that the average runtime for films or TV shows is approximately 70 minutes, most titles being added after 2018(50% of titles were added in 2019, 75% in 2020), and monthly additions saw a significant increase across the years.

#RELEASE YEAR DISTRIBUTION

plt.figure()
df['release_year'].plot(kind='hist', bins=30, title='Distribution of Release Year')
plt.xlabel('Release Year')
plt.ylabel('Frequency')
plt.show()

#Duration Distribution for movies only
plt.figure()
df.loc[df['type'] == 'Movie', 'duration_int'].dropna().plot(kind='hist', bins=30, title='Movie Duration (minutes) ')
plt.xlabel('Minutes')
plt.ylabel('Frequency')
plt.show()

#Duration distribution for TV Shows
plt.figure()
df.loc[df['type'] == 'TV Show', 'duration_int'].dropna().plot(kind='hist', bins=30, title='TV Shows Duration (seasons) ')
plt.xlabel('Seasons')
plt.ylabel('Frequency')

#The release year distribution shows that most Netflix titles are recent, with a sharp rise after 2010. Movie durations are centered around 90 minutes, while TV shows are mostly limited to 1–2 seasons. This indicates Netflix’s focus on recent content, standard-length movies, and short TV series. Probably as a strategy to keep their users engaged. 

#Relationships

type_year = df.groupby(['year_added', 'type']).size().unstack(fill_value=0)
plt.figure()
type_year.plot(kind='line', title='Titles Added per Year by Type')
plt.xlabel('Year Added')
plt.ylabel('Count')
plt.show()

avg_dur_genre = (df[df['type']=='Movie']
                 .groupby('main_genre')['duration_int']
                 .mean()
                 .sort_values(ascending=False)
                 .head(15))
plt.figure()
avg_dur_genre.plot(kind='bar', title='Avg Movie Duration by Main Genre (Top 15)')
plt.xlabel('Main Genre')
plt.ylabel('Avg Duration (min)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()