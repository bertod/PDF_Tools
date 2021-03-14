# PDF_Handler

Python package (with GUI) for implementing operation on PDF files. 

Main Features implemented:
- Page extractor -> create a new PDF containing only the specified pages (or ranges of pages)
- PDF Merger -> merge in a new PDF all the selected PDF files


Modularity:
Anyone could develop new features (or modify user interface) by writing a custom GuiHandler and eventually new Plugins.
There is a custom Gui handler of example in 'GuiHandler' directory. The same custom gui handler uses also a custom created Plugins for extending
the user interface with a new section.
To run the new GuiHandler, you need just to change the 'run.py' file to call you handler.


There is also the possibility of extending the 'PDFHandler' (in dir 'Helpers') but I did not try it yet. You could also do it with a custom helper 
which inherits the original PDFHandler and then you should overwrite the helper object in your custom GuiHandler:
self.helper_pdf = PDFHandler() -> self.helper_pdf = PDFHandlerCustom()



# Windows .exe
In PDF/PDF_Handler_Win32 there is the runable file for Windows generated with pyinstaller.
The .exe has been tested under windows 10 only.

