import os
import csv
import requests
from sys import argv
from bs4 import BeautifulSoup as bs


csv_output_path = os.path.abspath(os.path.join('.', 'output.csv'))
download_path = os.path.abspath(os.path.join('.', 'download'))
if not os.path.exists(download_path):
    os.mkdir(download_path)


def parse_index_page(page_num):
    url = 'https://www.ed2000k.com/archives.asp?PageIndex={}'.format(page_num)
    r = requests.get(url)
    if r.ok:
        soup = bs(r.text, 'html.parser')
        tags = [tag for tag in soup.find_all(name='a', attrs={"href": True}) if '/ShowFile/' in tag['href']]
        return {tag['href'].replace('/ShowFile/', '').replace('.html', ''):tag.text  for tag in tags}


def parse_page(uid):
    url = 'https://www.ed2000k.com/ShowFile/{}.html'.format(uid)
    r = requests.get(url)
    if r.ok:
        soup = bs(r.text, 'html.parser')
        if '出错' in soup.title.text:
            return {}
        context = {'raw': r}
        title = soup.find_all(name='td', attrs={'colspan': '2'})
        context['title'] = title[0].text if title else None
        summary = soup.find_all(name='div', attrs={'class': 'PannelBody'})
        context['summary'] = summary[0] if summary else None
        context['ed2k_links'] = {tag['href']:tag.text for tag in soup.find_all(name='a', attrs={'href': True}) if 'ed2k://' in tag['href']}
        print('uid: {}, title: {}'.format(uid, context['title']))
        return context
    return {}


def main(uid):
    try:
        if not uid.isdigit() or int(uid) < 0 or int(uid) >= 999999:
            print('Invaid uid {}'.format(uid))
            return
        context = parse_page(uid)
        if context:
            writing_list = [uid, context['title']]
            for link, filename in context['ed2k_links'].items():
                writing_list.append(filename)
                writing_list.append(link)
            # save csv
            with open(csv_output_path, 'a', newline='', encoding='utf-8', errors='ignore') as csv1:
                csv_write = csv.writer(csv1, dialect='excel')
                csv_write.writerow(writing_list)
            # save html file
            with open(os.path.join(download_path, '{}.html'.format(uid)), 'w', encoding='utf-8', errors='ignore') as w:
                w.write(context['raw'].text)
        else:
            print('Parse fail with uid {}'.format(uid))
    except Exception as e:
        print('Error Occur, error: {}'.format(e))
    

if __name__ == "__main__":
    uid = input('uid: ') if len(argv) < 2 else argv[1]
    main(uid)
    