class FTP(object):
    def __init__(self,endpoint,port=21):
        self.endpoint=endpoint
        self.port=port
        
    def __repr__(self) -> str:
        return f"FTP(endpoint={self.endpoint},port{self.port}"