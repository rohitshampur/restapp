from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from urlparse import urlparse, parse_qs
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from io import BytesIO
from xml.etree import ElementTree
import json


users = Element('users')
def hello(request):
    return Response('Hello world!')

def write(username,passwd):
	print 'Writng data to file'
	file = open('user.xml','w')
	user = SubElement(users, 'user')
	user.attrib["username"] = username 
	user.attrib["password"] = passwd
	file.write(prettify(users))
	file.close()
	
def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem 

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent=" ")

def login(request):
    tree = ElementTree.parse('user.xml')
    root = tree.getroot()
    o = urlparse(request.url)
    query = parse_qs(o.query)
    param1 = query.get('user')
    param2 = query.get('pass')
    username =  param1[0]
    passwd =  param2[0]
    res = False
    for child in root:
	if child.attrib['username'] == username:
		if child.attrib['password'] == passwd:
			res = True
    if res:
	return Response(getsuccess())
    else:
        return Response(getfailure())

def getfailure():
	with open('failure.json') as json_data:
	    d = json.load(json_data)
	    json_data.close()
	    jsonString = json.dumps(d)
	    return jsonString

def getsuccess():
	with open('success.json') as json_data:
	    d = json.load(json_data)
	    json_data.close()
	    jsonString = json.dumps(d)
	    return jsonString

def register(request):
    o = urlparse(request.url)
    query = parse_qs(o.query)
    param1 = query.get('user')
    param2 = query.get('pass')
    username =  param1[0]
    passwd =  param2[0]
    write(username,passwd)
    return Response(getsuccess())

	

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello_world', '/')
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.add_view(hello, route_name='hello_world')
    config.add_view(login, route_name='login')
    config.add_view(register, route_name='register')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    print 'Server started on port localhost:8080'
    server.serve_forever()
