# Compiling Instructions
ok, so i guess you are here for compiling instructions, well here we GOOO
the compiling instructions are pretty simple, you only need these prerequisites 
- Python
- pyinstaller (can be installed by pip install pyinstaller)
- nothing more!
ok so lets start, first make a folder because you dont want the Downloads folder to get messy with the build files
move the latest version's (or the version you desire) py file to that folder.
open up a terminal windows in that folder, and use this command:pyinstaller db-assistant-X.X.X (replace the Xs with the version number, for example db-assistant-1.0.0 or db-assistant-0.0.5) and you also need to use the proper arguments for the build. these are the arguments you can use: "--onefile" quite obvious what it means, it will bundle everything into one .exe file, this option should the on the command unless you have specific desires for some reason (example of the argument on the command: pyinstaller db-assistant.X.X.X.py --onefile) and you also have "--noconsole" it is even more obvious, a terminal doesnt show up when you execute it.
Well, id say this tutorial is done!
