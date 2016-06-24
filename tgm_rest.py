# -*- coding: utf-8 -*-

import sys, re, json
from bottle import route, run, template, request, response, post
import urllib, urllib2


ip = '121.254.173.77'
port = 7044


def enable_cors(fn):
  def _enable_cors(*args, **kwargs):
      # set CORS headers
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
      response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

      if request.method != 'OPTIONS':
          # actual request; reply with the actual response
          return fn(*args, **kwargs)
        
  return _enable_cors


@route(path='/tgm', method=['OPTIONS', 'POST'])
@enable_cors
def query():
  #i_text = request.body.read()
  i_text = '{"language": "en", "string": "Which rivers flow through Seoul?"}'
  i_json = json.loads(i_text)
  
  if is_right_input(i_json):
    return "Exception: Input error"

  ''' -------------------- '''
  ''' TGM logic            '''
  ''' -------------------- '''

  o_text = '[{"query": "SELECT ?v4 WHERE { ?v4 ?v2 ?v6 ; ?v7 ?v3 . } ","score": "1.0","slots": [{"o": "rdf:Property","p": "is","s": "v2"},{"o": "flow","p": "verbalization","s": "v2"},{"o": "rdf:Class","p": "is","s": "v3"},{"o": "rivers","p": "verbalization","s": "v3"},{"o": "","p": "is","s": "v7"},{"o": "rdf:Resource|rdfs:Literal","p": "is","s": "v6"},{"o": "Seoul","p": "verbalization","s": "v6"}]}]'
  o_json = json.loads(o_text)

  if is_right_output(o_json):
    return "Exception: Output error"
  
  # Returning the results in JSON format
  #response.headers['Content-type'] = 'application/json'
  return o_text


def is_right_input(x_json):
    try:
      x_json.language
      x_json.string
    except:
      return False
    return True


def is_right_output(x_json):
    try:
      x_json[0].query
      x_json[0].score
      x_json[0].slots
    except:
      return False
    return True


run(host=ip, port=port)