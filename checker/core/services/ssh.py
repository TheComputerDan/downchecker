class SSH(object):
    def __init__(self,endpoint,port=22):
        self.endpoint=endpoint
        self.port=port

    def __repr__(self) -> str:
        return f"SSH(endpoint={self.endpoint},port={self.port})"
