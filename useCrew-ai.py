import os
import warnings
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from openai import OpenAI

load_dotenv()
warnings.filterwarnings('ignore')

model = os.getenv("MODEL")
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
# Initialize the api client for chat completions
client = OpenAI(api_key=api_key, base_url=base_url)
