import os
import csv
from main import parse_index_page

csv_output_path = os.path.abspath(os.path.join('.', 'index.csv'))


if __name__ == "__main__":
    for x in range(1, 7300):
        print(x)
        try:
            with open(csv_output_path, 'a', newline='', encoding='utf-8', errors='ignore') as csv1:
                csv_write = csv.writer(csv1, dialect='excel')
                for uid, title in parse_index_page(x).items():
                    csv_write.writerow([uid, title])
        except Exception as e:
            print('Error Occur, error: {}'.format(e))