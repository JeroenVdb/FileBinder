import sublime, sublime_plugin, json

class FileBinderCommand(sublime_plugin.WindowCommand):

	s = None

	def run(self):

		self.show_binders()

	def show_binders(self):

		self.s = sublime.load_settings('FileBinder.sublime-settings').get('binders')
		binders = []

		for item in self.s:
			binders.append(item['name'])

		self.window.show_quick_panel(binders, self.callback)

	def callback(self, index):
		print('go?')