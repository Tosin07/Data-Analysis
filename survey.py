import pandas as pd

survey_df = pd.read_csv("survey.csv")

print(survey_df)

#mock analysis

avg_rating = survey_df["Rating"].mean()
rating_by_city = survey_df.groupby("City")["Rating"].mean()
gender_distribution = survey_df["Gender"].value_counts()

print(f"Average Rating: {avg_rating}")

# print(f"Rating By City: {rating_by_city}")
print("Rating By City:\n", rating_by_city)
print("Gender Distribution:\n", gender_distribution)