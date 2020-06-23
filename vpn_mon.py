# Python program to test 
# internet speed and VPN connection
  
import speedtest
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import psutil
import pymysql
import sys

def is_running(program_name):
    try:
        for p in psutil.process_iter():
            try:
                if program_name == p.name():
                    return True
            except Exception as ex:
                print(ex)
                pass
        return False
    except Exception as ex:
        print(ex)
        return False

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def insert_db(vpn_on, host, host_accessible, download_speed, upload_speed):
    # Open database connection
    db = pymysql.connect("localhost","root","","vpn_mon" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    print('creating db...')

    sql_create = "CREATE DATABASE IF NOT EXISTS vpn_mon;"

    cursor.execute(sql_create)
    print('created')

    print('creating table...')

    sql_create = """CREATE TABLE IF NOT EXISTS vpn_mon (
            timestamp  TIMESTAMP NOT NULL,
            vpn_on BOOL,
            ip  CHAR(20),
            ip_accessible BOOL,
            download_speed DOUBLE,
            upload_speed DOUBLE
            )"""

    cursor.execute(sql_create)
    print('created')

    print('inserting...')

    sql_create = """INSERT INTO vpn_mon
    (timestamp,vpn_on,ip,ip_accessible,download_speed,upload_speed)
    VALUES
    (NOW(), {}, '{}', {}, {}, {})""".format(vpn_on, host, host_accessible, download_speed, upload_speed)

    cursor.execute(sql_create)

    db.commit()
    print('inserted')

    db.close()

def main():
    host = sys.argv[1]
    st = speedtest.Speedtest() 

    vpn_on = is_running('openvpn.exe') #TODO: add this as a parameter

    if vpn_on:
        host_accessible = ping(host)
        download_speed = st.download()
        upload_speed = st.upload()
        insert_db(vpn_on, host, host_accessible, download_speed, upload_speed)
    else:
        print('Is the VPN connected?')

if __name__ == "__main__":
    main()