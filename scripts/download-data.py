#!/usr/bin/env python3

from multiprocessing import Pool
from os.path import exists

import requests
from bs4 import BeautifulSoup
from ftfy import fix_text

from os import mkdir

from shutil import rmtree

from core.common import raw_data_dir, confirm_loop

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

    with open( f'{raw_data_dir}/{filename}', "w+" ) as file:
        file.write( raw_text )


def get_story_text( link ):
    story = ''
    response = requests.get( link )
    if response.status_code == 200:
        page = BeautifulSoup( response.text, 'html.parser' )
        paragraphs = list( filter( lambda p: len( p ) > 0, page.find_all( 'br' ) ) )
        for section in paragraphs:
            story += section.text

    return story


def make_filename( title: str ) -> str:
    fixed = fix_text( title ).replace( r'"', '' ).replace( "'", '' )
    formatted = fixed.lower().replace( r'[^a-zA-Z0-9 ]', '' ).replace( r'"', '' ).replace( "'", '' ).replace( ' ', '-' )
    return fix_text( f'{formatted}.txt' )


def do_download():
    if exists( raw_data_dir ):
        rmtree( raw_data_dir )

    mkdir( raw_data_dir )
    [ write_story( link ) for link in get_story_links() ]


if __name__ == '__main__':

    if exists( raw_data_dir ):
        confirm_loop( f"the directory {raw_data_dir} already exists, would you like to overwrite?", do_download )
    else:
        do_download()