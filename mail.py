import json
import imaplib, email
from email.header import decode_header
import os
import webbrowser

def obtain_header(msg):
    # decode the email subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding)
 
    # decode email sender
    From, encoding = decode_header(msg.get("From"))[0]
    if isinstance(From, bytes):
        From = From.decode(encoding)
 
    print("Subject:", subject)
    print("From:", From)
    return subject, From


class Mail():
    def __init__(self, username, password, server):
        self.username = username
        self.password = password
        self.server = server
        self.imap = imaplib.IMAP4_SSL(self.server)
        self.imap.login(self.username, self.password)

    def get_mails(self):
        mails = []

        status, messages = self.imap.select("INBOX")
        numOfMessages = int(messages[0])
        print(numOfMessages)

        res,msg = self.imap.fetch(str(2), "(RFC822)")  # fetches email using ID
 
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                obtain_header(msg)
                if msg.is_multipart():
                    pass
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
     
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
     
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            mails.append(body)
                else:       
                    content_type = msg.get_content_type()
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        print(body)

        return mails

