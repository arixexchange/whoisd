from database import ARIXDatabase
import socket
import sys

HOST = "localhost"
PORT = 43

WELCOME_MESSAGE = """% This is the ARIX Database WHOIS server.
% Objects follow a loose RPSL-like format.
%
% For more information, visit https://arix.dev/whois\n
"""

db = ARIXDatabase()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (HOST, PORT)
print("Starting ARIXDB WHOIS server on {}:{}".format(*server_address))
sock.bind(server_address)

sock.listen(20)

def output_format(entry):
    if entry != None:
        entry["source"] = "ARIX"
        out = ""
        for key in entry.keys():
            out += "{: <10} {}\n".format(*[key + ":", entry[key]])
        out = out.strip()
    else:
        out = "No data found."

    return out.encode()

try:
    while True:
        connection, client_address = sock.accept()

        try:
            connection.sendall(WELCOME_MESSAGE.encode())

            query = connection.recv(1024).decode().strip().rstrip().upper()

            if query.endswith("-MNT"): # mntner
                connection.sendall(output_format(db.get_mntner(query)))

            elif query.startswith("AS"): # aut-num
                connection.sendall(output_format(db.get_aut_num(query.strip("AS"))))

            elif query.startswith("44"): # route
                connection.sendall(output_format(db.get_route(query)))

            elif query.startswith("2"): # route6
            connection.sendall(output_format(db.get_route6(query)))

        except:
            connection.close()
        finally:
            connection.close()
except:
    print("\nClosing socket.")
    sock.close()
