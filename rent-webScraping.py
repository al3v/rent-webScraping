import requests
from bs4 import BeautifulSoup
import time
from smtplib import SMTP
from email.mime.text import MIMEText

# URL to scrape
url = "https://www.wg-gesucht.de/wg-zimmer-und-1-zimmer-wohnungen-und-wohnungen-und-haeuser-in-Muenchen.90.0+1+2+3.1.0.html?offer_filter=1&city_id=90&sort_order=0&noDeact=1&categories%5B%5D=0&categories%5B%5D=1&categories%5B%5D=2&categories%5B%5D=3&rent_types%5B%5D=2&rMax=530&wgSea=1"

# Email credentials
sender_email = "l3vy.r3nt@gmail.com"
sender_password = "iqkdwmllkqmnifpg"
receiver_email = "al3v.ayaz@gmail.com"

def check_for_new_posts():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Locate posts by class or id, depending on the website structure
    posts = soup.find_all("div", class_="listings")  # adjust as per actual structure
    post_titles = [post.text.strip() for post in posts]

    # Read previous results
    try:
        with open("posts.txt", "r") as file:
            old_posts = file.readlines()
    except FileNotFoundError:
        old_posts = []

    new_posts = [post for post in post_titles if post not in old_posts]

    if new_posts:
        send_email_notification(new_posts)
        # Save new posts to file
        with open("posts.txt", "w") as file:
            file.writelines(post + "\n" for post in post_titles)

def send_email_notification(new_posts):
    msg_content = f"New posts found:\n\n" + "\n".join(new_posts)
    msg = MIMEText(msg_content)
    msg['Subject'] = "New Rental Post Notification"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

if __name__ == "__main__":
    while True:
        check_for_new_posts()
        time.sleep(1800)  # Check every hour
