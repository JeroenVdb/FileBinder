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
				self.window.open_file(item['path'])

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

		print(self.window.views())

		# Extend newBinderList with new binder
		for view in self.window.views():
			self.newPathsList.append({"path": view.file_name() , "pane": "5"})

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