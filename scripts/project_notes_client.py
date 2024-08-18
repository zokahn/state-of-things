"""
This module provides client functions to interact with the Project Notes API.
"""

import requests

BASE_URL = "http://localhost:8000"  # Adjust this if your API is hosted elsewhere

def create_project(name: str, description: str) -> dict:
    """
    Create a new project.

    Args:
        name (str): The name of the project.
        description (str): The description of the project.

    Returns:
        dict: The created project data.
    """
    response = requests.post(
        f"{BASE_URL}/projects/",
        json={"name": name, "description": description}
    )
    return response.json()

def list_projects() -> list:
    """
    List all projects.

    Returns:
        list: A list of all projects.
    """
    response = requests.get(f"{BASE_URL}/projects/")
    return response.json()

# Add other functions as needed
