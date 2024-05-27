import json
import re
import html

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def convert_links_to_markdown(text):
    # Convert HTML links to Markdown format
    if not text:
        return text
    link_pattern = re.compile(r'<a href="(.*?)">(.*?)</a>')
    return re.sub(link_pattern, r'[\2](\1)', text)

def remove_non_ascii(text):
    return text.encode('ascii', 'ignore').decode('ascii')

def process_article(article):
    body = article.get('body', 'No Body')
    if body:
        body = convert_links_to_markdown(body)
        body_cleaned = clean_html(body).strip()
        body_cleaned = body_cleaned.replace('\n', ' ').replace('\r', '')
        body_cleaned = remove_non_ascii(body_cleaned)  # Remove non-ASCII characters
    else:
        body_cleaned = "No Body"
    return body_cleaned

def main():
    # Load JSON data
    with open('response.json', 'r') as file:
        data = json.load(file)
    
    articles = data.get('articles', [])
    
    cleaned_data = []
    for article in articles:
        body_cleaned = process_article(article)
        cleaned_data.append(body_cleaned)
    
    # Save cleaned data to a text file
    with open('cleaned_data.txt', 'w') as file:
        for body in cleaned_data:
            file.write(body + '\n\n')

if __name__ == "__main__":
    main()
