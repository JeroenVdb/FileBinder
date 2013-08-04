import sublime, sublime_plugin

class FileBinderCommand(sublime_plugin.WindowCommand):

	s = None

	def run(self):

		self.s = sublime.load_settings('FileBinder.sublime-settings')

		options = ['Single file', 'Package file']
        
    	self.window.show_quick_panel(options, self.callback)

	def callback(self, index):

		print("callback")
