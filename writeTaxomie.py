#!/usr/bin/env python

import logging

from parser import DmozParser
from handlers import JSONWriter
from handlers import TaxonomieWriter

logger = logging.getLogger(__name__)

logging.basicConfig(
	format='%(asctime)s : %(levelname)s : %(module)s:%(funcName)s:%(lineno)d : %(message)s',
      	level=logging.INFO)

parser = DmozParser()
parser.input_path = '../content.rdf.u8.gz'
parser.add_handler(TaxonomieWriter('output.json'))
parser.run()
