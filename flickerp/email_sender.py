import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from django.conf import settings

FROM_EMAIL = 'hr@geitpl.com'

TEMPLATE_ID = 'd-d027f2806c894df38c59a9dec5460594'

SENDGRID_API_KEY = settings.SENDGRID_API_KEY


# template ids based on status of Candidate model. 
TEMPLATE_IDS=(
    (2, "d-f23e271c9aab4608a6b840007e813bd2"), # cv seelcted for interview
    (4, "d-72adec37e43a498889c4466cd9de1ab4"),  #Selected after Interview
    (6, "d-bd2c2416976048248ca42db3db675fc1"), #cv rejected by HR  without interview
    (7, "d-a2701f97107943439be88084c1cb914f"), #Rejected after interview
)

TEMPLATE_IDS = dict(TEMPLATE_IDS)
 
def send_sendgrid_mail(obj,subject=None, status=None):
    if not TEMPLATE_IDS.get(obj.status, None):
        return False
    
    message = Mail(from_email=FROM_EMAIL,to_emails=[obj.email])

    
    message.dynamic_template_data = {
        'Candidate_name': obj.full_name,
        }
    message.template_id = TEMPLATE_IDS.get(obj.status)

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("Dynamic Messages Sent!")
    except Exception as e:
        print("Error: {0}".format(e))