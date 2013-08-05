import sublime, sublime_plugin, json

class FileBinderCommand(sublime_plugin.WindowCommand):

	s = None

	def run(self):

		self.choose_binder()

	def choose_binder(self):

		self.s = sublime.load_settings('FileBinder.sublime-settings').get('binders')
		binders = []

		for item in self.s:
			print(item)
			binders.append(item['name'])

		self.window.show_quick_panel(binders, self.callback_choose_binder)

	def callback_choose_binder(self, index):
		for item in self.s[index]['files']:
			print(item)
			self.window.open_file(item)

	def add_binder(self):
		print('add open files to binder in the settings files + ask for name')

		

	def remove_binder(self): print('list binder like in choose_binder but other callback (delete)')

	def callback_remove_binder(self): print('remove a binder from the settings file')

class AddFileBinderCommand(sublime_plugin.WindowCommand):

	s = None
	binderList = []
	newPathsList = []
	
	def run(self):


		self.window.show_input_panel("Name your binder", "<name>", self.on_done, self.on_change, self.on_cancel)

	def on_done(self, input):

		placeholder = {"name":"Placeholder", "description":"Placeholder", "files": [] }
		# newbinder = {"name":"NIEUW", "desciption":"description 1", "files": ["/C/Home1", "/C/Home4"] }
		
		self.s = sublime.load_settings('FileBinder.sublime-settings')

		binders = self.s.get('binders')

		# if not binders:
		# 	self.s.set('binders', placeholder)
		# 	sublime.save_settings('FileBinder.sublime-settings')
		# 	binders = self.s.get('binders')

		for item in binders: self.binderList.append(item)

		# self.binderList.append(newbinder)

		# jeroen = None

		# Fill binderList with new object, but how?
		for view in self.window.views():
			self.newPathsList.append(view.file_name())

		# print(self.newPathsList)

		conc = {"name": "" + input + "", "description": "jajaja", "files": self.newPathsList}

		self.binderList.append(conc)

		self.s.set('binders', self.binderList)
		
		sublime.save_settings('FileBinder.sublime-settings')



	def on_change(self, input): print("change")

	def on_cancel(self): print("cancel")