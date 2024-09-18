import os
import requests
from bs4 import BeautifulSoup
from smtplib import SMTP
from email.mime.text import MIMEText

# Base URL to scrape (without page numbers)
base_url = "https://www.wg-gesucht.de/wg-zimmer-und-1-zimmer-wohnungen-und-wohnungen-und-haeuser-in-Muenchen.90.0+1+2+3.1.0.html"

# Email credentials
sender_email = "l3vy.r3nt@gmail.com"
sender_password = os.getenv("SENDER_EMAIL_PASSWORD")  # Get password from environment variable
receiver_email = "al3v.ayaz@gmail.com"

def get_posts_from_page(page_url):
    try:
        response = requests.get(page_url, timeout=10)  # Add a timeout to prevent hanging
        response.raise_for_status()  # Raise an error if the request fails
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Locate posts by class or id, depending on the website structure
        posts = soup.find_all("div", class_="listings")  # Adjust as per actual structure
        post_titles = [post.text.strip() for post in posts]

        return post_titles

    except requests.exceptions.RequestException as e:
        print(f"Error while fetching posts: {e}")
        return []

def get_next_page(soup):
    """Find the 'next page' link in the pagination section."""
    next_page = soup.find("a", text="›")  # Look for the anchor with text "›" (the next arrow button)
    if next_page and "href" in next_page.attrs:
        return "https://www.wg-gesucht.de" + next_page["href"]
    return None

def check_for_new_posts():
    page_url = base_url
    all_new_posts = []

    while page_url:
        # Get posts from the current page
        new_posts = get_posts_from_page(page_url)
        if new_posts:
            all_new_posts.extend(new_posts)

        # Find the next page URL
        soup = BeautifulSoup(requests.get(page_url).text, 'html.parser')
        page_url = get_next_page(soup)  # Get the URL of the next page

        if not page_url:
            break  # No more pages

    # Read previous results
    try:
        with open("posts.txt", "r") as file:
            old_posts = file.readlines()
    except FileNotFoundError:
        old_posts = []

    # Find posts that are new
    unique_new_posts = [post for post in all_new_posts if post not in old_posts]

    if unique_new_posts:
        send_email_notification(unique_new_posts)
        # Save new posts to file
        with open("posts.txt", "w") as file:
            file.writelines(post + "\n" for post in all_new_posts)

def send_email_notification(new_posts):
    try:
        msg_content = f"New posts found:\n\n" + "\n".join(new_posts)
        msg = MIMEText(msg_content)
        msg['Subject'] = "New Rental Post Notification"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        with SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

    except Exception as e:
        print(f"Error while sending email: {e}")

if __name__ == "__main__":
    check_for_new_posts()
