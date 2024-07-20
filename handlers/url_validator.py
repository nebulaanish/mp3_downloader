from urllib.parse import urlparse

class URLValidator:
    def is_valid_youtube_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc in ['www.youtube.com', 'youtu.be']