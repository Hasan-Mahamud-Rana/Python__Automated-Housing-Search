#------------------------------------------#
# Email send                               #
#------------------------------------------#

import smtplib

class emailClass:

  def __init__(self, param):
    self.param    = param

  def emailProcessor(self, address_from, auth_password, address_to, message):
    server        = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(address_from, auth_password)
    server.sendmail(address_from, address_to, message)
    server.quit()
  
  def emailAuth(self):
    address_from  = 'webscraping21@gmail.com'
    auth_password = 'saima@5430'
    return address_from, auth_password

  def emailBody(self):
    subject       = 'Rental Search Results'
    email_body    = 'Hello {},\n\nWelcome to the "Rental Search using Web Scraping". \nThe results based on your input requirements are available on the dashboard. \n\nPlease visit this link: http://192.168.0.104:8501 to view the results. \n\nRegards\nRental Search using Web Scraping \nPython Panthers'.format(self.param['name'])

    message       = 'Subject: {}\n\n{}'.format(subject, email_body)
    return message

  def emailSend(self):
    login         = self.emailAuth()
    address_from  = login[0]
    auth_password = login[1]

    address_to    = self.param['email']
    message       = self.emailBody()

    self.emailProcessor(address_from, auth_password, address_to, message)
