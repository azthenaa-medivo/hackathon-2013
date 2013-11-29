from google.appengine.api import mail

def send_email(username,trip_name,email_addr,trip_id):
		message = mail.EmailMessage(sender="BroccoTeamBot <broccotripteam@gmail.com>",
                            subject="Your trip has been created !")
		message.to = username +"<"+email_addr+">"
		link="http://broccotrip.appspot.com/"+trip_id
		message.body = """
Dear %s :

	Your trip %s has been created.  You can now visit %s and planified your trip with more precisions !

	May the broccoli be with you.

The Brocco Team
""" % ( username,trip_name, link )
		message.send()
		
def share_trip(receiver,messageBody):
		message = mail.EmailMessage()
		message.sender = "BroccoTeamBot <broccotripteam@gmail.com>"
		message.subject="Someone shared a trip with you !"
		message.to = receiver
		message.body = messageBody
		message.send()