from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")


COMMANDS = (
    "/start - bot ishga tushdi\n"
    "/help - buyruqlar\n"
    "/send_message - habar qoldirish\n"
)

SEND_GROUP_TEXT = lambda first_name, last_name, username, user_message: f"""
FROM: 
{ first_name }
{ last_name }
https://t.me/{ username } \n

MESSAGE: 
{ user_message }
"""