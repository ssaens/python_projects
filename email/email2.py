import smtplib

fromaddr = 'dilong.yao@gmail.com'
toaddrs  = 'dillon.yao@berkeley.edu'
msg = "\r\n".join([
  "From: dilong.yao@gmail.com",
  "To: dillon.yao@berkeley.edu",
  "Subject: Just a message",
  "",
  "Hi"
  ])
username = 'dilong.yao@gmail.com'
password = '5PHnnC*J!'

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
