import sublime, sublime_plugin

# Open binder
class FileBinderCommand(sublime_plugin.WindowCommand):

	binders = None

	def run(self):

		self.choose_binder()

	def choose_binder(self):

		# Gather all binder names
		self.binders = sublime.load_settings('FileBinder.sublime-settings').get('binders')
		binderNameList = []
		for item in self.binders:
			binderNameList.append(item['name'])

		# Choose your binder
		if len(binderNameList) > 0:
			self.window.show_quick_panel(binderNameList, self.callback_choose_binder)
		else:
			self.window.show_quick_panel(["You dont have any binders yet"], None)

	def callback_choose_binder(self, index):

		if not index == -1:

			for item in self.binders[index]['files']:
				self.window.open_file(item)

# Add binder
class AddFileBinderCommand(sublime_plugin.WindowCommand):

	binders = None
	newBinderList = []
	newPathsList = []
	
	def run(self):

		# reset
		self.newBinderList = []

		self.window.show_input_panel("Name your binder", "", self.on_done, None, None)

	def on_done(self, input):

		# Gather existing binders in newBinderList
		self.binders = sublime.load_settings('FileBinder.sublime-settings').get('binders')
		for item in self.binders:
			self.newBinderList.append(item)

		# Extend newBinderList with new binder
		for view in self.window.views():
			self.newPathsList.append(view.file_name())
		jsonStr = {"name": "" + input + "", "description": "", "files": self.newPathsList}
		self.newBinderList.append(jsonStr)

		# Save them all
		sublime.load_settings('FileBinder.sublime-settings').set('binders', self.newBinderList)
		sublime.save_settings('FileBinder.sublime-settings')

# Remove binder
class RemoveFileBinderCommand(sublime_plugin.WindowCommand): 

	binders = None
	newBinderList = []

	def run(self):

		# reset
		self.newBinderList = []

		self.choose_binder()

	def choose_binder(self):

		# Gather all binder names
		self.binders = sublime.load_settings('FileBinder.sublime-settings').get('binders')
		binderNameList = []
		for item in self.binders: binderNameList.append(item['name'])

		# Choose your binder
		if len(binderNameList) > 0:
			self.window.show_quick_panel(binderNameList, self.callback_choose_binder)
		else:
			self.window.show_quick_panel(["You dont have any binders yet"], None)

	def callback_choose_binder(self, index):

		if not index == -1:

			# Gather all binder but the one to remove
			self.binders = sublime.load_settings('FileBinder.sublime-settings').get('binders')
			for i, item in enumerate(self.binders):
				if i != index:
					self.newBinderList.append(item)

			# Save them all
			sublime.load_settings('FileBinder.sublime-settings').set('binders', self.newBinderList)
			sublime.save_settings('FileBinder.sublime-settings')