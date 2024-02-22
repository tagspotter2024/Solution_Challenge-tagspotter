import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

f=open("password.txt", "r")

def send_mail(gmailid,current_datetime,nospace_text):
    # Email account details
    sender_email = 'tagspotterproject@gmail.com'  
    sender_password = f.read()      


    recipient_email = gmailid
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  

    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()  

        
        smtp.login(sender_email, sender_password)
        
    except Exception as e:
        print(f"Error: Unable to connect to SMTP server - {e}")
        exit()

    
    msg = MIMEMultipart()


    msg['Subject'] = 'Important Notice: Traffic Violation Fine Notification'

    msg['From'] = sender_email
    msg['To'] = recipient_email


    body = f'''Dear User,

            We hope this message finds you well. We are writing to inform you about a recent traffic violation that has been recorded in your name. It is our responsibility to ensure the safety of all road users, and in accordance with local traffic laws, this violation has resulted in a fine.

            Here are the details of the violation:

            Date and Time of Violation: {[current_datetime]}
            Description of Violation: Speed Violation

            To resolve this matter, you are required to pay a fine of 1000/- within 60 days from the date of this notification. Failure to pay the fine within the stipulated timeframe may result in further legal action and potential license suspension.

            Payment Methods:
             Online Payment: You can conveniently pay your fine online through our official website https://mahatrafficechallan.gov.in/payechallan/PaymentService.htm?_qc=48f189cbd4146b7fd2ce95ccfdb54046.

            Please note that it is essential to reference the provided case number {[nospace_text]} when making your payment. Once the payment is processed.

            We value road safety and your cooperation in adhering to traffic regulations. Thank you for your prompt attention to this matter. If you have any questions or require further assistance, please do not hesitate to contact our traffic department at [Contact Information].

            We urge you to settle this matter promptly to avoid any additional consequences. Your commitment to safe and responsible driving is greatly appreciated.

            Sincerely,

            eChallan
            https://echallan.parivahan.gov.in/'''
    msg.attach(MIMEText(body, 'plain'))

    try:
        smtp.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error: Unable to send email - {e}")

    smtp.quit()
