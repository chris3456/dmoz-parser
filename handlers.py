import copy
import json
import logging
import os
import urllib2
import html2text

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
        h = html2text.HTML2Text()
	h.ignore_links = True

	if page is not None and page != "":
            	topic = content ['topic']
		if self.checkTopic(topic):
			directory = "./" + topic 
			if not os.path.exists(directory):
				os.makedirs(directory)
			try:
				file_path = directory + "/" + content["d:Title"] + ".txt"
				if not os.path.exists(file_path):
					response = urllib2.urlopen(page, timeout=10)
					htmlContent = response.read()
					f = open (file_path, 'w')
					f.write(h.handle(htmlContent))
					f.close()
					logging.info("Downloaded: %s", page)
			except Exception as e:
				logger.warn("Skipping page %s, Error: %s", page, e)
	    	else:
			logger.info("Skipping topic %s", topic)	
        else:
            logger.info("Skipping page %s, page attribute is missing", page)


    def checkTopic(self, topic):
	topics = ["Top/Computers","Top/Science", "Top/World/Deutsch/Computer", "Top/World/Deutsch/Wissenschaft"]
	match = False
	for t in topics:
		if t in topic:
			match = True
			break
	
	return match


    def finish(self):
        self._file.close()


