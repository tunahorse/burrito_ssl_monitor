This script checks the SSL certificate expiration of a list of URLs and sends a daily report of their expiration status to a Telegram chat. The script has the following functions:

check_ssl_expiry(url): This function takes a single URL as input, checks the SSL certificate expiration date, and returns a message indicating the expiration status of the certificate.

check_ssl_expiry_multiple(hosts): This function takes a list of URLs as input, calls check_ssl_expiry() on each URL, and returns a list of messages with the expiration status of each SSL certificate.

format_daily_report(messages): This function takes a list of messages as input, formats them into a daily report, and returns the report as a string.

delete_message(chat_id, message_id, bot_token): This function takes the chat ID, message ID, and bot token as input, and sends a request to the Telegram API to delete the message with the specified ID in the specified chat.

The main part of the script defines a list of URLs to check, calls check_ssl_expiry_multiple() to get the SSL certificate expiration status of each URL, formats the messages into a daily report using format_daily_report(), and sends the report to a specified Telegram chat using the Telegram Bot API. If the message is successfully sent, the script prints a success message to the console. If there is an error sending the message, the script prints an error message to the console.



