import requests

def scrape(reddit_url):
    map = {}
    headers = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(reddit_url + "/.json", headers=headers)
    
    if r.status_code != 200:
        print(f"Error: Unable to fetch data, Status Code: {r.status_code}")
        return None

    data = r.json()  # Parse JSON data

    # Ensure 'children' exists
    children = data.get('data', {}).get('children', [])
    if not children:
        print("No posts found.")
        return None

    first_post = children[0]['data']
    title = first_post.get('title', 'No Title')
    self_text = first_post.get('selftext', 'No Description')

    map['title'] = title.strip() if title else "No Title"
    map['desc'] = self_text.strip() if self_text else "No Description"

    print("Scraped! Currently saving ...")
    return map

def scrape_llm(reddit_url):
    headers = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(reddit_url + "/.json", headers=headers)

    if r.status_code != 200:
        print(f"Error: Unable to fetch data, Status Code: {r.status_code}")
        return []

    data = r.json()  # Parse JSON data

    dist = data.get('data', {}).get('dist', 0)
    children = data.get('data', {}).get('children', [])

    if not children:
        print("No posts found.")
        return []

    fin = []
    for i in range(min(dist, len(children))):  # Ensure no index error
        post_data = children[i]['data']
        title = post_data.get('title', 'No Title')
        desc = post_data.get('selftext', 'No Description')

        fin.append([
            title.strip() if title else "No Title",
            desc.strip() if desc else "No Description"
        ])

    return fin

def save_map_to_txt(map, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Title: {map['title']}\n")
        file.write(f"Description: {map['desc']}\n")
    print("SCRAPING DONE! SUCCESSFULLY SAVED")

