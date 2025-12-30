import os
import re
import streamlit as st

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Trim leading and trailing whitespace
    text = text.strip()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

# Scraping Helper
def scrape_page_content(url):
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for element in soup(["script", "style", "nav", "footer", "header", "form"]):
            element.decompose()
            
        text = soup.get_text(separator=' ')
        cleaned = clean_text(text)
        
        if len(cleaned) < 500:
            return None
            
        return cleaned
    except Exception as e:
        print(f"Scraping Error for {url}: {e}")
        return None

def process_institution_url(chain, url):
    cleaned = scrape_page_content(url)
    if cleaned:
        return chain.summarize_institution(cleaned[:10000]) 
    return None

# Resource Caching for Performance and Startup
# @st.cache_resource
def get_chain(api_key=None):
    """Refreshed version 1.0.1"""
    try:
        from chains import Chain
        key = api_key or os.getenv("GROQ_API_KEY")
        # Force reload of the module if needed, but usually creating a new instance is enough if the file changed
        import importlib
        import chains
        importlib.reload(chains)
        from chains import Chain
        return Chain(api_key=key)
    except Exception as e:
        st.error(f"Error initializing Chain: {e}")
        return None
    
# @st.cache_resource
def get_portfolio():
    try:
        from portfolio import Portfolio
        return Portfolio()
    except Exception as e:
        st.error(f"Error initializing Portfolio: {e}")
        return None