from twilio.rest import Client



def alert(message:str):
    # Replace with your actual credentials
    account_sid = ''
    auth_token = ''

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='',  # Use from_ instead of from
        body=f'{message}',
        to=''
    )


