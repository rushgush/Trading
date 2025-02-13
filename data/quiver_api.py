"""
Quiver Quantitative API client for fetching trading signals data.
"""
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class QuiverAPI:
    """
    Client for interacting with Quiver Quantitative API endpoints.
    Handles data fetching for congress trading, WSB sentiment, insider trading, and other signals.
    """
    
    def __init__(self):
        """Initialize the API client with configuration."""
        self.auth_token = os.getenv('AUTHORISATION_TOKEN')
        self.base_url = 'https://api.quiverquant.com/beta'
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.auth_token}'
        }

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Make a request to the Quiver API with error handling.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters for the request
            
        Returns:
            pandas DataFrame with the response data
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params)
            
            # Log request details for debugging
            print(f"Request URL: {url}")
            print(f"Response Status: {response.status_code}")
            
            response.raise_for_status()
            data = response.json()
            
            if not data:
                print(f"Warning: No data received from endpoint {endpoint}")
                return pd.DataFrame()
                
            return pd.DataFrame(data)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {endpoint}: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Error details: {e.response.text}")
            return pd.DataFrame()

    # Congress Trading Methods
    def get_congress_trading_live(self, page: int = 1, page_size: int = 100) -> pd.DataFrame:
        """Get most recent congress trading data."""
        return self._make_request('live/congresstrading', {
            'page': page,
            'page_size': page_size
        })

    def get_historical_congress_trading(self, ticker: str) -> pd.DataFrame:
        """Get historical congress trading data for a specific ticker."""
        return self._make_request(f'historical/congresstrading/{ticker}')

    def get_congress_trading_bulk(self, page: int = 1, page_size: int = 100) -> pd.DataFrame:
        """Get bulk congress trading data."""
        return self._make_request('bulk/congresstrading', {
            'page': page,
            'page_size': page_size
        })

    # WallStreetBets Methods
    def get_wallstreetbets_live(self, count_all: bool = True) -> pd.DataFrame:
        """Get live WallStreetBets sentiment data."""
        return self._make_request('live/wallstreetbets', {
            'count_all': count_all
        })

    def get_historical_wallstreetbets(self, ticker: str) -> pd.DataFrame:
        """Get historical WallStreetBets data for a specific ticker."""
        return self._make_request(f'historical/wallstreetbets/{ticker}')

    def get_wallstreetbets_trending(self) -> pd.DataFrame:
        """Get trending stocks on WallStreetBets."""
        df = self.get_wallstreetbets_live()
        if not df.empty:
            return df.nlargest(10, 'Mentions')
        return df

    # Government Contracts Methods
    def get_government_contracts_live(self) -> pd.DataFrame:
        """Get recent government contracts data."""
        return self._make_request('live/govcontracts')

    def get_historical_government_contracts(self, ticker: str) -> pd.DataFrame:
        """Get historical government contracts for a specific ticker."""
        return self._make_request(f'historical/govcontracts/{ticker}')

    # Dark Pool / Off-Exchange Trading Methods
    def get_off_exchange_live(self) -> pd.DataFrame:
        """Get recent off-exchange trading data."""
        return self._make_request('live/offexchange')

    def get_historical_off_exchange(self, ticker: str) -> pd.DataFrame:
        """Get historical off-exchange data for a specific ticker."""
        return self._make_request(f'historical/offexchange/{ticker}')

    # Lobbying Data Methods
    def get_lobbying_live(self, page: int = 1, page_size: int = 100) -> pd.DataFrame:
        """Get recent lobbying data."""
        return self._make_request('live/lobbying', {
            'page': page,
            'page_size': page_size
        })

    def get_historical_lobbying(self, ticker: str) -> pd.DataFrame:
        """Get historical lobbying data for a specific ticker."""
        return self._make_request(f'historical/lobbying/{ticker}')

    # Political Beta Methods
    def get_political_beta_live(self) -> pd.DataFrame:
        """Get current political beta values."""
        return self._make_request('live/politicalbeta')

    def get_historical_political_beta(self, ticker: str) -> pd.DataFrame:
        """Get historical political beta for a specific ticker."""
        return self._make_request(f'historical/politicalbeta/{ticker}')

    def test_connection(self) -> bool:
        """
        Test the API connection and authentication.
        Returns True if connection is successful.
        """
        try:
            # Try to fetch a small amount of congress data as a test
            test_data = self.get_congress_trading_live(page_size=1)
            return not test_data.empty
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False

    def get_composite_data(self, ticker: str) -> Dict[str, pd.DataFrame]:
        """
        Get all relevant data for a specific ticker.
        Returns a dictionary containing all data sources.
        """
        return {
            'congress': self.get_historical_congress_trading(ticker),
            'wsb': self.get_historical_wallstreetbets(ticker),
            'govcontracts': self.get_historical_government_contracts(ticker),
            'lobbying': self.get_historical_lobbying(ticker),
            'offexchange': self.get_historical_off_exchange(ticker),
            'political_beta': self.get_historical_political_beta(ticker)
        }

def main():
    # Initialize the API client
    api_client = QuiverAPI()
    
    # Test the connection
    if api_client.test_connection():
        print("Connection successful!")
        
        # Fetch live congress trading data
        congress_data = api_client.get_congress_trading_live()
        print(congress_data)
    else:
        print("Connection failed!")

if __name__ == "__main__":
    main()