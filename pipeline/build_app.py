#!/usr/bin/env python3
"""Build the single-file Kent Repertory Explorer: inject gzip+base64 data into the template."""
import base64, gzip, os, sys

TPL = '/scratch/work/kent/app_template.html'
DATA = '/scratch/work/kent/kent.json'
OUT = '/scratch/work/kent/kent_repertory.html'
VERSION = '1.0.0'

def main():
    raw = open(DATA, 'rb').read()
    gz = gzip.compress(raw, 9)
    b64 = base64.b64encode(gz).decode('ascii')
    tpl = open(TPL, encoding='utf-8').read()
    assert '__DATA__' in tpl, 'placeholder missing'
    html = tpl.replace('__DATA__', b64, 1)
    html = html.replace('<title>', '<meta name="app-version" content="%s">\n<title>' % VERSION, 1)
    open(OUT, 'w', encoding='utf-8').write(html)
    print('data raw   :', round(len(raw)/1048576, 2), 'MB')
    print('data gzip  :', round(len(gz)/1048576, 2), 'MB')
    print('base64     :', round(len(b64)/1048576, 2), 'MB')
    print('output html:', round(len(html)/1048576, 2), 'MB ->', OUT)

if __name__ == '__main__':
    main()
