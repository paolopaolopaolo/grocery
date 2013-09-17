import os,sys,re,subprocess,ast,json


class Grocery:

  stores=[]
	items=[]
	item_price={}

	def store_stores(self):
		inkput="Y"
		while inkput=="Y":
			store=raw_input("Give me the name of a store!")
			if store not in self.stores:
				self.stores.append(store)
			else:
				print "Try again!\n"
				self.store_stores()
			inkput=raw_input("Would you like to save another store? (Y/N)?").upper()

		print "Thank you!"

		self.menu()

	def price_data(self):
		again="Y"
		#Repeating Menu
		while again=="Y":
			#Set Item Name, Price, and Store
			new_item=raw_input("What is the item?")
			new_price=raw_input("What is the price per unit of that item?")

			#Numbered Menu based on stored Stores
			try:
				storelist=""
				for i in range(1,len(self.stores)+1):
					storelist+= str(i)+"..."+str(self.stores[i-1])+"\n"
				new_store=int(raw_input("Which of the stores below did you buy that item from?\n"+storelist))
				
			except ValueError:
				print "That's no number! Try again"
				self.price_data()

			

			#Adds key to dictionary if it is a new item; inputs new values as well
			if new_item not in self.items:
				self.items.append(new_item)
				self.item_price[new_item]=[]
				try:
					self.item_price[new_item].append((self.stores[new_store-1],new_price))
				except (KeyError,ValueError,IndexError):
					print "Number error! ADD A STORE!"
					self.store_stores()

			#If item is already in dictionary, overwrite if the store is the same.  
			else:
				if self.stores[new_store-1] not in [x[0] for x in self.item_price[new_item]]:
					self.item_price[new_item].append((self.stores[new_store-1],new_price))
				else:
					storevalues=[x[0] for x in self.item_price[new_item]]
					#Overwrite Menu
					question=raw_input("Would you like to change the price of this object from "+str(self.item_price[new_item][storevalues.index(self.stores[new_store-1])][1])+" to "+new_price+"(Y/N)?").upper()
					if question=="N":
						print "Try again!"
						self.price_data()
					elif question=="Y":
						print "DONE!"
						self.item_price[new_item]=[x for x in self.item_price[new_item] if x[0]!=self.stores[new_store-1]]
						self.item_price[new_item].append((self.stores[new_store-1],new_price))
					else:
						print "Try again!"
						self.price_data()
			again=raw_input("Would you like to try again(Y/N)?").upper()

		self.menu()

	def save_data(self):
		print "You have the following items in storage:\n"
		results=""
		itemorder=[key for key in self.item_price if not(key =="stores") and not (key=="items") and len(self.item_price[key])>0]
		for item in self.item_price:
			if item in itemorder:
				results+= "item: "+str(item)+"\n"
				for thing in self.item_price[item]:
					results+= "\t"+"store: "+str(thing[0])+"\tprice: "+str(thing[1])+"\n"
		print results
		inkput=raw_input("Save this data(Y/N)?\n").upper()

		if inkput=="Y":
			if not(self.item_price.has_key("stores")):
				self.item_price["stores"]=self.stores

			if not (self.item_price.has_key("items")):
				self.item_price["items"]=self.items

			saveas=raw_input("Savename (will save in .txt format)?\t")
			x=open(os.path.join("./storage",saveas+".txt"),"w")
			x.write(str(self.item_price))
			x.close
			y=open(os.path.join("./storage","STORES"+saveas+".txt"),"w")
			y.write(str(self.stores))
			y.close
			z=open(os.path.join("./storage/JSON FILES",saveas+".json"),"w")
			with z as outfile:
				json.dump(self.item_price,outfile)
			z.close

		if inkput=="N":
			print "Thank you!"
			self.menu()

	def load_data(self):
		leest=[]
		for item in os.listdir("./storage"):
			if re.search(r".txt",item)!= None and re.search(r"STORES",item)==None:
				leest.append(item)

		print "The following files are in storage:\n"
		for i in range(0,len(leest)):
			print str(i+1)+"..."+str(leest[i])
		try:
			fileopen=int(raw_input("Which file did you wish to access?\t"))
		except ValueError:
			print "Number values only! Try again."
			self.load_data()

		try:
			f=open(os.path.join(os.path.abspath("./storage"),leest[fileopen-1]),"r")
		except IOError:
			print "No such file found!"
			self.menu()
		extract=f.read()
		self.item_price=ast.literal_eval(extract)
		for item in self.item_price:
			self.items.append(item)
		g=open(os.path.join(os.path.abspath("./storage"),"STORES"+leest[fileopen-1]),"r")
		extract=g.read()
		self.stores=ast.literal_eval(extract)

		
		self.menu()

	def edit_data(self):
		print "You have the following items in storage:\n"
		results=""
		itemorder=[key for key in self.item_price if not(key =="stores") and not (key=="items") and len(self.item_price[key])>0]
		for item in self.item_price:
			if item in itemorder:
				results+= "item: "+str(item)+"\n"
				for thing in self.item_price[item]:
					results+= "\t"+"store: "+str(thing[0])+"\tprice: "+str(thing[1])+"\n"
		print results
		
		opt=raw_input("To change the price of an item, type in \"CHG [item]*[store]*[newprice]\".\nTo delete an item, type in \"DEL [item]*[store]\" \n")
		changematch=re.search(r"[Cc][Hh][Gg][ ]*([\w\d ]+)\*([\w\d ]+)\*([.\d]+)",opt)
		deletematch=re.search(r"[Dd][Ee][Ll][ ]*([\w\d ]+)\*([\w\d ]+)",opt)
		
		if changematch != None :
			self.item_price[changematch.group(1)]=[x for x in self.item_price[changematch.group(1)] if x[0] !=changematch.group(2)]
			self.item_price[changematch.group(1)].append((changematch.group(2),changematch.group(3)))
			print "CHG SUCCESS"
		elif deletematch != None:
			self.item_price[deletematch.group(1)][:]=[x for x in self.item_price[deletematch.group(1)] if x[0]!=deletematch.group(2)]
			print "DEL SUCCESS"
		else:
			print "ERROR"
			self.menu()

	def show_data(self):
		for key in [x for x in sorted(self.items) if x!='stores' and x!='items']:
			print key
			for itemprice in [x for x in self.item_price[key] if len(x)==2]:
				print "\t"+str(itemprice[0])+"..."+str(itemprice[1])
		
		self.menu()


	def menu(self):
		choix=raw_input("Welcome to Grocery App 1.0!\nChoose from the following items:\n\tSHOW data\n\tSave a STORE\n\tINPUT price data\n\tEDIT data\n\tEXIT app\n\tSAVE data\n\tLOAD data\n\n\t").upper()
		if choix=="STORE":
			self.store_stores()
		if choix=="INPUT":
			self.price_data()
		if choix=="SAVE":
			self.save_data()
		if choix=="EDIT":
			self.edit_data()
		if choix=="EXIT":
			sys.exit(0)
		if choix=="LOAD":
			self.load_data()
		if choix=="SHOW":
			self.show_data()
		else:
			self.menu()




def main():
	if os.path.exists("./storage")==True:
		x=Grocery()
		x.menu()
	else:
		os.mkdir("./storage")
		os.mkdir("./storage/JSON FILES")
		main()


if __name__=="__main__":
	main()
