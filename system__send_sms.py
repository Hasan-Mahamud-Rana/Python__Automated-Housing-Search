#------------------------------------------#
# SMS send                                 #
#------------------------------------------#

from twilio.rest import Client

class smsClass:

  def __init__(self, param):
    self.param  = param

  def smsAuth(self):
    auth_sid    = 'ACc3cf88230a63fbf5cb874ab6a405f9b3'
    auth_token  = 'cc357b6608b27e927d9ec6a4aa03f15c'

    return Client(auth_sid, auth_token)

  def smsSend(self):
    client      = self.smsAuth()
    message     = client.messages \
                  .create(
                    body   = 'Hello {},\n\nWelcome to the "Rental Search using Web Scraping". \nThe results based on your input requirements are available on the dashboard. \n\nPlease visit this link: http://192.168.0.104:8501 to view the results.\n\nRegards\nRental Search using Web Scraping\nPython Panthers'.format(self.param['name']),
                    from_  = '+14692810677',
                    to     = self.param['phone']
                  )
    print(message.Status.DELIVERED)