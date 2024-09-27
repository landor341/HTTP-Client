'''
    This module contains the code to parse out the
    body an http/1.1 response from a socket and to
    receive the body of an http response when given
    the URL to query from
'''


import socket
import sys


def parse_response(sock):
    '''
        Parses http/1.1 response from the given socket
        and returns the body of the result
        Supports chunk-encoding
    '''
    # Class Init
    headers = {}
    body = bytearray(b'')

    # Get chunk with headers
    init_chunk = sock.recv(4096)
    title_and_chunk = init_chunk.split(b'\n', 1)

    # For this assignment we return none if the response isn't a 200 code
    if title_and_chunk[0].split(b' ')[1] != b"200":
        return None

    # Parse out all headers into a dictionary
    header_body = title_and_chunk[1].split(b"\r\n\r\n", 1)
    for line in header_body[0].split(b'\r\n'):
        if line == b"":
            break
        header = line.split(b":", 1)
        headers[header[0]] = header[1]

    # Parse out the body of the request
    if headers.get(b"Transfer-Encoding", b" ").lstrip(b' ') == b"chunked":
        receive_chunk_encoding_body(sock, header_body[1], body)
    else:  # non-chunked body
        chunk = header_body[1]
        while len(chunk) != 0:
            body.extend(chunk)
            chunk = sock.recv(4096)
    return bytes(body)


def receive_chunk_encoding_body(sock, init_chunk, body):
    '''
        Receive body chunks from the sock. Start with the body
        which was left from the initial chunk

        Take each chunk of 4096 bytes and split it into chunks for
        each line separated by \r\n. We only need every other line
        since the other half is just the length of the current chunk
    '''
    # add new line so the algorithm scans size properyly
    sock_chunk = b"\r\n" + init_chunk
    cur_len = 0
    while len(sock_chunk) != 0:
        if cur_len > 0:
            # Either the length of the data is greater t
            # han the size of the current chunk
            if len(sock_chunk) < cur_len:
                cur_len -= len(sock_chunk)
                body.extend(sock_chunk)
                sock_chunk = sock.recv(4096)
            # or the length of the data is less than than
            # or equal to the size of the current chunk
            else:
                body.extend(sock_chunk[:cur_len])
                sock_chunk = sock_chunk[cur_len:]
                cur_len = 0
                if len(sock_chunk) == 0:
                    sock_chunk = sock.recv(4096)
        else:  # Filter out size of chunk line
            # Either the current chunk ends on "\r\n" (in which
            # case the start of the next chunk contains the sizing
            # for the new chunk or you parse the next \r\n and then the chars
            # until you hit a ';' or '\r\n' is the size of the next chunk
            if not sock_chunk.count(b"\r\n") > 0:
                sock_chunk = sock.recv(4096)
            else:
                sock_chunk = sock_chunk.split(b"\r\n", 1)[1]
                if sock_chunk == b"":
                    # if sock_chunk is empty, loop to get next chunk
                    sock_chunk = sock.recv(4096)
                # sock_chunk contains the line containing chunk size
                len_str = sock_chunk.split(b";", 1)[0].split(b"\r\n")[0]
                cur_len = int(len_str, base=16)

                if cur_len == 0:
                    break

                if sock_chunk.count(b"\r\n") > 0:
                    sock_chunk = sock_chunk.split(b"\r\n", 1)[1]
                else:
                    sock_chunk = b""


def retrieve_url(url):
    """
    return bytes of the body of the document at url
    """

    split_url = url.split(':', 1)[-1].lstrip('/').split('/', 1)
    if len(split_url) == 1:
        split_url.append("/")
    else:
        split_url[1] = "/" + split_url[1]

    port = split_url[0].split(":")
    if len(port) > 1:
        split_url[0] = port[0]
        port = int(port[1])
        req = (
                f'GET {split_url[1]} HTTP/1.1\r\n'
                f'Host:{split_url[0]}:{port}\r\n'
                f'Connection:close\r\n\r\n'
                ).encode()
    else:
        port = 80  # default port
        req = (
                f'GET {split_url[1]} HTTP/1.1\r\n'
                f'Host:{split_url[0]}\r\n'
                f'Connection:close\r\n\r\n'
                ).encode()

    resp = None

    try:
        sock = socket.socket()
        # Will throw error if domain doesn't resolve
        sock.connect((split_url[0], port))
        sock.send(req)

        resp = parse_response(sock)
        sock.close()
    except socket.gaierror:
        pass
    return resp


if __name__ == "__main__":
    # pylint: disable=no-member, line-too-long
    sys.stdout.buffer.write(retrieve_url(sys.argv[1]))
