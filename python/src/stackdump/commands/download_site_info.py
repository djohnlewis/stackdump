#!/usr/bin/env python

# This script downloads the sites RSS file and associated logos from the net.
import tarfile
import urllib.request
from xml.etree import ElementTree
import sys
def printf(format, *args):
    sys.stdout.write(format % args)
from shutil import copy
import os, ssl, fnmatch
from optparse import OptionParser
from xml.etree import ElementTree
import elasticsearch

import settings
from sqlobject import sqlhub, connectionForURI,AND, IN, SQLObject, \
    UnicodeCol, DateTimeCol, IntCol, DatabaseIndex, dbconnection
from sqlobject.sqlbuilder import Delete, Insert
from sqlobject.styles import DefaultStyle
from pysolr import Solr, SolrError

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_defat_https_context = ssl._create_unverified_context

se_dir = os.path.join(os.environ.get('HOME'), 'stackexchange')
sites_path = os.path.join(se_dir, 'Sites.xml')

script_dir = os.path.dirname(sys.argv[0])
sites_file_path = os.path.join(script_dir, ''
                                           '../../../../data/')
# ensure the data directory exists
# download the sites RSS file

if not os.path.exists(os.path.dirname(sites_file_path)):
    os.mkdir(os.path.dirname(sites_file_path))

print('Downloading StackExchange sites XML file...')
# urllib.request.urlretrieve('https://archive.org/download/stackexchange/Sites.xml', sites_file_path)
print('done.')

print('')



# parse sites RSS file and download logosc
images_dir_path = os.path.join(script_dir, '../../../media/images')
print(os.listdir(images_dir_path))
logos_dir_path = os.path.join(images_dir_path, 'logos48')
if not os.path.exists(logos_dir_path):
    os.mkdir(logos_dir_path)
icons_dir_path = os.path.join(images_dir_path, 'icons')
if not os.path.exists(icons_dir_path):
    os.mkdir(icons_dir_path)
badges_dir_path = os.path.join(images_dir_path, 'badges')
if not os.path.exists(badges_dir_path):
    os.mkdir(badges_dir_path)

with open(sites_path) as f:
    sites_file = ElementTree.parse(f)
    sites = sites_file.findall('row')
    # print(rows[0].attrib)

    for site in sites:
        site_title = site.attrib['LongName']
        site_name = site.attrib['Name']
        # extract the key from the url - remove the http:// and .com
        site_key = site.attrib['TinyName']
        site_url = site.attrib['Url'][8:]
        logo_url = site.attrib['ImageUrl']
        icon_url = site.attrib['IconUrl']
        badge_url = site.attrib['BadgeIconUrl']


        site_vars = (site_url, site_key, site_name, site_title)
        # print(site_vars)
        printf('Site: %s,  key=%s, name="%s", longname="%s"\n' % site_vars)
        try:
            logo_file = os.path.join(logos_dir_path, 'logo-%s.png' % site_key)
            if not os.path.exists(logo_file):
                print('Downloading logo for %s...' % site_title, urllib.request.urlretrieve(logo_url, logo_file))
        except Exception as e:
            print('Failed download logo for %s...' % site_title, str(e))

        try:
            icon_path = os.path.join(icons_dir_path, 'icon-%s.png' % site_key)
            if not os.path.exists(icon_path):
                print('Downloading icon for %s...' % site_title, urllib.request.urlretrieve(icon_url, icon_path))
        except:
            print('Failed download ico for %s...' % site_title, icon_url)

        try:
            badge_file = os.path.join(badges_dir_path, 'badge-%s.png' % site_key)
            if not os.path.exists(icon_path):
                print('Downloading badge for %s...' % site_title, urllib.request.urlretrieve(badge_url, badge_file))
        except:
            printf('Failed download badge for %s...' % site_title)

        site_files = []
        print('Key: ' + site_url)
        for root, dirs, files in os.walk(se_dir):
            for name in files:
                if fnmatch.fnmatch(name, site_url + '*'):
                    print('Match: ' + os.path.join(root, name))
                    site_files.append(os.path.join(root, name))

        sites_data = sites_file_path
        for site_file in site_files:
            dst = sites_data + os.sep + site_key[0] + os.sep + site_key + os.sep + '7z'
            os.makedirs(dst, exist_ok=True)
            os.chdir(dst)
            os.system('tar xzf '+site_file)
            print('Data: ' + site_file)

def prepare_site(xml_root, dump_date, site_key):
    print('Using the XML root path: ' + xml_root + '\n')

    if not os.path.exists(xml_root):
        print('The given XML root path does not exist.')
        sys.exit(1)

    # connect to the database
    print('Connecting to the Stackdump database...')
    conn_str = settings.DATABASE_CONN_STR
    sqlhub.processConnection = connectionForURI(conn_str)
    print('Connected.\n')

# MAIN METHOD
if __name__ == '__main__':
    parser = OptionParser(usage='usage: %pro'
                                'g [options] xml_root_dir')
    parser.add_option('-k', '--site-key', help='Key of the site (if not in sites).')
    parser.add_option('-c', '--dump-date', help='Dump date of the site.')

    (cmd_options, cmd_args) = parser.parse_args()

    if len(cmd_args) < 1:
        print('The path to the directory containing the extracted XML files is required.')
        sys.exit(1)

    prepare_site(cmd_args[0], cmd_options.dump_date, cmd_options.site_key)
