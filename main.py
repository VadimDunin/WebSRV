import socket

debug_mode = True

URLS = {
    "/": "hello index",
    "/blog": "hello blog"
}


def parse_request(request):
    parsed = request.split(" ")
    debug_msg("request: "+request)
    debug_msg("parsed: ")
    debug_msg(parsed)
    method = parsed[0]
    url = parsed[1]
    return method, url


def generate_headers(method, url):
    if not method == 'GET':
        return ("HTTP/1.1 405 Method not allowed\n\n", 405)
    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)
    return ('HTTP/1.1 200 OK', 200)


def generate_content(code, url):
    if code == 404:
        return '<h1>404<h1><p>NotFound'
    if code == 405:
        return '<h1>405<h1><p>MethodNotAllowed'
    return "<h1>{}<h1>".format(URLS[url])


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)
    return (headers + body).encode()


def debug_msg(msg):
    if debug_mode:
        print(f"DEBUG: {msg}")


def run_server():
    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Server.bind(('localhost', 5000))
    Server.listen()

    while True:
        client_socket, address = Server.accept()
        request = client_socket.recv(1024)
        debug_msg(request.decode("utf-8"))
        print(" ")
        debug_msg(address)

        response = generate_response(request.decode("utf-8"))

        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    run_server()
