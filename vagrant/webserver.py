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
				output += "</br></br><a href=/restaurants/new>Add Restaurant</a></br></br></br>"
			
				for restaurant in session.query(Restaurant).all():
					output += restaurant.name
					output += "</br>"
					output += "<a href=/restaurants/%s/edit>Edit</a></br><a href=/restaurants/%s/delete>Delete</a></br></br>" %(restaurant.id, restaurant.id)
				output += "</body></html>"
				self.wfile.write(output)
				return

			
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Add a Restaurant</h2><input name='newRestaurantName' type='text' placeholder='New Restaurant Name'><input type='submit' value='Add Restaurant'></form></br>"
				self.wfile.write(output)
				return


			if self.path.endswith("/edit"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				restaurant_id = self.path.split('/')[2]
				restaurant_name = session.query(Restaurant).filter_by(id = restaurant_id).one().name
				print restaurant_name
				output = ""
				output += "<html><body><h1> Edit Details of %s" %restaurant_name
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><input name='newName' type='text' placeholder='New Name'><input type='submit' value='Update'></form></br>" %restaurant_id
				self.wfile.write(output)
				return


			if self.path.endswith("/delete"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				restaurant_id = self.path.split('/')[2]
				restaurant_name = session.query(Restaurant).filter_by(id = restaurant_id).one().name
				print restaurant_name
				output = ""
				output += "<html><body><h1> Are you sure you want to delete the details of %s" %restaurant_name
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><input type='submit' value='Delete'></form></br>" %restaurant_id
				self.wfile.write(output)
				return

		except IOError:
			self.send_error(404, "File Not Found %s" %self.path)


	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('newRestaurantName')
				
				newRestaurant = Restaurant(name=messagecontent[0])
				session.add(newRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-Type',	'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()


			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('newName')
				
				restaurant_id = self.path.split('/')[2]
				updated = session.query(Restaurant).filter_by(id = restaurant_id).one()
				print updated
				updated.name = messagecontent[0]
				print updated.name
				session.add(updated)
				session.commit()

				self.send_response(301)
				self.send_header('Content-Type',	'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()


			if self.path.endswith("/delete"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

				restaurant_id = self.path.split('/')[2]
				to_delete = session.query(Restaurant).filter_by(id = restaurant_id).one()
				
				if to_delete != []:
					session.delete(to_delete)
					session.commit()
					self.send_response(301)
					self.send_header('Content-Type',	'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

			# if ctype == 'multipart/form-data':
			# 	fields=cgi.parse_multipart(self.rfile, pdict)
			# 	messagecontent = fields.get('message')

			# output = ""
			# output += "<html><body>"
			# output += "<h2> Okay, How about this test: </h2>"
			# output += "<h1> %s </h2>" % messagecontent[0]
			# output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/test'><h2>What would you like me to say?<h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
			# output += "</body></html>"
			# self.wfile.write(output)

		except:
			pass

if __name__ == "__main__":
	main()
