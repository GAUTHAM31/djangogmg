import smtplib

gmail_user = 'test4generalpurpose@gmail.com'  
gmail_password = 'gmggmggmg'

From =gmail_user  
to = ['gauthamgajith@gmail.com']  
subject = 'OMG Super Important Message'  
body = 'Hey, what'

message = 'Subject: %s\n\n%s' % (subject,body)

try:  
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(From, to, message)
    server.close()

    print 'Email sent!'
except:  
    print 'Something went wrong...'