import re


class Validators(object):
    def __init__(self):
        """
        Validation Checks for various strings i.e. valid domain name

        https://github.com/kvesteri/validators/blob/master/validators/domain.py

        """
        self.domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9]'
            r'(?:[a-zA-Z0-9-_]{0,61}[A-Za-z0-9])?\.)'
            r'+[A-Za-z0-9][A-Za-z0-9-_]{0,61}'
            r'[A-Za-z]$'
        )
        self.text_type = str
        self.unicode = str

    def _to_unicode(self, obj, charset='utf-8', errors='strict'):
        if obj is None:
            return None
        if not isinstance(obj, bytes):
            return self.text_type(obj)
        return obj.decode(charset, errors)

    def domain(self, value):
        try:
            return True if self.domain_pattern.match(self._to_unicode(value).encode('idna').decode('ascii')) else False
        except (UnicodeError, AttributeError):
            return False
