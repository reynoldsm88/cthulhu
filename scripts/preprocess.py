#!/usr/bin/env python3

import re
from multiprocessing import Pool
from os.path import exists
from os import listdir
from typing import List, Tuple
from os import mkdir
import spacy
from ftfy import fix_text

from shutil import rmtree

from core.common import raw_data_dir, preprocess_data_dir, confirm_loop

sentence_splitter = spacy.load( 'en_core_web_sm' )


def split_sentences( text: str ) -> List[ str ]:
    doc = sentence_splitter( text )
    sentences = [ ]
    [ sentences.append( s.text ) for s in doc.sents ]

    return sentences


def cleanup( text: str ):
    # get rid of all kinds of nasty unicode nonsense
    text = fix_text( text )
    text = re.sub( r'X{0,3}V{0,3}I{0,3}V{0,3}\.\n', '', text )
    text = re.sub( r'http(s)?:.*\w', '', text ).strip()
    text = text.lower()
    text = text.replace( u'\u2014', ' ' )
    text = text.replace( '-', ' ' )
    text = text.replace( "*", ' ' )

    text = text.replace( u'\u0000', ' ' )
    text = text.replace( u'\u0001', ' ' )
    text = text.replace( u'\u0002', ' ' )
    text = text.replace( u'\u0003', ' ' )
    text = text.replace( u'\u0004', ' ' )
    text = text.replace( u'\u0005', ' ' )
    text = text.replace( u'\u0006', ' ' )
    text = text.replace( u'\u0007', ' ' )
    text = text.replace( u'\u0008', ' ' )

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
    text = text.replace( "\n", " " )

    text = text.replace( "'", "" )
    text = text.replace( '"', "" )

    text = text.replace( ",", '' )
    text = text.replace( ";", '' )
    text = text.replace( ':', ' ' )
    text = text.replace( "(", "" )
    text = text.replace( ")", "" )
    text = text.replace( '...', '.' )
    text = text.replace( "[\. ]{2,}", " " )

    text = text.replace( '\s{2,}', ' ' )

    return text


def preprocess( doc: Tuple[ str, str ] ):
    filename, text = doc
    cleaned_text = cleanup( text )
    sentences = split_sentences( cleaned_text )
    with open( f'{preprocess_data_dir}/{filename}', '+w' ) as out:
        [ out.write( f'{line}\n' ) for line in sentences ]


def get_corpus() -> List[ Tuple[ str, str ] ]:
    files = listdir( raw_data_dir )
    corpus = [ ]

    for file in files:
        with open( f'{raw_data_dir}/{file}' ) as story:
            text = story.read()
            corpus.append( (file, text) )

    return corpus


def do_preprocessing():
    if not exists( raw_data_dir ):
        print( 'there is no raw data present, cannot preprocess what doesnt exist' )
        exit( 1 )

    if exists( preprocess_data_dir ):
        rmtree( preprocess_data_dir )

    mkdir( preprocess_data_dir )

    pool = Pool( 20 )
    pool.map( preprocess, get_corpus() )


if __name__ == '__main__':
    if exists( preprocess_data_dir ):
        confirm_loop( "the data has already been pre-processed. would you like to delete and reprocess from scratch? y/n", do_preprocessing )
    else:
        do_preprocessing()