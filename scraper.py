import requests as requests
from bs4 import BeautifulSoup
import os


def head():
    homepage = 'https://scrapingclub.com/exercise/list_basic/?page='
    page_numbers = [str(i + 1) for i in range(7)]
    print('Please wait...')
    for number in page_numbers:
        link = homepage + number
        source_dir = os.getcwd()
        work_dir = source_dir + f'\\Page_{number}'
        os.mkdir(work_dir)
        os.chdir(work_dir)
        get_page(link)
        links_content(link)
        os.chdir(source_dir)
        print(f'Directory {work_dir} saved.')
        if number != page_numbers[-1]:
            print('Starting the next page.')
    print('All done!\nHave a nice day!')


def get_page(url: str) -> [list, print]:
    r = requests.get(url)
    match r.status_code:
        case 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            picture_links = soup.find_all('img', {'class': 'card-img-top img-fluid'})
            picture_links_list = [link['src'] for link in picture_links]
            return picture_links_list
        case _:
            return print(f'The URL returned {r.status_code}')


def links_content(url: str) -> object:
    for path in get_page(url):
        r = requests.get(url)
        match r.status_code:
            case 200:
                img_data = requests.get(url).content
                name = path.split('/')[-1]
                with open(name, 'wb') as file:
                    file.write(img_data)
                print(f'{name}\t\t\t\tDownloaded and saved.')
            case _:
                return print(f'The URL returned {r.status_code}')


if __name__ == '__main__':
    head()
