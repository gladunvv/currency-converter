import socket
import json


URLS = {
    '/': {'HEllo': 'BUYs'},
}


def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return method, url

def genreate_headers(method, url):
    if not method == 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)

    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)

def genreate_content(code, url):
    if code == 404:
        return '<h1>Page not found 404</h1>'

    if code == 405:
        return '<h1>Method not allowd 405</h1>'

    return json.dumps(URLS[url])


def generate_response(request):
    method, url = parse_request(request)
    headers, code = genreate_headers(method, url)
    body = genreate_content(code, url)
    return (headers + body).encode()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server_socket.bind(('localhost', 8000))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        print(request)
        print()
        print(addr)

        response =  generate_response(request.decode('UTF-8'))

        client_socket.sendall(response)
        client_socket.close()



if __name__ == "__main__":
    main()