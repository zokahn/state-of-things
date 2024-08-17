
import requests

BASE_URL = "http://localhost:8000"  # Adjust this if your API is hosted elsewhere

def create_project(name, description):
    response = requests.post(f"{BASE_URL}/projects/", json={"name": name, "description": description})
    return response.json()

def list_projects():
    response = requests.get(f"{BASE_URL}/projects/")
    return response.json()

# Add other functions as needed
