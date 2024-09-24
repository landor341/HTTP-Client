import logging
import socket
import sys


# Parses and http response and allows you to acces its parsed data
class http_response():
    def __init__(self, sock):
        self.headers = {}
        self.body = bytearray(b'')
        initChunk = sock.recv(4096)
        titleAndChunk = initChunk.split(b'\n', 1)
        
        if titleAndChunk[0].split(b' ')[1] != b"200":
            self.body = None
            return

        initChunk = titleAndChunk[1]
        headerBody = initChunk.split(b"\r\n\r\n")
        for line in headerBody[0].split(b'\r\n'):
            if line == b"":
                break
            header = line.split(b":",1)
            self.headers[header[0]] = header[1]

        if self.headers.get(b"Transfer-Encoding").lstrip(b' ') == b"chunked":
            chunk = headerBody[1]
            isCurLineChunkHead = False
            while len(chunk) != 0:
                if isCurLineChunkHead:
                    if headerBody.contains("\r\n")
                else:

                chunk = sock.recv(4096)
        else:
            chunk = headerBody[1]
            while len(chunk) != 0:
                self.body.extend(chunk)
                chunk = sock.recv(4096)
        self.body = bytes(self.body)
        print(self.headers)

    def getContent(self):
        return self.body



def retrieve_url(url):
    """
    return bytes of the body of the document at url
    """

    splitURL = url.split(':',1)[-1].lstrip('/').split('/',1)
    if len(splitURL) == 1:
        splitURL.append("/")
    else:
        splitURL[1] = "/" + splitURL[1]
    


    port = splitURL[0].split(":")
    if len(port) > 1:
        splitURL[0] = port[0]
        port = int(port[1])
        req = f'GET {splitURL[1]} HTTP/1.1\r\nHost:{splitURL[0]}:{port}\r\nConnection:close\r\n\r\n'.encode()
    else:
        port = 80 # default port
        req = f'GET {splitURL[1]} HTTP/1.1\r\nHost:{splitURL[0]}\r\nConnection:close\r\n\r\n'.encode()
    print(port)

    
    try:
        sock = socket.socket()
        sock.connect((splitURL[0], port))
        sock.send(req)

        resp = http_response(sock)
        sock.close()

        return resp.getContent()
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    sys.stdout.buffer.write(retrieve_url(sys.argv[1])) # pylint: disable=no-member
