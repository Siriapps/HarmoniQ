import requests
import json
import re
from collections import Counter

url = "https://api.parse.bot/scraper/79c49ea3-efb5-435d-af9f-83779b815a00/extract_network_feedback"

# List of telecom subreddits to analyze
# Try alternative names for AT&T and Verizon
subreddits = ["ATT"]

headers = {
    "Content-Type": "application/json",
    "X-API-Key": "3f32bd8e-4cb8-48bf-9ed8-8a2fc249b122"
}

# US States and abbreviations for location extraction
US_STATES = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

def extract_locations(text):
    """Extract location mentions from text"""
    locations = []
    text_upper = text.upper()
    
    # Check for state names and abbreviations
    for state, abbr in US_STATES.items():
        # Check for full state name (case insensitive)
        if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
            locations.append(state)
        # Check for state abbreviation
        elif re.search(r'\b' + abbr + r'\b', text_upper):
            locations.append(state)
    
    # Check for city patterns (city, state)
    city_state_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z]{2})\b'
    city_matches = re.findall(city_state_pattern, text)
    for city, state_abbr in city_matches:
        for state, abbr in US_STATES.items():
            if abbr == state_abbr:
                locations.append(f"{city}, {state}")
                break
    
    return list(set(locations))  # Remove duplicates

all_results = {}
location_mentions = Counter()

# Loop through each subreddit
for subreddit in subreddits:
    print(f"\n{'='*60}")
    print(f"Fetching data from r/{subreddit}...")
    print('='*60)
    
    payload = {
        "subreddit": subreddit,
        "post_limit": 10,
        "comment_limit": 5,
        "time_range": "all",
        "keyword_filter": ""
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        all_results[subreddit] = data
        
        # Extract locations from posts and comments
        subreddit_locations = []
        
        # Extract from post titles
        for post in data.get('post_summaries', []):
            post_locations = extract_locations(post.get('title', ''))
            subreddit_locations.extend(post_locations)
        
        # Extract from feedback posts
        for feedback in data.get('feedback', []):
            feedback_locations = extract_locations(feedback.get('content', ''))
            subreddit_locations.extend(feedback_locations)
        
        # Extract from sentiment results (comments)
        for result in data.get('sentiment', {}).get('results', []):
            comment_locations = extract_locations(result.get('text', ''))
            subreddit_locations.extend(comment_locations)
        
        # Count location mentions
        for loc in subreddit_locations:
            location_mentions[loc] += 1
        
        # Add location data to results
        location_counter = Counter(subreddit_locations)
        data['location_mentions'] = dict(location_counter)
        data['total_location_mentions'] = len(subreddit_locations)
        
        # Print summary for this subreddit
        print(f"\nSubreddit: r/{subreddit}")
        print(f"Posts Considered: {data.get('posts_considered', 0)}")
        print(f"Total Comments: {data.get('aggregated_comment_count', 0)}")
        print(f"Location Mentions Found: {len(subreddit_locations)}")
        
        if location_counter:
            print(f"\nTop Locations Mentioned:")
            for location, count in location_counter.most_common(5):
                print(f"  {location}: {count}")
        
        sentiment = data.get('sentiment', {})
        print(f"\nSentiment Analysis:")
        print(f"  Positive: {sentiment.get('positive', 0)} ({sentiment.get('positive', 0) / max(sentiment.get('count', 1), 1) * 100:.1f}%)")
        print(f"  Neutral: {sentiment.get('neutral', 0)} ({sentiment.get('neutral', 0) / max(sentiment.get('count', 1), 1) * 100:.1f}%)")
        print(f"  Negative: {sentiment.get('negative', 0)} ({sentiment.get('negative', 0) / max(sentiment.get('count', 1), 1) * 100:.1f}%)")
        
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        all_results[subreddit] = {"error": response.status_code, "message": response.text}

# Print overall summary
print(f"\n\n{'='*60}")
print("OVERALL SUMMARY")
print('='*60)

for subreddit, data in all_results.items():
    if "error" not in data:
        sentiment = data.get('sentiment', {})
        total = sentiment.get('count', 0)
        print(f"\nr/{subreddit}:")
        print(f"  Total Comments: {total}")
        if total > 0:
            print(f"  Positive: {sentiment.get('positive', 0)} ({sentiment.get('positive', 0) / total * 100:.1f}%)")
            print(f"  Neutral: {sentiment.get('neutral', 0)} ({sentiment.get('neutral', 0) / total * 100:.1f}%)")
            print(f"  Negative: {sentiment.get('negative', 0)} ({sentiment.get('negative', 0) / total * 100:.1f}%)")
    else:
        print(f"\nr/{subreddit}: Error - {data.get('message', 'Unknown error')}")

# Print location summary
if location_mentions:
    print(f"\n\n{'='*60}")
    print("LOCATION ANALYSIS - ALL SUBREDDITS")
    print('='*60)
    print(f"\nTop 10 Most Mentioned Locations:")
    for location, count in location_mentions.most_common(10):
        print(f"  {location}: {count} mentions")

# Save detailed results to JSON file
with open('telecom_sentiment_results.json', 'w') as f:
    json.dump(all_results, f, indent=2)

# Save location data separately
location_data = {
    'total_locations_found': len(location_mentions),
    'location_breakdown': dict(location_mentions.most_common()),
    'by_subreddit': {
        subreddit: data.get('location_mentions', {}) 
        for subreddit, data in all_results.items() 
        if 'error' not in data
    }
}

with open('location_analysis.json', 'w') as f:
    json.dump(location_data, f, indent=2)
    
print(f"\n\nDetailed results saved to 'telecom_sentiment_results.json'")
print(f"Location analysis saved to 'location_analysis.json'")
