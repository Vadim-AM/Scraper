import os

import pytest
import requests as requests

from .scraper import get_page

RECURSIVE_URL = 'https://scrapingclub.com/exercise/list_basic/'
DIR = os.getcwd()


class TestImageScraper:

    @staticmethod
    def img_urls():
        page = requests.get(RECURSIVE_URL)
        pages_num = [i for i in page.text.split() if 'page-link' in i]
        pages_num = len(pages_num[:-1])
        img_urls = [RECURSIVE_URL + '?page=' + str(i) for i in range(1, pages_num + 1)]
        return img_urls

    @staticmethod
    def img_dirs():
        dir_counter = os.listdir(DIR)
        dir_counter = [DIR + '\\' + i for i in dir_counter if 'Page' in i]
        return dir_counter


@pytest.mark.image_scraper
def test_dirs_num():
    pages_num = len(TestImageScraper.img_urls())
    dirs_num = len(TestImageScraper.img_dirs())
    assert pages_num == dirs_num, 'Количество папок не равно количеству страниц'


@pytest.mark.image_scraper
@pytest.mark.parametrize('page, pic_dir', list(zip(TestImageScraper.img_urls(), TestImageScraper.img_dirs())))
def test_pictures_num(page, pic_dir):
    assert len(get_page(page)) == len(os.listdir(
        pic_dir)), 'Количество изображений на странице не соответствует количеству изображений в соответствующей ' \
                   'директории '


@pytest.mark.image_scraper
@pytest.mark.parametrize('img_dir', TestImageScraper.img_dirs())
def test_file_type(img_dir):
    for file in os.listdir(img_dir):
        assert file.endswith('.jpg'), 'Расширение файла не .jpg'
