import yt_dlp
import os

class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts = {
            'extract_flat': 'in_playlist',
            'skip_download': True,
        }

    def get_video_urls(self, url):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            
            if 'entries' in result:
                return [entry['url'] for entry in result['entries'] if entry]
            else:
                return [result['webpage_url']]

    def download_audio(self, url, output_path, audio_format, audio_quality):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': audio_quality,
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])