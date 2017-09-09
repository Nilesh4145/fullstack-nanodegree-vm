import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session=DBSession()

restaurants = []
[restaurants.append(restaurant.name) for restaurant in session.query(Restaurant).all()]


def main():
	try:
		port=5000
		server=HTTPServer(("",port), webserverHandler)
		print "Web Server is running on port %s" % port
		server.serve_forever()


	except KeyboardInterrupt:
		print "^C entered, stopping web browser"
		server.socket.close()


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>Hello!!"
				#output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?<h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>You are at index page!!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?<h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				for restaurant in restaurants:
					output += restaurant
					output += "</br>"
				output += "</body></html>"
				self.wfile.write(output)
				print(output)
				return


		except IOError:
			self.send_error(404, "File Not Found %s" %self.path)


	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			print ctype
			print pdict
			if ctype == 'multipart/form-data':
				print self.rfile
				print pdict
				fields=cgi.parse_multipart(self.rfile, pdict)
				print fields
				messagecontent = fields.get('message')
				print messagecontent

			output = ""
			output += "<html><body>"
			output += "<h2> Okay, How about this: </h2>"
			output += "<h1> %s </h2>" % messagecontent[0]
			output += "<form method='POST' enctype='multipart/form-data' action='/'><h2>What would you like me to say?<h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
			output += "</body></html>"
			self.wfile.write(output)
			print output

		except:
			pass

if __name__ == "__main__":
	main()
