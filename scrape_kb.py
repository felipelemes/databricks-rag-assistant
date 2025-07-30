import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin
import json

# --- Configurations ---
BASE_URL = "https://kb.databricks.com"
START_URL = "https://kb.databricks.com/en_US/azure" # URL of the main listing page
OUTPUT_DIR = "scraped_kb_articles" # Folder to save extracted articles (in JSON format)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
}

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_page_content(url, delay=1):
    """Function to fetch HTML content from a URL with error handling and delay."""
    print(f"Fetching: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=30) # Increased timeout to 30s
        response.raise_for_status() # Raises an HTTPError for bad status codes (4xx or 5xx)
        time.sleep(delay) # Pause to be polite to the website server
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

def parse_listing_page(html_content):
    """
    Function to parse the listing page and extract links and titles of ALL articles.
    Returns a list of dictionaries: [{'title': '...', 'url': '...'}]
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    articles_data = []

    # Find all article containers on the main page
    # The selector is 'div.row[data-helpjuice-element="SubCategory Article"]'
    # meaning: div that has class 'row' AND attribute 'data-helpjuice-element' equal to "SubCategory Article"
    article_containers = soup.find_all('div', class_='row', attrs={'data-helpjuice-element': 'SubCategory Article'})

    if not article_containers:
        print("Warning: No article containers found on the listing page with the specified selector.")
        print("This might indicate that the HTML has changed or content is loaded dynamically via JavaScript.")
        return articles_data

    for container in article_containers:
        # Try to find the main article link (the first <a> inside the container)
        link_tag = container.find('a', href=True)
        if link_tag:
            relative_url = link_tag['href']
            full_url = urljoin(BASE_URL, relative_url) # Constructs the full URL

            # Try to find the article title (h3 inside the link)
            title_tag = container.find('h3', attrs={'data-helpjuice-element': 'SubCategory Article Title'})
            title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"

            # Add article data to the list
            articles_data.append({'title': title, 'url': full_url})
        else:
            print(f"Warning: Article container with no valid main link found: {container.prettify()[:200]}...")

    return articles_data

def scrape_article_content(article_url):
    """
    Function to fetch the content of an individual article page, using the validated selector.
    Returns a dictionary with 'url', 'title', and 'content'.
    """
    html_content = fetch_page_content(article_url, delay=2) # Pause a bit more for individual article content
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title (Main article question/title)
    # Validated for h1 with class article-title
    title_tag = soup.find('h1', class_='article-title')
    title = title_tag.get_text(strip=True) if title_tag else "Unknown Article Title"

    # Extract article body (Answer/Main content)
    # Validated for div with class 'helpjuice-article-body-content'
    body_content_div = soup.find('div', class_='helpjuice-article-body-content')
    content = ""
    if body_content_div:
        # Extracts all text within this div, using '\n' to separate blocks and strip whitespace
        content = body_content_div.get_text(separator='\n', strip=True)
    else:
        print(f"Warning: Article body with class 'helpjuice-article-body-content' NOT found for {article_url}")
        print("This might be a JavaScript loading issue or a different HTML structure for this article.")

    return {'url': article_url, 'title': title, 'content': content}

# --- Main Scraping Logic ---
if __name__ == "__main__":
    print(f"Starting scraping process from: {START_URL}")

    # 1. Fetch HTML from the main listing page
    list_page_html = fetch_page_content(START_URL, delay=3) # Increased pause for the main page

    all_article_links = []
    if list_page_html:
        # 2. Parse the listing page and collect ALL article links
        articles_on_main_page = parse_listing_page(list_page_html)
        all_article_links.extend(articles_on_main_page)
        print(f"Total of {len(all_article_links)} article links collected from the main page.")
    else:
        print("Could not proceed, error fetching the initial listing page.")
        exit() # Stop the script if the initial page cannot be accessed

    scraped_articles_data = []
    # 3. Iterate over each article link and scrape the full content
    for i, article_link_info in enumerate(all_article_links):
        print(f"Scraping article {i+1}/{len(all_article_links)}: {article_link_info['title']}")
        
        # Check if the JSON file for this article already exists
        file_name_hash = article_link_info['url'].split('/')[-1] # Base filename from URL
        output_filepath = os.path.join(OUTPUT_DIR, f"{file_name_hash}.json")
        
        if os.path.exists(output_filepath):
            print(f"  Article already scraped and saved: {output_filepath}. Skipping.")
            try: # Try to load to include in total if it exists
                with open(output_filepath, 'r', encoding='utf-8') as f:
                    scraped_articles_data.append(json.load(f))
            except Exception as e:
                print(f"  Error loading existing file {output_filepath}: {e}")
            continue # Skip to the next article

        article_content = scrape_article_content(article_link_info['url'])
        if article_content:
            scraped_articles_data.append(article_content)
            # Save the content as JSON in a file for reference and debugging
            try:
                with open(output_filepath, 'w', encoding='utf-8') as f:
                    json.dump(article_content, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"  Error saving JSON file {output_filepath}: {e}")

    print(f"\nScraping of {len(scraped_articles_data)} articles completed and saved/loaded from '{OUTPUT_DIR}'.")

    print("\n--- Next Steps ---")
    print("1. Knowledge Base articles scraped and saved as JSONs in the 'scraped_kb_articles' folder.")
    print("2. Now, run the 'update_vector_db_with_kb.py' script to integrate this data into your FAISS vector database.")
    print("   `python update_vector_db_with_kb.py`")