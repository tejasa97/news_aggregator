class InvalidAPIKey(Exception):
    
    def __init__(self, provider):
        self.provider = provider

class APIKeyMissing(Exception):
    
    def __init__(self, provider):
        self.provider = provider
