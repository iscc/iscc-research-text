import requests
import concurrent.futures
import pandas as pd    
import json as j
import time
import os

database_file = r'D:\unpaywall_snapshot_2021-07-02T151134.jsonl'
threadNumber = 1

def generate_iscc(pdf_url, thread_name):
    print(f'Thread {thread_name} started...')
    print(f'PDF Download URL: {pdf_url}')
    donwload_pdf(pdf_url, thread_name)
    iscc(thread_name)
    delete_file(thread_name)
    print(f'Thread {thread_name} done.')

# Function to download the PDF file
def donwload_pdf(pdf_url, file_name):
    try:
        pdf_bytes = requests.get(pdf_url).content
        pdf_name = file_name
        pdf_name = f'{pdf_name}.pdf'
        with open(pdf_name, 'wb') as pdf_file:
            pdf_file.write(pdf_bytes)
            print(f'{pdf_name} was downloaded...')
    except Exception:
        print('Can not download pdf file.')

def iscc(thread_name):
    #genreate iscc
    try:
        print(f'Generate ISCC for file: {thread_name}.pdf')
        output = os.system(f'igen iscc {thread_name}.pdf --granular -vv')
        print(output)
    except Exception:
        print(f'Can not genreate ISCC for {thread_name}.pdf')

def delete_file(thread_name):
    try:
        print(f'File {thread_name}.pdf removed...')
        os.remove(f'{thread_name}.pdf')
    except Exception:
        print(f'Can not delete file {thread_name}.pdf')

def main(t):

    threads = t

    files = []
    for number in range(threads):
        files.append(str(number))

    result = []
                                                         #has to be 1
    for chunk in pd.read_json(database_file, lines=True, chunksize=1):
        
        #print(chunk[:1])

        index = chunk.index.start
        print(f'### Calculating index {index} ###')

        json = chunk[:1].iloc[0].best_oa_location

        if len(result) <= threads:
            if str(json) != 'nan':
                pdf_url = json.get('url')
                result.append(pdf_url)

                if len(result) == threads:
                    with concurrent.futures.ThreadPoolExecutor() as executer:
                        results = executer.map(generate_iscc, result, files)
                        for result in results:
                            print(result)
                            pass

                    result = []
                    #break

start = time.perf_counter()

#parameter value equals number of threads
main(8)

finish = time.perf_counter()

print(f'Finished in {round(finish - start, 2)} seconds(s)')