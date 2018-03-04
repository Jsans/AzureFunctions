# Name : resize image to needed size based on request and save to blob.
# Created by : Jathisan Chandrasegaram


#################################################################################################################
# IMPORTS
#################################################################################################################
#Standard Python 3.6.x
import os
from json import dumps,loads
from collections import defaultdict
from urllib.parse import urlparse, parse_qs,urlencode
from datetime import datetime
from azure.storage.blob import BlockBlobService
from PIL import Image
import io
import base64

#################################################################################################################
# store data
#################################################################################################################
##### get blob environment
name=os.environ.get('blob_name')
key=os.environ.get('blob_key')
block_blob_service = BlockBlobService(account_name=name, account_key=key)

#################################################################################################################
# HTTP queries , parse the get url to a dict 
#################################################################################################################
query=os.environ.get('REQ_QUERY')

request_fn=defaultdict(str,size=None,image=None)
request_=parse_qs(urlparse(query).query)
request_fn.update(request_)

#################################################################################################################
# FUNCTION
#################################################################################################################

#get image from blob or resize it
img_file=str(request_fn['image'][0])
if request_fn['size']!=None:
    size=32
    size= int(request_fn['size'][0])
    try:
        
        d=block_blob_service.get_blob_to_bytes('master',"%s_" % str(size) +img_file)
        print('in blob')
        stream = io.BytesIO(d.content)
        img = Image.open(stream)
        out= io.BytesIO()
        img.save(out,format="png")
        data_uri=base64.b64encode(out.getvalue())
    except:
        print('not in master blob')
        d=block_blob_service.get_blob_to_bytes('incontainer',img_file)
        stream = io.BytesIO(d.content)
        basewidth = size
        img = Image.open(stream)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        out= io.BytesIO()
        img.save(out,format="png")
        block_blob_service.create_blob_from_bytes('master',"%s_" % str(size) +img_file,out.getvalue())
        data_uri=base64.b64encode(out.getvalue())

if request_fn['size']==None:
    d=block_blob_service.get_blob_to_bytes('incontainer', img_file)
    stream = io.BytesIO(d.content)
    img = Image.open(stream)
    out= io.BytesIO()
    img.save(out,format="png")
    data_uri=base64.b64encode(out.getvalue())


#################################################################################################################
# HTML RESPONSE back from azure functions
#################################################################################################################



img=str("<img src='data:image/png;base64," +str(data_uri.decode("utf-8") ) + "'/>")
returnData = {
    #HTTP Status Code:
    "status": 200,
    
    #Response Body:
    "body": img,
    # Send any number of HTTP headers
    "headers": {
        "Content-Type": 'text/html',
    }
}
open(os.environ['res'], 'w').write(dumps(returnData))