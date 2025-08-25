from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

survey_df = pd.read_csv("survey.csv")
gender_distribution = survey_df["Gender"].value_counts().to_dict()
avg = round(survey_df["Rating"].mean(), 2)
avg_rating = {"average_rating": avg}

@app.get("/")
def home():
    return {"message" : "Survey Analysis API"}

@app.get("/average-rating")
def get_avg_rating():
    return avg_rating

@app.get("/rating-by-city")
def get_rating_by_city () :
    return survey_df.groupby("City")["Rating"].mean().to_dict()

@app.get("/gender-distribution")
def get_gender_distribution(): 
    return gender_distribution

class SurveyResponse(BaseModel):
    name: str
    age: int
    gender: str
    city: str
    rating: int
    comment: str
    
try:
    survey_df = pd.read_csv("survey.csv")
except FileNotFoundError:
    survey_df = pd.DataFrame(columns=["Name", "Age", "Gender", "City", "Rating", "Comment"])
    
@app.post("/add-response")
def add_response(response: SurveyResponse):
    global survey_df
    new_row = {
        "Name": response.name,
        "Age": response.age,
        "Gender": response.gender,
        "City": response.city,
        "Rating": response.rating,
        "Comment": response.comment,
    }
    survey_df = pd.concat([survey_df, pd.DataFrame([new_row])], ignore_index = True)
    survey_df.to_csv('survey.csv', index=False)
    return {"message": "Response added successfully"}