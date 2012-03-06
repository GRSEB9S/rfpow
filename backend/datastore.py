import logging
from datetime import datetime
from google.appengine.ext import db

class RFP(db.Model):
    title = db.StringProperty()
    description = db.TextProperty()
    keywords = db.StringListProperty()
    organization = db.StringProperty()
    original_uri = db.StringProperty()
    original_id = db.StringProperty()
    origin = db.StringProperty()
    publish_date = db.DateProperty()
    parse_date = db.DateProperty()
    close_date = db.DateProperty()

    @classmethod
    def from_dict( self, dict ):
        """Create an RFP based on a dictionary as received from a parser"""
        rfp = RFP()

        rfp.title = dict['title']
        rfp.description = dict['description']
        rfp.keywords = [dict['original_category']]
        rfp.organization = dict['org']
        rfp.original_uri = dict['uri']
        rfp.original_id = dict['original_id']
        rfp.origin = dict['origin']
        rfp.publish_date = dict['published_on']
        rfp.parse_date = dict['parsed_on']
        rfp.close_date = dict['ends_on']

        return rfp

    @classmethod
    def by_original_id(self, origin, id):
        return RFP.gql("WHERE original_id = :1", id)
    
    def __str__(self):
        return u"<RFP Object: '%s'>" % self.title


def create_RFP(title, description, keywords, organization, original_uri, original_id, publish_date, parse_date, close_date):
    rfp = RFP()

    rfp.title = title
    rfp.description = description
    rfp.keywords = keywords
    rfp.organization = organization
    rfp.original_uri = original_uri
    rfp.original_id = original_id
    rfp.publish_date = publish_date
    rfp.parse_date = parse_date
    rfp.close_date = close_date
    
    rfp.put()

def query_RFPs_by_keyword(keyword):
    return RFP.gql("WHERE keywords = '{0}'".format(keyword))

def query_RFPs(query):
    return RFP.gql(query)

def query_Keywords(keyword):
    c = db.GqlQuery('SELECT * FROM RFP')
    keywords = []
    for entity in c:
	if entity.keywords not in keywords and entity.keywords[0] != "":
	    keywords.append(entity.keywords)
	
    keywords.sort()
    
    return keywords

def form_printable(rfps):
    for r in rfps:
        r['detail'] = "<b>Origin: </b>" + r['origin'] + '<br /><br />'\
			+ "<b>Organization: </b>" + r['organization'] + \
			'<br /><br />' + "<b>Publish date: </b>" + str(r['publish_date'])\
			+ "Close date: " + str(r['close_date']) + '<br /><br />' +\
			"<b>URL: </b>" + r['uri'] + '<br /><br />' + "<b>Description: </b>"\
			+ r['description'] + '<br /><br />'
    return rfps

def form_top_printable(rfps):
    for r in rfps:
        r['detail'] = "<b>Origin: </b>" + r['origin'] + '<br /><br />'\
			+ "<b>Organization: </b>" + r['org'] + \
			'<br /><br />' + "<b>Publish date: </b>" + str(r['published_on'])\
			+ "Close date: " + str(r['ends_on']) + '<br /><br />' +\
			"<b>URL: </b>" + r['uri'] + '<br /><br />' + "<b>Description: </b>"\
			+ r['description'] + '<br /><br />'
    return rfps
