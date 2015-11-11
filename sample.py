#!/usr/bin/env python

from parser import DmozParser
from handlers import JSONWriter
from handlers import TaxonomieWriter


parser = DmozParser()
parser.input_path = '../content.rdf.u8.gz'
parser.add_handler(TaxonomieWriter('output.json'))
parser.run()
