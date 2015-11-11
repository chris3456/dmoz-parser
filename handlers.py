import copy
import json
import logging
import os
import urllib2

from smart_open import smart_open

logger = logging.getLogger(__name__)


class JSONWriter:
    def __init__(self, name):
        self._file = smart_open(name, 'w')

    def page(self, page, content):
        if page is not None and page != "":
           	if content["topic"] == "Top/World/Deutsch/Computer/Programmieren/Werkzeuge/Versionskontrolle":
			newcontent = copy.copy(content)
            		newcontent["url"] = page
            		self._file.write(json.dumps(newcontent) + "\n")
	    	else:
			logger.info("Skipping page %s, wrong topic", page)	
        else:
            logger.info("Skipping page %s, page attribute is missing", page)

    def finish(self):
        self._file.close()


class TaxonomieWriter:
    def __init__(self, name):
        self._file = smart_open(name, 'w')

    def page(self, page, content):
        if page is not None and page != "":
            	if check(content["topic"]):
			directory = "./" + content["topic"] 
			if not os.path.exists(directory):
				os.makedirs(directory)
			try:
				response = urllib2.urlopen(page)
				htmlContent = response.read()
				f = open (directory + "/" + content["d:Title"] + ".txt", 'w')
				f.write(htmlContent)
				f.close()
			except Exception as e:
				logger.info("Skipping page %s, Error: %e", page)
	    	else:
			logger.info("Skipping page %s, wrong topic", page)	
        else:
            logger.info("Skipping page %s, page attribute is missing", page)


    def checkTopic(topic):
	topics = ["Top/Computers","Top/Science", "Top/World/Deutsch/Computer", "Top/World/Deutsch/Wissenschaft"]
	match = false
	for t in topics:
		if t in topic:
			match = true
	
	return match


    def finish(self):
        self._file.close()


class CSVWriter:
  # Note: The CSVWriter has several bugs and assumptions, as documented below.
    def __init__(self, name):
        self._file = smart_open(name, 'w')

    def page(self, page, content):
        if page is not None and page != "":
            page = page.encode("utf-8")
            page = page.replace('"', '')
            page = page.replace('&quot;', '')

            self._file.write('"%(page)s"' % {'page': page})
            # for type in content:
            # For CSV, read only these fields, in only this order.
            newcontent = {}
            for type in ['d:Title', 'd:Description', 'priority', 'topic']:
                newcontent[type] = content[type].encode("utf-8")
                newcontent[type] = newcontent[type].replace('"', '')
                newcontent[type] = newcontent[type].replace('&quot;', '')
                # BUG: Convert comma to something else? Otherwise, it will trip up the CSV parser.
                self._file.write(',"%s"' % newcontent[type])

            self._file.write("\n")
        else:
            logger.info("Skipping page %s, page attribute is missing", page)

    def finish(self):
        self._file.close()
