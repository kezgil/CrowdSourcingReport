#oggpnosn
#hkhr

import webapp2
from lib import BaseHandler, NGO, Project, User
import random 
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import ndb

class HomePageHandler(BaseHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			userid = user.user_id()
			userAuthentication =  User.query(User.userid == userid).fetch(1)
			ngoAuthentication = NGO.query(NGO.userid == userid).fetch(1)
			if userAuthentication:
				self.render("userHomePage.html")
			elif ngoAuthentication:
				self.render("ngoHomePage.html")
			else:
				self.redirect("/signup/registration")
		else:
			self.redirect("/")
	
class ProjectUpdateHandler(BaseHandler):
	def get(self):
		user = users.get_current_user()
                if user:
                        userid = user.user_id()
                        userAuthentication =  User.query(User.userid == userid).fetch(1)
                        if userAuthentication:
				parameter = {}
				userObject = userAuthentication[0]
				projectsIdentifier = userObject.projects[:10]
				projects = []
				for projectIdentifier in projectsIdentifier:
					key = ndb.Key("Project", projectIdentifier)
					projects.append(key.get())
				parameter["projects"] = projects
                                self.render("projectUpdate.html", parameter)
                        else:
                                self.redirect("/")
                else:   
                        self.redirect("/login")
	
class UpdateProjectHandler(BaseHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			userid = user.user_id()
			userAuthentication = NGO.query(NGO.userid == userid).fetch(1)
			if userAuthentication:
				parameter={}
				ngo = userAuthentication[0]
				projectsIdentifierList = ngo.projects
				projects = []
				for projectIdentifier in projectsIdentifierList:
					ngo, title = self.stripProjectIdentifier(projectIdentifier)
					projectObject = Project.query(Project.ngo == ngo, Project.title == title).fetch(1)[0]
					projects.append(projectObject)
				parameter["projects"] = projects
				self.render("updateProject.html", parameter)
			else:
				self.redirect("/")	
		else:
			self.redirect("/login")
		
                
app = webapp2.WSGIApplication([('/home', HomePageHandler),('/home/ProjectUpdate',ProjectUpdateHandler),('/home/UpdateProject', UpdateProjectHandler)])



