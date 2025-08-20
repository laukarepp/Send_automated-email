#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---
# @author  Laura Karina Eppens
# @date    2024-06-15
# @version 1.0
# @brief   This script automates the process of sending emails using SMTP.
# ---

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os

# --- USER eMAIL CONFIGURATION ---

# User email address
user=input("Enter your email address: ")
# User email password
pwd=input("Enter your email password: ")

# Recipient email address 
destination=input("Enter the recipient's email address: ")
# Subject of the email
subj=input("Enter the subject of the email: ")
# Check if the subject is empty, if so, set a default subject
if subj.strip() == "":
    subject = "AVISO"
else:
    subject = subj
# If the subject is not empty, use the provided subject


# --- SMTP CONFIGURATION ---
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login('user', 'pwd')

#Chek if the image file exists
image_path=print("Enter the path of the image to attach: ")
img_path=input(image_path)
img=os.path.basename(img_path)
if os.path.isfile(img_path):
    with open(img_path, 'rb') as img_file:
        img_data = img_file.read()
    image = MIMEImage(img_data, name=os.path.basename(img_path))
else:
    img=None # If the image file does not exist, set img to None
   

#Check if the attachment document file exists
document_path=print("Enter the path of the document to attach: ")
doc_path=input(document_path)
if os.path.isfile(doc_path):
    with open(doc_path, 'rb') as doc_file:
        doc_data = doc_file.read()
    attachment = MIMEApplication(doc_data, name=os.path.basename(doc_path))
else:
    attachment=None # If the document file does not exist, set attachment to None

# The email body text. You can customize this text as needed
text=input("Enter the body text of the email: ")
#If the text body is empty, set it to a default message    
if text.strip() == "":
    text_body="This is an automated message, please do not reply."
else:
    text_body=text
# If the text body is not empty, use the provided text

# --- EMAIL CONTENT ---
# Attach the email body
def message(subject, text_body, img, attachment):
    # build message contents
    msg=MIMEMultipart()
    # Add Subject
    msg['Subject']=subject  
    # Add text contents
    msg.attach(MIMEText(text_body))  # Attach the email body
    # Add From and To headers
    msg['From'] = user
    msg['To'] = destination

    # Check image parameter
    if img is not None:
         if type(img) is not list:
            img = [img] 
        for img_path in img:
              # read the image binary data
            img_data = open(img_path, 'rb').read()  
            # Attach the image data to MIMEMultipart using MIMEImage, we add the given filename use os.basename
            msg.attach(MIMEImage(img_data, name=os.path.basename(img_path)))
    else:
        print(f"Image file not found. Skipping image attachment.")

    # Check attachment parameter
    if attachment is not None:
         if type(attachment) is not list:
            attachment = [attachment]  

        for one_attachment in attachment:
            with open(doc_path, 'rb') as f:
                # Read in the attachment using MIMEApplication
                file = MIMEApplication(f.read(), name=os.path.basename(doc_path))
            file['Content-Disposition'] = f'attachment; filename="{os.path.basename(doc_path)}"'
            #Add the attachment to our message object
            msg.attach(file)
    else:
        print(f"Document file not found. Skipping document attachment.")
    
    # Return the complete message object
    return msg
# --- END EMAIL CONTENT ---

# Call the message function
msg = message(subj, text_body, img, attachment)

# --- DEBUGGING ---
# Uncomment the following line to print the message content for debugging purposes
# print(msg.as_string())
# --- END DEBUGGING ---


# --- SEND EMAIL ---
smtp.sendmail(user, destination, msg.as_string())

 
# Also, you can use a list of emails, where you wanna send this email
# Example:
to = ["123@gmail.com", "111213@gmail.com", "212223@gmail.com"]

# Use sendmail function to send the email to multiple recipients
for recipient in to:
    msg['To'] = recipient 
    # Send the email 
    smtp.sendmail(from_addr=user, to_addrs=to, msg=msg.as_string())
    # Print a success message
    print(f"Email sent successfully to {recipient}")
# --- END SEND EMAIL ---

# Close the connection
smtp.quit()
# -*- coding: utf-8 -*-
# ---



