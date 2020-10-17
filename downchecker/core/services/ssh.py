import socket
from downchecker.core.validators import Validators
from downchecker.core.advancedDNS import AdvancedDNS


class SSH(object):
    def __init__(self, endpoint: str, port: int = 22, timeout: float = 5.0):
        self.endpoint = endpoint
        self.port = port
        self.timeout = timeout

        self.vd = Validators()
        self.adns = AdvancedDNS(hostname=self.endpoint)

    def __repr__(self) -> str:
        return f"SSH(endpoint={self.endpoint},port={self.port})"

    def check(self):
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.vd.domain(self.endpoint) or self.adns.is_private():
                s.settimeout(float(self.timeout))
                s.connect((self.endpoint, self.port))
                s.sendall(b'')
                header = str(s.recv(4096), 'utf-8')
                if any(protocol in header for protocol in ['ssh', 'SSH']):
                    return True
                else:
                    return False
            else:
                return False

        except Exception:
            return False
        finally:
            s.settimeout(None)
            s.close()

    def authenticated_check(self):
        ...
