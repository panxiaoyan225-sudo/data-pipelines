import os
import requests
from dotenv import load_dotenv

# 1. loading credentials securely from a .env file
# Never hardcode keys in code that goes to GitHub!
load_dotenv()

def get_api_data():
    #  fetch this via os.environ.get("MY_API_KEY")
    api_url = "https://jsonplaceholder.typicode.com/posts"
    mock_token = os.environ.get("mock_token")

    # 2.  building standard authorization headers
    headers = {
        "Authorization": f"Bearer {mock_token}",
        "Content-Type": "application/json"
    }

    try:
        # 3. Executing the Web Call with a Network Timeout :sending the request with a timeout
        #If the web server threw an error (like 404 Not Found or 500 Internal Server Error), 
        # this line immediately halts the script and throws an exception rather than passing corrupted or empty data down the line.
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # 4. The Validation Gatekeeper :robust error handling (raises an HTTPError if status is 4xx or 5xx)
        response.raise_for_status()
        
        # Parse the JSON response:Turning Raw Payload into Python Data
        # Parse the response content as JSON and assign it to the variable 'data'
        data = response.json()
        #the data is stored in your computer's temporary volatile memory (RAM), specifically inside a Python variable named data.
 
        print(f"✅ Success! Successfully retrieved {len(data)} records.")
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"❌ Connection error occurred: {conn_err}")
    except Exception as err:
        print(f"❌ An unexpected error occurred: {err}")

if __name__ == "__main__":
    print("🏃‍♂️ Running standalone test for api_pipeline.py...")
    
    # Call the function ONCE and save its output to 'data'
    data = get_api_data()
    
    if data:
        print("\n📋 First 10 rows of data:")
        for row in data[:10]:
            print(row)
