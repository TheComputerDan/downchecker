import socket


class FTP(object):
    def __init__(self, endpoint, port=21):
        self.endpoint = endpoint
        self.port = port
        
    def __repr__(self) -> str:
        return f"FTP(endpoint={self.endpoint},port{self.port}"

    def check(self):
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.endpoint, self.port))
            s.sendall(b'')
            header = str(s.recv(4096), 'utf-8')
            if any(protocol in header for protocol in ['ftp', 'FTP']):
                return True
            else:
                return False
        except Exception:
            return False
        finally:
            s.close()
