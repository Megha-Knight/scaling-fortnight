import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector # For database connection (you can use other DBs like MySQL or PostgreSQL)

# Function to fetch email data from the database
def fetch_email_data(db_path):
    try:
        # Connect to the SQLite database
        conn = mysql.connector.connect(db_path)
        cursor = conn.cursor()

        # Fetch email details
        query = "SELECT email FROM user "
        cursor.execute(query)
        email_data = cursor.fetchall()

        conn.close()
        return email_data
    except Exception as e:
        print(f"Error fetching data from database: {e}")
        return []

# Function to send email
def send_email(sender_email, sender_password, recipient_email):
    try:
        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = "Your Order is Confirmed!"

        # Add body to the email
        message.attach(MIMEText("You have purchased {pdt_name} from IDEA LAb for RS.{price}".format(pdt_name="Tshirt", price=900), 'plain'))

        # Connect to the Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade to secure connection
            server.login(sender_email, sender_password)  # Login to the email account

            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent successfully to {recipient_email}")

    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

# Main function
if __name__ == "__main__":
    # Database path
    db_path = "lab"  # Replace with your actual database path

    # Sender credentials
    sender_email = "arunprakashcoc.com"
    sender_password = "ztce dgaw mofi qyky"  # Use App Password for Gmail

    # Fetch email data from the database
    email_data = fetch_email_data(db_path)

    # Send emails dynamically
    for recipient_email in email_data:
        send_email(sender_email, sender_password, recipient_email)
