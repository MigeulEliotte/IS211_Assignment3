import argparse
import urllib.request
import csv
import re
from io import StringIO
from datetime import datetime

# Function to download the CSV log file
def download_log_file(url):
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        return data
    except Exception as e:
        print(f"Failed to download file: {e}")
        return None

# Function to process CSV data and store it in a structured format
def process_csv(data):
    log_entries = []
    csv_reader = csv.reader(StringIO(data), delimiter=',')
    
    for row in csv_reader:
        log_entries.append({
            'path': row[0],
            'datetime': row[1],
            'browser': row[2],
            'status': row[3],
            'size': row[4]
        })
    return log_entries

# Function to calculate image hits and their percentage
def calculate_image_hits(log_entries):
    image_hits = [entry for entry in log_entries if re.search(r'\.(jpg|gif|png)$', entry['path'])]
    total_hits = len(log_entries)
    image_hit_percentage = (len(image_hits) / total_hits) * 100 if total_hits > 0 else 0
    print(f"Image requests account for {image_hit_percentage:.1f}% of all requests")

# Function to find the most popular browser
def most_popular_browser(log_entries):
    browser_counts = {'Firefox': 0, 'Chrome': 0, 'Safari': 0, 'Internet Explorer': 0}
    
    for entry in log_entries:
        if 'Firefox' in entry['browser']:
            browser_counts['Firefox'] += 1
        elif 'Chrome' in entry['browser']:
            browser_counts['Chrome'] += 1
        elif 'Safari' in entry['browser']:
            browser_counts['Safari'] += 1
        elif 'MSIE' in entry['browser']:
            browser_counts['Internet Explorer'] += 1
    
    popular_browser = max(browser_counts, key=browser_counts.get)
    print(f"The most popular browser is {popular_browser}")

# Extra Credit: Function to display hits by hour
def hits_by_hour(log_entries):
    hour_counts = {hour: 0 for hour in range(24)}
    
    for entry in log_entries:
        try:
            hit_time = datetime.strptime(entry['datetime'], '%m/%d/%Y %H:%M:%S')
            hour_counts[hit_time.hour] += 1
        except Exception as e:
            print(f"Error processing datetime: {e}")
    
    for hour, count in sorted(hour_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"Hour {hour:02d} has {count} hits")

if __name__ == "__main__":
    # Set up argument parsing for URL input
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, default="http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv", help='URL of the web log file')
    args = parser.parse_args()

    # Download and process the log file
    log_data = download_log_file(args.url)
    
    if log_data:  # Proceed only if file was successfully downloaded
        log_entries = process_csv(log_data)

        # Part III: Calculate image hits
        calculate_image_hits(log_entries)

        # Part IV: Find the most popular browser
        most_popular_browser(log_entries)

        # Extra Credit: Display hits by hour
        hits_by_hour(log_entries)
