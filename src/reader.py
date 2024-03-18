import mailbox
from email import message_from_string
from bs4 import BeautifulSoup
import re
# Path to your .mbox file


def extract_messages():
    mbox_file = '../Takeout/Mail/Category Promotions.mbox'

    # Open the .mbox file
    mbox = mailbox.mbox(mbox_file)
    # Iterate over each email in the .mbox file

    message_list = []
    counter = 0
    for message in mbox:
        # Convert the email message to a string
        if counter >= 1000:
            return message_list
        counter += 1
        subject = message['subject']
        sender = message['from']
        date = message['date']

        # print(f"Subject: {subject}")
        # print(f"From: {sender}")
        # print(f"Date: {date}")

        message_str = message.as_string()
        
        # Parse the email message
        parsed_message = message_from_string(message_str)
        
        # Extract the HTML body
        html_body = None
        for part in parsed_message.walk():
            if part.get_content_type() == 'text/html':
                html_body = part.get_payload(decode=True)
                charset = part.get_content_charset()  # Get the charset
                if charset is not None:
                    html_body = html_body.decode(charset)
                else:
                    # If charset is None, use a default charset                    
                    print("continue Nothing")  # You can choose any default charset or handle it based on your preference
                    continue
                break          
        
        # If HTML body exists, extract text content
        if html_body:
            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(html_body, 'html.parser')
            text_content = soup.get_text()
        
            text_content = re.sub(r'\n+', ' ', text_content)
            # text_content = '\n'.join([line.lstrip() for line in text_content.split('\n')])
            # text_content = re.sub(r'\n+', ' ', text_content)
            text_content = '\n'.join([line.lstrip() for line in text_content.split('\n')])
            final_text = f'Received From: {sender}\nReceived Timestamp: {date}\nEmail Body: \n{text_content}'
            message_list.append(final_text)
            print(f'processed: {counter} / {len(mbox)}')
            
    return message_list