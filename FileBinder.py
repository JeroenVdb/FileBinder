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
		for item in self.s[index]['files']:
			print(item)

	def add_binder(self): print('add open files to binder in the settings files + ask for name')

	def remove_binder(self): print('list binder like in choose_binder but other callback (delete)')

	def callback_remove_binder(self): print('remove a binder from the settings file')