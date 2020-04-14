#!/usr/bin/env python3

import re
from multiprocessing import Pool
from os import mkdir
from os.path import exists
from shutil import rmtree

import requests
from bs4 import BeautifulSoup
from ftfy import fix_text

root_page = 'http://www.hplovecraft.com/writings/texts'


def get_story_links() -> list:
    story_links = [ ]
    response = requests.get( root_page )
    if response.status_code == 200:
        html = response.text
        page = BeautifulSoup( html, "html.parser" )

        html_links = page.find_all( "a", href = True )
        for link in html_links:
            if link[ 'href' ].startswith( "fiction" ):
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

    return cleanup( fix_text( story ) )


def cleanup( text: str ):
    # get rid of all kinds of nasty unicode nonsense
    text = text.replace( u'\u2014', ' ' )
    text = text.replace( '-', ' ' )

    text = text.replace( u'\u0000', '' )
    text = text.replace( u'\u0001', '' )
    text = text.replace( u'\u0002', '' )
    text = text.replace( u'\u0003', '' )
    text = text.replace( u'\u0004', '' )
    text = text.replace( u'\u0005', '' )
    text = text.replace( u'\u0006', '' )
    text = text.replace( u'\u0007', '' )
    text = text.replace( u'\u0008', '' )

    text = text.replace( u'\u000B', '' )
    text = text.replace( u'\u000C', '' )
    text = text.replace( u'\u000D', '' )
    text = text.replace( u'\u000E', '' )
    text = text.replace( u'\u000F', '' )
    text = text.replace( u'\u0010', '' )
    text = text.replace( u'\u0011', '' )
    text = text.replace( u'\u0012', '' )
    text = text.replace( u'\u0013', '' )
    text = text.replace( u'\u0014', '' )
    text = text.replace( u'\u0015', '' )
    text = text.replace( u'\u0016', '' )
    text = text.replace( u'\u0017', '' )
    text = text.replace( u'\u0018', '' )
    text = text.replace( u'\u0019', '' )
    text = text.replace( u'\u0019', '' )
    text = text.replace( u'\u001A', '' )
    text = text.replace( u'\u001B', '' )
    text = text.replace( u'\u001C', '' )
    text = text.replace( u'\u001D', '' )
    text = text.replace( u'\u001E', '' )
    text = text.replace( u'\u001F', '' )

    text = text.replace( u'\u0081', '' )
    text = text.replace( u'\u008D', '' )
    text = text.replace( u'\u008F', '' )
    text = text.replace( u'\u0090', '' )
    text = text.replace( u'\u009D', '' )
    text = text.replace( u'\u00A0', '' )
    text = text.replace( u'\u00AD', '' )

    # remove the chapter headings
    return re.sub( r'X{0,3}V{0,3}I{0,3}V{0,3}\.\n', '', text ).strip()


def make_filename( title: str ) -> str:
    fixed = fix_text( title ).replace( r'"', '' ).replace( "'", '' )
    formatted = fixed.lower().replace( r'[^a-zA-Z0-9 ]', '' ).replace( r'"', '' ).replace( "'", '' ).replace( ' ', '-' )
    return fix_text( f'{formatted}.txt' )


if __name__ == '__main__':
    data_dir = "data"
    download_dir = f"{data_dir}/raw"

    if not exists( data_dir ):
        mkdir( data_dir )

    if exists( download_dir ):
        print( 'removing existing data directory and getting data from scratch' )
        rmtree( download_dir )

    mkdir( download_dir )

    links = get_story_links()

    pool = Pool( 16 )
    pool.map( write_story, links )