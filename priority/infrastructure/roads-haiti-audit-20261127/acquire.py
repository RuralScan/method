"""Acquire only complete road members from a pinned, dated provider ZIP."""
import hashlib
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

URL = 'https://download.geofabrik.de/central-america/haiti-and-domrep/haiti-and-domrep-261126-free.shp.zip'
root = Path(sys.argv[1])
root.mkdir(parents=True, exist_ok=True)
with urllib.request.urlopen(urllib.request.Request(URL, method='HEAD'), timeout=60) as response:
    size = int(response.headers['Content-Length'])
    etag = response.headers['ETag']
    modified = response.headers.get('Last-Modified')

class Remote(io.RawIOBase):
    def __init__(self):
        self.pos = 0
        self.transferred = 0
    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos
    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos + offset if whence == 1 else size + offset
        return self.pos
    def read(self, count=-1):
        count = min(size-self.pos, count if count >= 0 else size-self.pos)
        if count <= 0: return b''
        request = urllib.request.Request(URL, headers={
            'Range': f'bytes={self.pos}-{self.pos+count-1}', 'If-Match': etag})
        with urllib.request.urlopen(request, timeout=90) as response:
            assert response.status == 206 and response.headers.get('ETag') == etag
            assert response.headers['Content-Range'] == f'bytes {self.pos}-{self.pos+count-1}/{size}'
            data = response.read()
        assert len(data) == count
        self.pos += count
        self.transferred += count
        return data

remote = Remote()
manifest = {'url': URL, 'etag': etag, 'last_modified_utc': modified,
            'archive_size': size, 'full_archive_acquired': False, 'members': {}}
with zipfile.ZipFile(remote) as source:
    names = [n for n in source.namelist() if n.startswith('gis_osm_roads_free_1.')]
    assert {Path(n).suffix for n in names} >= {'.shp', '.shx', '.dbf', '.prj'}
    for name in names:
        data = source.read(name)  # zipfile also checks each complete member CRC
        (root/name).write_bytes(data)
        manifest['members'][name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        print(name, len(data), flush=True)
manifest['range_bytes_transferred'] = remote.transferred
(root/'acquisition.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps(manifest, indent=2))
