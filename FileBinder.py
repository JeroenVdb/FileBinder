import sublime, sublime_plugin, json

class FileBinderCommand(sublime_plugin.WindowCommand):

	s = None

	def run(self):

		self.choose_binder()

	def choose_binder(self):

		# Gather all binder names
		self.s = sublime.load_settings('FileBinder.sublime-settings').get('binders')
		binderNameList = []
		for item in self.s: binderNameList.append(item['name'])

		# Choose your binder
		if len(binderNameList) > 0:
			self.window.show_quick_panel(binderNameList, self.callback_choose_binder)
		else:
			self.window.show_quick_panel(["You dont have any binders yet"], None)

	def callback_choose_binder(self, index):

		if not index == -1:

			for item in self.s[index]['files']:
				self.window.open_file(item)

class AddFileBinderCommand(sublime_plugin.WindowCommand):

	s = None
	binderList = []
	newPathsList = []
	
	def run(self):

		self.binderList = []

		self.window.show_input_panel("Name your binder", "<name>", self.on_done, self.on_change, self.on_cancel)

	def on_done(self, input):

		self.s = sublime.load_settings('FileBinder.sublime-settings')

		# Gather existing binders in binderList
		binders = self.s.get('binders')
		for item in binders: self.binderList.append(item)

		# Extend binderList with new binder
		for view in self.window.views():
			self.newPathsList.append(view.file_name())
		jsonStr = {"name": "" + input + "", "description": "", "files": self.newPathsList}
		self.binderList.append(jsonStr)

		# Save them all, clear first
		self.s.set('binders', "")
		self.s.set('binders', self.binderList)
		sublime.save_settings('FileBinder.sublime-settings')

	def on_change(self, input): print("change")

	def on_cancel(self): print("cancel")

class RemoveFileBinderCommand(sublime_plugin.WindowCommand): 

	s = None
	binderList = []

	def run(self):

		self.binderList = []

		self.choose_binder()

	def choose_binder(self):

		# Gather all binder names
		self.s = sublime.load_settings('FileBinder.sublime-settings').get('binders')
		binderNameList = []
		for item in self.s: binderNameList.append(item['name'])

		# Choose your binder
		if len(binderNameList) > 0:
			self.window.show_quick_panel(binderNameList, self.callback_choose_binder)
		else:
			self.window.show_quick_panel(["You dont have any binders yet"], None)

	def callback_choose_binder(self, index):

		if not index == -1:

			# Gather all binder but the one to remove
			self.s = sublime.load_settings('FileBinder.sublime-settings').get('binders')
			for i, item in enumerate(self.s):
				if i != index:
					self.binderList.append(item)

			# Save them all, clear first
			sublime.load_settings('FileBinder.sublime-settings').set('binders', "")
			sublime.load_settings('FileBinder.sublime-settings').set('binders', self.binderList)
			sublime.save_settings('FileBinder.sublime-settings')