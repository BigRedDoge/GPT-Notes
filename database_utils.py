import requests
import os
import dotenv

dotenv.load_dotenv()

SEARCH_TOP_K = 3


def upsert_file(directory):
    """
    Uploads all files in a directory to the database
    """
    url = "http://0.0.0.0:8000/upsert_file"
    headers = {"Authorization": "Bearer " + os.getenv("BEARER_TOKEN")}
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_path = os.path.join(directory, filename)
            with open(file_path, "rb") as f:
                file_content = f.read()
                files.append((filename, file_content, "text/plain"))

    response = requests.post(url, headers=headers, files=files, timeout=600)
    if response.status_code == 200:
        print("Successfully uploaded file: " + filename)
    else:
        print(f"Error: {response.status_code} {response.content} for uploading " + filename)

def upsert(id, content):
    """
    Uploads one piece of text to the database
    """
    url = "http://0.0.0.0:8000/upsert"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("BEARER_TOKEN")
    }

    data = {
        "documents": [{
            "id": id,
            "content": content
        }]
    }
    response = requests.post(url, headers=headers, json=data, timeout=600)
    if response.status_code == 200:
        print("Successfully uploaded text: " + content)
    else:
        print(f"Error: {response.status_code} {response.content} for uploading " + content)

def query_database(query_prompt):
    """
    Queries the vector database to retrieve chunk with user's input question
    """
    url = "http://0.0.0.0:8000/upsert"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("BEARER_TOKEN")
    }
    data = {"queries": [{"query": query_prompt, "top_k": SEARCH_TOP_K}]}

    response = requests.post(url, headers=headers, json=data, timeout=600)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise ValueError(f"Error: {response.status_code} {response.content} for query " + query_prompt)