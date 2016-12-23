import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
def py_mail(SUBJECT, BODY, TO, FROM):
    """With this function we send out our html email"""
 
    # Create message container - the correct MIME type is multipart/alternative here!
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    MESSAGE.preamble = """
Your mail reader does not support the report format.
Please visit us <a href="http://www.mysite.com">online</a>!"""
 
    # Record the MIME type text/html.
    HTML_BODY = MIMEText(BODY, 'html')
 
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    MESSAGE.attach(HTML_BODY)
 
    # The actual sending of the e-mail
    server = smtplib.SMTP('smtp.gmail.com:587')
 
    # Print debugging output when testing
    if __name__ == "__main__":
        server.set_debuglevel(1)
 
    # Credentials (if needed) for sending the mail
    password = "gmggmggmg"
 
    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM, [TO], MESSAGE.as_string())
    server.quit()
 
if __name__ == "__main__":
    """Executes if the script is run as main script (for testing purposes)"""
 
    email_content = """
<html>
<header>
<span itemscope itemtype="http://schema.org/EmailMessage">  
   <meta itemprop="description" content="Email address verification"/>  
   <span itemprop="action" itemscope itemtype="http://schema.org/ConfirmAction">    
      <meta itemprop="name" content="Verify email"/>    
        <span itemprop="handler" itemscope itemtype="http://schema.org/HttpActionHandler">      
            <link itemprop="url" href="http://ec2-52-66-125-230.ap-south-1.compute.amazonaws.com/tests/verfiy.php"/>    
        </span>  
  </span>
</span>
</header>
<body>
<div>EMAIL CONTENT GOES HERE</div>
</body>
</html>
"""
 
    TO = 'gauthamgajith@gmail.com'
    FROM ='test4generalpurpose@gmail.com'
 
    py_mail("Test email subject", email_content, TO, FROM)