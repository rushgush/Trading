import os
import requests
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

def test_congress_connection():
    """
    Test connection to the Congress trading endpoint
    """
    # Get the authorization token
    auth_token = os.getenv('AUTHORISATION_TOKEN')
    if not auth_token:
        print("Error: No authorization token found in .env file")
        return

    # API configuration
    base_url = "https://api.quiverquant.com/beta"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    # Test endpoint
    endpoint = f"{base_url}/live/congresstrading"
    
    try:
        # Make the request with detailed debug information
        print(f"Making request to: {endpoint}")
        print("Headers:", headers)
        
        response = requests.get(endpoint, headers=headers)
        
        # Print response status and headers for debugging
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        
        # Check if we got any data
        if not data:
            print("Warning: Received empty response")
            return
            
        # Print the first record to understand the structure
        print("\nFirst record in response:")
        print(data[0])
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Print basic information about the data
        print("\nDataFrame Info:")
        print(df.info())
        
        # Print available columns
        print("\nAvailable columns:")
        print(df.columns.tolist())
        
        # Print first few rows
        print("\nFirst few rows of data:")
        print(df.head())
        
        return df

    except requests.exceptions.RequestException as e:
        print(f"\nError making request:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response Status Code: {e.response.status_code}")
            print(f"Response Text: {e.response.text}")
        return None

if __name__ == "__main__":
    print("Testing Congress Trading API Connection...")
    result = test_congress_connection()
    
    if result is not None:
        print("\nConnection test successful!")
        print(f"Retrieved {len(result)} records")
    else:
        print("\nConnection test failed!")