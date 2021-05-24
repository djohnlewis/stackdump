#!/usr/bin/env python

# This script downloads the sites RSS file and associated logos from the net.

import urllib
from xml.etree import ElementTree
import os
import sys
We

se_dir = os.path.join(os.environ.get('HOME'), 'stackexchange')
sites_path = os.path.join(se_dir, 'Sites.xml')

script_dir = os.path.dirname(sys.argv[0])
sites_file_path = os.path.join(script_dir, '../../../../data/sites')

# ensure the data directory exists\\\\
if not os.path.exists(os.path.dirname(sites_file_path)):
    os.mkdir(os.path.dirname(sites_file_path))

# download the sites RSS file
print('Downloading StackExchange sites XML file...',)
urllib.urlretrieve('https://archive.org/download/stackexchange/Sites.xml', sites_file_path)
print('done.')

print('')

# parse sites RSS file and download logosc
images_dir_path = os.path.join(script_dir, '../../../media/images/logos')
logos_dir_path = os.path.join(images_dir_path, 'logos')
icons_dir_path = os.path.join(images_dir_path, 'icons')
badgos_dir_path = os.path.join(images_dir_path, 'badgos')
if not os.path.exists(logos_dir_path):
    os.mkdir(logos_dir_path)

with open(sites_path) as f:
    sites_file = ElementTree.parse(f)
    entries = sites_file.findall('sites/row')
    print(entries)
    
    for entry in entries:
        entry_title = entry.find('{http://www.w3.org/2005/Atom}title').text.encode('ascii', 'ignore')
        
        # extract the key from the url - remove the http:// and .com
        site_key = entry.find('{http://www.w3.org/2005/Atom}id').text
        if site_key.startswith('http://'):
            site_key = site_key[len('http://'):]
        if site_key.endswith('.com'):
            site_key = site_key[:-len('.com')]
        if site_key.endswith('.stackexchange'):
            site_key = site_key[:-len('.stackexchange')]
        
        print('Downloading logo for %s...' % entry_title,
              urllib.urlretrieve('http://cdn.sstatic.net/Sites/%s/img/icon-48.png' % site_key,
                                 os.path.join(logos_dir_path, '%s.png' % site_key)))
        print('done.')
