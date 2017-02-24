import sublime, sublime_plugin, json, string

# Open binder
class FileBinderCommand(sublime_plugin.WindowCommand):

	binder = []
	binders = None
	settings = None

	def run(self):

		self.choose_binder()

	def choose_binder(self):

		# Settings
		self.settings = sublime.load_settings('FileBinder.sublime-settings').get('settings')

		# Gather all binder information
		self.binders = sublime.load_settings('FileBinder.sublime-settings').get('binders')
		binderNameList = []
		for item in self.binders:

			# Reset binder
			self.binder = []

			# Name
			self.binder.append(item['name'])

			# Show number of files
			if (self.settings.get("show_number_of_files", False)):
				numberOfFiles = len(item['files'])
				self.binder.append(str(numberOfFiles) + " files")

			# Show file path teaser
			if (self.settings.get("show_path_teaser", False)):
				numberOfFiles = len(item['files'])
				maxRange = 3 if numberOfFiles >= 3 else numberOfFiles

				for i in range(0, maxRange):
					self.binder.append(item['files'][i]['path'])

				if (numberOfFiles > 3):
					self.binder.append("...")

			binderNameList.append(self.binder)

		# Choose your binder
		if len(binderNameList) > 0:
			self.window.show_quick_panel(binderNameList, self.callback_choose_binder)
		else:
			self.window.show_quick_panel(["You dont have any binders yet"], None)

	def callback_choose_binder(self, index):

		if not index == -1:

			if (self.settings.get('remember_groups')):
				self.window.set_layout(self.binders[index]['layout'])

			if (self.settings.get('close_other_files')):
				for view in self.window.views():
					view.close()

			for item in self.binders[index]['files']:
				if 'path' in item:
					if (self.settings.get('remember_groups')):
						self.window.focus_group(item['group'])
					self.window.open_file(item['path'])
				else:
					self.window.open_file(item) # deprecated


# Add binder
class AddFileBinderCommand(sublime_plugin.WindowCommand):

	binders = None
	newBinderList = []
	newPathsList = []

	def run(self):

		# reset
		self.newBinderList = []
		self.newPathsList = []

		self.window.show_input_panel("Name your binder", "", self.on_done, None, None)

	def on_done(self, input):

		# Gather existing binders in newBinderList
		self.binders = sublime.load_settings('FileBinder.sublime-settings').get('binders')
		for item in self.binders:
			self.newBinderList.append(item)

		# Extend newBinderList with new binder
		for view in self.window.views():
			if (view.file_name() is not None):
				(group, index) = self.window.get_view_index(view)
				self.newPathsList.append({"path": view.file_name() , "group": group})

		jsonStr = {"name": "" + input + "", "description": "", "files": self.newPathsList, "layout": self.window.get_layout()}
		self.newBinderList.append(jsonStr)

		# Save them all
		sublime.load_settings('FileBinder.sublime-settings').set('binders', self.newBinderList)
		sublime.save_settings('FileBinder.sublime-settings')

# Update binder
class UpdateFileBinderCommand(sublime_plugin.WindowCommand):

	binders = None
	# newBinderList = []
	newPathsList = []

	def run(self):

		# reset
		self.newPathsList = []

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

			# Get the new files
			for view in self.window.views():
				(group, group_index) = self.window.get_view_index(view)
				self.newPathsList.append({"path": view.file_name() , "group": group})

			# Gather all binders
			self.binders = sublime.load_settings('FileBinder.sublime-settings').get('binders')

			# Update the files
			self.binders[index]['files'][:] = []
			self.binders[index]['files'].append(self.newPathsList)

			# Save them all
			sublime.load_settings('FileBinder.sublime-settings').set('binders', self.binders)
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

def changeLayout():

        layout = sublime.active_window().get_layout()
        rows = len(layout['rows']) - 1
        cols = len(layout['cols']) - 1

        active = sublime.active_window().get_view_index(sublime.active_window().active_view())[0]

        if active == 0:
                sublime.active_window().set_layout(createLayout(rows, 2))
                newGroup = 1
        else:
                newGroup = 0

        return newGroup

def createLayout(rows, cols):

    numCells = rows * cols
    rowIncrement = 1.0 / rows
    colIncrement = 1.0 / cols

    # Add initial layout arrays
    layoutRows = [0]
    layoutCols = [0]
    layoutCells = [[0] * 4] * numCells

    # Create rows array
    if rows > 1:
        for x in range(1, rows):
            increment = rowIncrement * x
            layoutRows.append(increment)

    layoutRows.append(1.0)

    # Create columns arraydown
    if cols > 1:
        for y in range(1, cols):
            increment = colIncrement * y
            layoutCols.append(increment)

    layoutCols.append(1.0)

    # Create cell definitions (a,b)
    counter = 0
    for a in range(rows):
        for b in range(cols):
            layoutCells[counter] = [b, a, b + 1, a + 1]
            counter += 1

    return {'cells': layoutCells, 'rows': layoutRows, 'cols': layoutCols}
