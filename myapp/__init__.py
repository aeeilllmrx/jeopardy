from flask import Flask
app = Flask(__name__)
import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import myapp.views
