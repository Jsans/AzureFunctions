#!/usr/bin/env python
# Created by : Jathisan Chandrasegaram

#################################################################################################################
# IMPORTS
#################################################################################################################
import os
import json
import jinja2
from collections import defaultdict
from urllib.parse import urlparse, parse_qs
#################################################################################################################
# Global 
#################################################################################################################

#print(os.environ['YOURAPPSETTING'])


#################################################################################################################
# GET : HTTP queries , parse the get url to a dict 
#################################################################################################################
query=os.environ.get('REQ_QUERY')

request_fn=defaultdict(str,code=None)
request_=parse_qs(urlparse(query).query)
request_fn.update(request_)

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

#################################################################################################################
# HTTP queries
#################################################################################################################
try:
    req = request_fn['req'][0]
except:
    req="error"

#################################################################################################################
# FUNCTION
#################################################################################################################
items=[]


context = {
    'firstname': '%s' % (req),
    'items': items
}


# Jinja2 render the defined HTML
result = render('./index.html', context)

#################################################################################################################
# HTML RESPONSE back from azure functions
#################################################################################################################

# Format Data to return as HTML
returnData = {
    #HTTP Status Code:
    "status": 200,
    
    #Response Body:
    "body": result ,
    # Send any number of HTTP headers
    "headers": {
        "Content-Type": "text/html",
        "X-Awesome-Header": "YesItIs"
    }
}

# Output the response to the client
output = open(os.environ['res'], 'w')
output.write(json.dumps(returnData))