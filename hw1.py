import logging
import socket
import sys

def retrieve_url(url):
    """
    return bytes of the body of the document at url
    """
    return b"this is unlikely to be correct"

if __name__ == "__main__":
    sys.stdout.buffer.write(retrieve_url(sys.argv[1])) # pylint: disable=no-member



class http_request():
    
    def __init__(self, method, url, version):
        self.request_line = f"{method} {url} {version} \n"
    
    def add_header

    def __str__(self):
        res = str(self.request_line)

        for h in self.header_fields:
            res.join(h)

        return res

class http_header_field():
    def __str__(self):
        return f"{self.name}: {self.value}\n"

class http_response():
    
