import tkinter as tk
from tkinter import ttk

class eg_class(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.wm_title("Test application")

		container = tk.Frame(self, height = 400, width = 600)
		container.pack(side = "top", fill ="both", expand = True)

		container.grid_rowconfigure(0, weight=1)

		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (pagina1, pagina2, pagina3):
			#calll the page with the frame as argument
			frame = F(container, self)#here the classes are instantiated. (only once in the constructor)
			
			self.frames[F] = frame#	frames{pagina1: pagina1, pagina2: pagina2, pagina3: pagina3}
			frame.grid(row = 0 ,column = 0, sticky = "nsew")
		self.show_frame(pagina1)

	def show_frame(self,cont):
		frame = self.frames[cont]
		frame.tkraise()
		# cont.tkraise()

#Main page: pagina1

class pagina1(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self, text = "Main Page")
		label.pack(padx = 10, pady = 10)

		switch_window_button = tk.Button(
			self,
			text = "Change Page",
			command=lambda: controller.show_frame(pagina2),
			)
		switch_window_button.pack(side = "bottom", fill =tk.X)

#Side page: pagina 2

class pagina2(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text = "This is the Side Page")
		label.pack(padx = 10, pady = 10)

		switch_window_button = tk.Button(
			self,
			text  ="Go to the Final Page",
			command = lambda: controller.show_frame(pagina3),
			)
		switch_window_button.pack(side = "bottom", fill = tk.X)


#Completion Screen ( pagina 3)

class pagina3(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text = "Completion Screen")
		label.pack(padx = 10, pady = 10)
		switch_window_button =ttk.Button(
			self, text = "Return Home", command = lambda: controller.show_frame(pagina1)
		)
		switch_window_button.pack(side = "bottom", fill = tk.X)



if __name__ == "__main__":
	Obj = eg_class()
	Obj.mainloop()#this method exist because of inheritance

