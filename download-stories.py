#!/usr/bin/env python3

from multiprocessing import Pool
from os import mkdir
from os.path import exists
from shutil import rmtree

import requests
from bs4 import BeautifulSoup
from ftfy import fix_text

root_page = 'http://www.hplovecraft.com/writings/texts'


# REPLACEMENT_RULES += ( ("([\u0000-\u0008]|[\u000B-\u001F])", "") )
# REPLACEMENT_RULES += ( ("[\\p{Zl}][\\p{Zp}]", "\n") )
# REPLACEMENT_RULES += ( ("\\{Cc}", "") )
# REPLACEMENT_RULES += ( ("\\{Cf}", "") )
# REPLACEMENT_RULES += ( ("\u0081", "") )
# REPLACEMENT_RULES += ( ("\u008D", "") )
# REPLACEMENT_RULES += ( ("\u008F", "") )
# REPLACEMENT_RULES += ( ("\u0090", "") )
# REPLACEMENT_RULES += ( ("\u009D", "") )
# REPLACEMENT_RULES += ( ("\u00A0", "") )
# REPLACEMENT_RULES += ( ("\u00AD", "") )

def get_story_links() -> list:
    story_links = [ ]
    response = requests.get( root_page )
    if response.status_code == 200:
        html = response.text
        page = BeautifulSoup( html, "html.parser" )

        links = page.find_all( "a", href = True )
        for link in links:
            if (link[ 'href' ].startswith( "fiction" )):
                story = link.text
                relative_path = link[ 'href' ]
                href = f'{root_page}/{relative_path}'
                story_links.append( (story, href) )

    return story_links


def write_story( story ):
    title, link = story
    filename = make_filename( title )
    raw_text = get_story_text( link )

    with open( f'{download_dir}/{filename}', "w+" ) as file:
        file.write( raw_text )


def get_story_text( link ):
    story = ''
    response = requests.get( link )
    if response.status_code == 200:
        page = BeautifulSoup( response.text, 'html.parser' )
        paragraphs = list( filter( lambda p: len( p ) > 0, page.find_all( 'br' ) ) )
        for section in paragraphs:
            story += section.text

    return fix_text( story )


def make_filename( title: str ) -> str:
    fixed = fix_text( title ).replace( r'"', '' ).replace( "'", '' )
    formatted = fixed.lower().replace( r'[^a-zA-Z0-9 ]', '' ).replace( r'"', '' ).replace( "'", '' ).replace( ' ', '-' )
    return fix_text( f'{formatted}.txt' )


if __name__ == '__main__':
    download_dir = 'data'

    if exists( download_dir ):
        print( 'removing existing data directory and getting data from scratch' )
        rmtree( download_dir )

    mkdir( download_dir )

    links = get_story_links()

    pool = Pool( 16 )
    pool.map( write_story, links )