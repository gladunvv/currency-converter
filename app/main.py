import socket
import json
import requests
		

URLS = {
    '/': {'RUB': '0'},
}




def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server_socket.bind(('localhost', 8000))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        #print(request)
        #print()
        #print(addr)

        response =  generate_response(request.decode('UTF-8'))

        client_socket.sendall(response)
        client_socket.close()

def generate_response(request):
    method, url, convert = parse_request(request)
    headers, code = genreate_headers(method, url)
    body = genreate_content(code, url, convert)
    return (headers + body).encode()

def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    res = parsed[3]
    convert_type = parsed[2].split('\n')
    convert_type = convert_type[1]
    print(convert_type)
    currency = res.split('\r')
    convert = {convert_type: currency}
    return method, url, convert

def genreate_headers(method, url):

    if not method == 'POST':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)

    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)



    return ('HTTP/1.1 200 OK\n\n', 200)


def genreate_content(code, url, convert):
    if code == 404:
        return '<h1>404</h1><p>Page not found</p>'

    if code == 405:
        return '<h1>405</h1><p>Method not allowd</p>'

    if 'RUB:' and 'USD:' not in convert.keys():
        return json.dump({'errors': 'not found data'})

    data = get_currency(convert)
    URLS[url]['RUB'] = data
    return json.dumps(URLS[url])    


if __name__ == "__main__":
    main()