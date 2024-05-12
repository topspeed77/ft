import os
import ftplib
import paramiko
from multiprocessing import Pool
from colorama import Fore, Style

bl = Fore.BLUE
wh = Fore.WHITE
gr = Fore.GREEN
red = Fore.RED
res = Style.RESET_ALL
yl = Fore.YELLOW

def check_ftp_connection(domain, host, port, username, password):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=3)
        ftp.login(username, password)
        ftp.quit()
        return True
    except Exception as e:
        return False

def check_sftp_connection(domain, host, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password, timeout=3)
        ssh.close()
        return True
    except Exception as e:
        return False

def check_connection(line, line_number):
    fields = line.strip().split("|")
    if len(fields) == 5:
        domain, host, port, username, password = fields
        port = int(port)

        if port == 21:
            result = check_ftp_connection(domain, host, port, username, password)
        else:
            result = check_sftp_connection(domain, host, port, username, password)

        if result:
            with open("log.txt", "a") as f:
                f.write("domain: {}\n".format(domain))
                f.write("host: {}\n".format(host))
                f.write("port: {}\n".format(port))
                f.write("username: {}\n".format(username))
                f.write("password: {}\n".format(password))
                f.write("\n")
    else:
        print("Invalid line format (line {}): {}".format(line_number, line))

if __name__ == '__main__':
    # Ask user for the name of the file to check
    filename = input("Masukkan nama file : ")

    # Check if the file exists
    if not os.path.exists(filename):
        print("File {} tidak ditemukan.".format(filename))
        exit()

    # Open the file and read each line
    with open(filename, "r") as f:
        lines = f.readlines()

    # Initialize a pool of worker processes
    pool = Pool()

    # Use the pool to run the check_connection function on each line
    pool.starmap(check_connection, [(line, i+1) for i, line in enumerate(lines)])

    # Close the pool to free up resources
    pool.close()
    pool.join()
