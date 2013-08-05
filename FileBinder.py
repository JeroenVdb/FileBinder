import sublime, sublime_plugin, json

class FileBinderCommand(sublime_plugin.WindowCommand):

	s = None

	def run(self):

		self.choose_binder()

	def choose_binder(self):

		self.s = sublime.load_settings('FileBinder.sublime-settings').get('binders')
		binders = []

		for item in self.s:
			binders.append(item['name'])

		self.window.show_quick_panel(binders, self.callback_choose_binder)

	def callback_choose_binder(self, index):

		if not index == -1:

			for item in self.s[index]['files']:
				self.window.open_file(item)

class AddFileBinderCommand(sublime_plugin.WindowCommand):

	s = None
	binderList = []
	newPathsList = []
	
	def run(self):

		self.window.show_input_panel("Name your binder", "<name>", self.on_done, self.on_change, self.on_cancel)

	def on_done(self, input):

		self.s = sublime.load_settings('FileBinder.sublime-settings')

		binders = self.s.get('binders')

		for item in binders: self.binderList.append(item)

		# Fill binderList with new object
		for view in self.window.views():
			self.newPathsList.append(view.file_name())

		jsonStr = {"name": "" + input + "", "description": "", "files": self.newPathsList}

		self.binderList.append(jsonStr)

		self.s.set('binders', self.binderList)
		sublime.save_settings('FileBinder.sublime-settings')

	def on_change(self, input): print("change")

	def on_cancel(self): print("cancel")