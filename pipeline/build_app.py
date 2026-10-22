#!/usr/bin/env python3
"""Build the single-file Repertorium Publicum Explorer.

  template  ->  app_template.html   (readable source, kept in the repo)
  data      ->  kent.json           (extracted from the OOReP dump)
  output    ->  kent_repertory.html (one self-contained file)

The repertory is embedded gzip + base64 and decompressed in the browser with
DecompressionStream.  CSS/JS/HTML whitespace is minified on the way out; the
readable template is what lives in the repository.
"""
import base64, gzip, os, re

TPL = '/scratch/work/kent/app_template.html'
DATA = '/scratch/work/kent/kent.json'
OUT = '/scratch/work/kent/kent_repertory.html'
VERSION = '1.3.0'


def minify_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};:,])\s*', r'\1', css)
    css = css.replace(';}', '}')
    return css.strip()


def minify_js(js):
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.S)
    js = re.sub(r'(?m)^\s*//.*$', '', js)          # whole-line comments only
    js = re.sub(r'(?m)^[ \t]+', '', js)            # indentation
    js = re.sub(r'\n{2,}', '\n', js)               # blank lines
    return js.strip()


def minify_html(html):
    html = re.sub(r'(?m)^[ \t]+', '', html)
    html = re.sub(r'\n{2,}', '\n', html)
    return html


def main():
    raw = open(DATA, 'rb').read()
    gz = gzip.compress(raw, 9)
    b64 = base64.b64encode(gz).decode('ascii')
    tpl = open(TPL, encoding='utf-8').read()
    assert '__DATA__' in tpl, 'placeholder missing'

    style = re.search(r'<style>(.*?)</style>', tpl, re.S)
    appjs = re.search(r'<script>\n"use strict";(.*?)</script>', tpl, re.S)
    before = len(tpl)

    html = tpl
    if style:
        html = html.replace(style.group(1), minify_css(style.group(1)), 1)
    if appjs:
        html = html.replace('"use strict";' + appjs.group(1), '"use strict";' + minify_js(appjs.group(1)), 1)
    html = minify_html(html)
    after = len(html)

    html = html.replace('__DATA__', b64, 1)
    html = html.replace('<title>', '<meta name="app-version" content="%s">\n<title>' % VERSION, 1)
    open(OUT, 'w', encoding='utf-8').write(html)

    print('data raw    :', round(len(raw)/1048576, 2), 'MB')
    print('data gzip   :', round(len(gz)/1048576, 2), 'MB')
    print('base64      :', round(len(b64)/1048576, 2), 'MB')
    print('code minify :', before, '->', after, 'bytes  (-%d, %.0f%%)' % (before-after, 100*(before-after)/before))
    print('output html :', round(len(html)/1048576, 2), 'MB ->', OUT)


if __name__ == '__main__':
    main()
