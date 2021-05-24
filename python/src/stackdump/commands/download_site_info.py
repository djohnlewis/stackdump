#!/usr/bin/env python

# This script downloads the sites RSS file and associated logos from the net.

import urllib.request
from xml.etree import ElementTree
import sys
import os, ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

se_dir = os.path.join(os.environ.get('HOME'), 'stackexchange')
sites_path = os.path.join(se_dir, 'Sites.xml')

script_dir = os.path.dirname(sys.argv[0])
sites_file_path = os.path.join(script_dir, '../../../../data/sites')

# ensure the data directory exists\\\\
if not os.path.exists(os.path.dirname(sites_file_path)):
    os.mkdir(os.path.dirname(sites_file_path))

# download the sites RSS file
print('Downloading StackExchange sites XML file...', )
urllib.request.urlretrieve('https://archive.org/download/stackexchange/Sites.xml', sites_file_path)
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
    rows = sites_file.findall('row')
    # print(rows[0].attrib)

    for row in rows:
        entry_title = row.attrib['Name']
        print('Entry: ' + entry_title)

        # extract the key from the url - remove the http:// and .com
        site_key = row.attrib['TinyName']
        print('Site: ' + site_key)
        logo_url = row.attrib['ImageUrl']
        icon_url = row.attrib['IconUrl']
        badge_url = row.attrib['BadgeIconUrl']

        try:
            print('Downloading logo for %s...' % entry_title,
                  urllib.request.urlretrieve(logo_url, os.path.join(logos_dir_path, 'logo-%s.png' % site_key)))
        except:
            print('Failed download logo for %s...' % entry_title)

        try:
            print('Downloading icon for %s...' % entry_title,
              urllib.request.urlretrieve(icon_url, os.path.join(icons_dir_path, 'icon-%s.png' % site_key)))
        except:
            print('Failed download ico for %s...' % entry_title)

        try:
            print('Downloading badge for %s...' % entry_title,
              urllib.request.urlretrieve(badge_url, os.path.join(badges_dir_path, 'badge-%s.png' % site_key)))
        except:
            print('Failed download badge for %s...' % entry_title)

print('done.')


# MAIN METHOD
if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options] xml_root_dir')
    parser.add_option('-n', '--site-name', help='Name of the site.')
    parser.add_option('-d', '--site-desc', help='Description of the site (if not in sites).')
    parser.add_option('-k', '--site-key', help='Key of the site (if not in sites).')
    parser.add_option('-c', '--dump-date', help='Dump date of the site.')
    parser.add_option('-u', '--base-url', help='Base URL of the site on the web.')
    parser.add_option('-Y', help='Answer yes to any confirmation questions.', dest='answer_yes', action='store_true', default=False)

    (cmd_options, cmd_args) = parser.parse_args()

    if len(cmd_args) < 1:
        print('The path to the directory containing the extracted XML files is required.')
        sys.exit(1)

    prepare_site(cmd_args[0], cmd_options.site_name, cmd_options.dump_date,
                cmd_options.site_desc, cmd_options.site_key,
                cmd_options.base_url, answer_yes=cmd_options.answer_yes)
