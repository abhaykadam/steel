import csv
import tempfile
import xml.etree.ElementTree as ET
import xmltodict
import zipfile

import requests

XML_URL = 'https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100'


def get_zipfile_url():
    resp = requests.get(XML_URL)

    root = ET.fromstring(resp.content)
    for doc in root.findall('./result/doc'):
        dltins = False
        download_link = None
        for child in doc.findall('./str'):
            if child.attrib['name'] == 'file_type' and child.text == 'DLTINS':
                dltins = True

            if child.attrib['name'] == 'download_link':
                download_link = child.text

        if dltins and download_link:
            return download_link


def download_file(url):
    filename = url.split('/')[-1]

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return filename


def extract_file(zip_name):
    file = zip_name.split('.zip')[0] + '.xml'
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        zip_ref.extract(file)

    return file


def xml_to_csv(xml_file):
    contents = xmltodict.parse(
        open(xml_file, 'rb'))

    with open('final.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ['FinInstrmGnlAttrbts.Id',
             'FinInstrmGnlAttrbts.FullNm',
             'FinInstrmGnlAttrbts.ClssfctnTp',
             'FinInstrmGnlAttrbts.CmmdtyDerivInd',
             'FinInstrmGnlAttrbts.NtnlCcy',
             'Issr'])

        for row in contents['BizData']['Pyld']['Document']['FinInstrmRptgRefDataDltaRpt']['FinInstrm']:
            if 'TermntdRcrd' not in row:
                continue

            record = row['TermntdRcrd']

            issr = record['Issr']
            id_ = record['FinInstrmGnlAttrbts']['Id']
            full_nm = record['FinInstrmGnlAttrbts']['FullNm']
            clssfctn_tp = record['FinInstrmGnlAttrbts']['ClssfctnTp']
            cmmdty_deriv_ind = record['FinInstrmGnlAttrbts']['CmmdtyDerivInd']
            ntnl_ccy = record['FinInstrmGnlAttrbts']['NtnlCcy']

            writer.writerow([
                id_, full_nm, clssfctn_tp,
                cmmdty_deriv_ind, ntnl_ccy, issr])


url = get_zipfile_url()
zip_name = download_file(url)
xml_file = extract_file(zip_name)
xml_to_csv(xml_file)
