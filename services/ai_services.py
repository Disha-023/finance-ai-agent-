import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Updated Gemini Model
model = genai.GenerativeModel("gemini-3.5-flash-lite")


def generate_stock_analysis(prompt):

    response = model.generate_content(prompt)

    return response.text