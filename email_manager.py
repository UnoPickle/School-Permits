import smtplib
from email.message import EmailMessage
EMAIL_ADDRESS = 'pelech.permits@gmail.com'
EMAIL_PASSWORD = 'MY_PASSWORD'# I dont want the code to be on github
EMAIL_CONTENT = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Password Reset</title>
    <style>
        /* Inline CSS Styles for Email */
        body {
            font-family: Arial, sans-serif;
            color: #333;
            background-color: #f7f7f7;
            margin: 0;
            padding: 20px;
        }
        .email-container {
            background-color: #ffffff;
            padding: 30px;
            margin: auto;
            max-width: 600px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h2 {
            color: #333;
        }
        .code {
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
            text-align: center;
            margin: 30px 0;
        }
        p {
            font-size: 16px;
            line-height: 1.6;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 12px;
            color: #888;
        }
        a {
            color: #667eea;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <h2>Password Reset Request</h2>
        <p>Hello,</p>
        <p>We received a request to reset your password. Please use the following code to reset it:</p>
        <div class="code">{content}</div>
        <p>Enter this code on the password reset page to create a new password.</p>
        <p>If you did not request a password reset, please ignore this email or contact support if you have questions.</p>
        <p>Thank you,<br>The Team</p>
    </div>
</body>
</html>
"""
def send_change_password(email: str, code: str):
    msg = EmailMessage()
    msg['Subject'] = 'Forgot your password'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.add_alternative(EMAIL_CONTENT.replace("{content}", code), subtype='html')
    # For HTML content, use:
    # msg.add_alternative('<h1>This is an HTML Email</h1>', subtype='html')

    # Send the email via the SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)