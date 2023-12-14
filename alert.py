from themes import subset_df
import smtplib
from email.message import EmailMessage

def send_email_alert(tweet, viral,theme, sender_email, app_password, receiver_email):
    msg = EmailMessage()
    msg.set_content(f"ALERT: This tweet is predicted to go viral!\nTweet: {tweet}\nPredicted Viral: {viral}\nTheme: {theme}")

    msg['Subject'] = 'Viral Tweet Alert'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Use starttls() for TLS encryption

        # Use the App Password to login
        server.login(sender_email, app_password)

        # Send the email
        server.send_message(msg)

# Set up your email credentials
sender_email = "productstudio.myriant@gmail.com"
app_password = "hxbppxidmrflpnfn"  # Replace with your actual App Password
receiver_email = "marcosanchez1166@gmail.com"

VIRAL_THRESHOLD = 10

for index, row in subset_df.iterrows():
    if row['virality_score'] > VIRAL_THRESHOLD:
        tweet = row['tweets']
        viral = row['predicted_viral']
        theme = row['theme']
        send_email_alert(tweet, viral, theme, sender_email, app_password, receiver_email)