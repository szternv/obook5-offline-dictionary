#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from datetime import datetime
import argparse, gzip, secrets

ap=argparse.ArgumentParser()
ap.add_argument('--host-ip',required=True)
ap.add_argument('--port',type=int,default=8085)
ap.add_argument('--image',required=True)
ap.add_argument('--version',default='V1.4')
a=ap.parse_args()
IMG=Path(a.image).resolve(); MD5=Path(str(IMG)+'.md5')
if not IMG.exists() or not MD5.exists(): raise SystemExit('Missing image or image.md5')
XML=(
'<?xml version="1.0" encoding="UTF-8"?>'
'<Response><GetReaderPackage>'
'<Item><title>Owner dictionary bootstrap</title><content>Installs local owner startup bridge.</content></Item>'
f'<Version>{a.version}</Version>'
f'<GetPackageUrl>http://{a.host_ip}:{a.port}/{IMG.name}</GetPackageUrl>'
f'<Md5>http://{a.host_ip}:{a.port}/{MD5.name}</Md5>'
'</GetReaderPackage></Response>')
class H(BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'; server_version='Microsoft-IIS/8.5'; sys_version=''
    def log_message(self,fmt,*args): print(f'[{self.client_address[0]}] '+fmt%args)
    def common(self):
        self.send_header('Cache-Control','private'); self.send_header('X-AspNet-Version','4.0.30319'); self.send_header('X-Powered-By','ASP.NET')
    def do_GET(self):
        print(self.requestline)
        path=self.path.split('?',1)[0]
        if path.lower()=='/readerapi.aspx':
            body=gzip.compress(XML.encode())
            self.send_response(200); self.common(); self.send_header('Content-Type','application/xml; charset=utf-8'); self.send_header('Content-Encoding','gzip'); self.send_header('Set-Cookie',f'ASP.NET_SessionId={secrets.token_hex(12)}; path=/; HttpOnly; SameSite=Lax'); self.send_header('result-code','0'); self.send_header('TimeStamp',datetime.now().strftime('%Y/%m/%d %H:%M:%S')); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body); return
        if path=='/'+IMG.name:
            d=IMG.read_bytes(); self.send_response(200); self.common(); self.send_header('Content-Type','application/octet-stream'); self.send_header('Content-Length',str(len(d))); self.end_headers(); self.wfile.write(d); return
        if path=='/'+MD5.name:
            d=MD5.read_bytes(); self.send_response(200); self.common(); self.send_header('Content-Type','text/plain'); self.send_header('Content-Length',str(len(d))); self.end_headers(); self.wfile.write(d); return
        self.send_error(404)
print(f'Serving on 0.0.0.0:{a.port}; redirect service.obook.com.cn to {a.host_ip}')
ThreadingHTTPServer(('0.0.0.0',a.port),H).serve_forever()
