import ssl
import socket
import datetime
import requests
import urllib.parse

def check_ssl_expiry(url):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    try:
        parsed_url = urllib.parse.urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port or 443  # use 443 if no port specified
        path = parsed_url.path or '/'
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
        conn.settimeout(5.0)
        conn.connect((hostname, port))
        ssl_info = conn.getpeercert()
        conn.close()

        cert_expiry = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        days_left = (cert_expiry - datetime.datetime.now()).days

        if days_left < 0:
            message = f"*!!! SSL CERTIFICATE FOR {hostname.upper()} HAS EXPIRED !!!*"
        elif days_left < 5:
            message = f"*!!! SSL CERTIFICATE FOR {hostname.upper()} EXPIRES IN {days_left} DAYS !!!*"
        else:
            message = f"SSL certificate for {hostname} expires in {days_left} days."

        return f"{url}: {message}"
    
    except ssl.SSLError as e:
        return f"SSL error occurred while checking {url}: {e}"
    except socket.error as e:
        return f"Socket error occurred while checking {url}: {e}"

def check_ssl_expiry_multiple(hosts):
    messages = []
    for host in hosts:
        message = check_ssl_expiry(host)
        messages.append(message)
    return messages

def format_daily_report(messages):
    header = "Daily SSL certificate report\n\n"
    table_header = "Hostname | Expiration Status\n--------|--------\n"
    table_body = ""
    for message in messages:
        if ':' in message:
            hostname, status = message.split(': ')
        else:
            hostname, status = message, ""
        table_body += f"{hostname} | {status}\n"
    footer = "\n\n*Note*: SSL certificates that have expired or are expiring in less than 5 days are highlighted in all caps with exclamation marks.\n"
    report = f"{header}{table_header}{table_body}{footer}"
    return report


if __name__ == '__main__':
    hosts = ['https://google.com','https://github.com','https://www.youtube.com'
    ]
    messages = check_ssl_expiry_multiple(hosts)
    report = format_daily_report(messages)
    print(report)
    
    ## These should be set as environment variables, but for the sake of simplicity, I'm hardcoding them here
    
    chat_id = ''  # replace with your chat ID, remember to add the -100 in front of the number
    bot = ''  # replace with your bot token
    
    
    text = urllib.parse.quote(report)

    url = f"https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown"

    response = requests.post(url)
    if response.status_code == 200:
        print(f"Message sent to chat ID {chat_id}")
    else:
        print(f"Failed to send message to chat ID {chat_id}: {response.status_code}")
        
