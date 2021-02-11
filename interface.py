from  io import BytesIO
from time import time
from requests import get,post
from tkinter import *
from bs4 import BeautifulSoup
from pandas import DataFrame,concat,read_csv
from os import listdir,path

class UI():
	"""docstring for UI"""
	def __init__(self,scraper):
		# to call functions of scraper class using ui
		self.scraper = scraper
		# root ui
		self.root = Tk()
		self.root.minsize(400,300)
		self.create_layout()

	def create_layout(self):
		# top text
		topFrame = Frame(self.root)
		Label(topFrame,text="SBI Scraper").pack()
		topFrame.pack()

		# current data page
		self.primary_field = StringVar()
		self.secondary_field = StringVar()
		current_fields = Frame(self.root)
		Label(current_fields,textvariable=self.primary_field).pack(side=RIGHT,padx=30)
		Label(current_fields,textvariable=self.secondary_field).pack(side=LEFT,padx=30)
		current_fields.pack()
	
		# show captcha
		imageFrame = Frame(self.root)
		self.image = PhotoImage(data = open("welcome.png","rb").read())
		self.photoLabel = Label(imageFrame,image=self.image)
		self.photoLabel.pack(padx=20,pady=20)
		imageFrame.pack(fill=None,expand=False)

		# fill captch
		self.captcha = StringVar()
		valueFrame = Frame(self.root)
		self.entry = Entry(valueFrame,textvariable=self.captcha)
		self.entry.pack()
		Button(valueFrame, text="try", width=10, command=self.process).pack()
		valueFrame.pack(pady=20)

		# navigation buttons
		buttonFrame = Frame(self.root)
		Button(buttonFrame, text="Start",command=self.StartAction).pack(side="left")
		Button(buttonFrame, text="Create one CSV",command=self.SaveAction).pack(side="left")
		Button(buttonFrame, text="Exit",command=self.ExitAction).pack(side="left")
		buttonFrame.pack(pady=20)

		# log area
		self.scrollbar = Scrollbar(self.root)
		self.scrollbar.pack(side=RIGHT,fill=BOTH)
		self.logList = Listbox(self.root,yscrollcommand=self.scrollbar.set,width=65)
		self.logList.pack(side=LEFT,fill=BOTH)
		self.scrollbar.config(command=self.logList.yview)

		# initial field values
		self.primary_field.set("primary field")
		self.secondary_field.set("secondary field")

	#insert a log
	def log(self,msg):
		self.logList.insert(END,msg)
		self.logList.see(END)

	# update captcha image (image file io object to be passed)
	def update_image(self,image_object):
		image = PhotoImage(data=image_object.read())
		self.photoLabel.configure(image=image)
		self.photoLabel.image = image
		
	# combine in database
	def SaveAction(self):
		database = DataFrame()
		self.log("[+] creating single database ....")
		for file in listdir("data"):
		    csv = read_csv("/".join(["data",file]),index_col=0)
		    database = concat([database,csv],ignore_index=True)
		database.to_csv("sbi_employee_dataset.csv")
		self.log("Done")

	# START
	def StartAction(self):
		# get index page with form
		self.scraper.get_primary_fields()

		png = self.scraper.get_Captcha()
		self.update_image(png)

		self.log("[+] available primary fields :-")
		for field in self.scraper.primary_fields:
			self.log(field)

		self.next_field()

		self.entry.focus()

		self.root.bind('<Return>',self.process)

	# you know very well what it does
	def ExitAction(self):
		self.root.destroy()
		sys.exit()

	# sets next field to be requested if previous on is save successfully
	def next_field(self):
		if len(self.scraper.secondary_fields):
			self.secondary_field.set(self.scraper.secondary_fields.pop(0))
		elif len(self.scraper.primary_fields):
			self.primary_field.set(self.scraper.primary_fields.pop(0))
			self.logList.insert(END,"[+] selecting primary field : " + self.primary_field.get())
			self.scraper.select_primary_field(self.primary_field.get())
			self.secondary_field.set(self.scraper.secondary_fields.pop(0))
		else:
			self.log("Scrapping Done")
			return 1
		if path.exists("".join(["data/",self.primary_field.get(),"_",self.secondary_field.get().replace("/","-"),".csv"])):
			self.log(self.primary_field.get()+" > "+self.secondary_field.get() + " exists")
			self.next_field()

	# request current fileds along with filled captcha value and save data in a file
	def process(self,event=None):
		# read captch value
		value = self.captcha.get() 
		self.entry.delete(0,'end')
		pf = self.primary_field.get()
		sf = self.secondary_field.get()
		x = self.scraper.get_data(pf,sf,value)
		if x:
			n = "".join(["data/",pf,"_",sf.replace("/","-"),".csv"])
			x[0].to_csv(n)
			self.log(sf + " saved, length : " + str(len(x[0])))
			self.next_field()
		else:
			self.log("Faied try again")
		# update captcha for next action
		png = self.scraper.get_Captcha()
		self.update_image(png)