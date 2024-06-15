from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .extract_result import ExtractResult

class WebExtractor:
    def extract(self, url: str, data: bytes) -> ExtractResult:
        data_str: str = data.decode('utf-8')
        soup = BeautifulSoup(data_str, 'html.parser')

        title: str
        if soup.title is None:
            title = soup.get_text().substring(0, 10) + '...'
        else:
            title = soup.title.string
        
        thumbnail_link = self._get_thumbnail_link(soup)
        if thumbnail_link != '':
            thumbnail_link = urljoin(url,thumbnail_link)

        return ExtractResult(
            title=title,
            content=soup.get_text(),
            image_links=[urljoin(url, img['src']) for img in soup.find_all('img') if img.get('src')],
            links=[urljoin(url, a['href']) for a in soup.find_all('a', href=True)],
            thumbnail_link=thumbnail_link,
        )
    
    def _get_thumbnail_link(self, soup: BeautifulSoup) -> str:
        thumbnail_url: str
        # Open Graphのサムネイル画像を取得
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            thumbnail_url = og_image['content']
        else:
            # Twitter Cardのサムネイル画像を取得
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image and twitter_image.get('content'):
                thumbnail_url = twitter_image['content']
            else:
                thumbnail_url = ''
        
        return thumbnail_url