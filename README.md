# multipaste

Information:
===

**Windows only**, uses pywin32 for clipboard since copying multiple files in
explorer uses a different format for the data (a list of files) other
than plain text.


It is for pasting multiple files from explorer. It uses the extension to
determine which import operator to use on each file.  Currently
supported formats are SVG, OBJ, DAE, PLY, and STL.  It is fairly easy to add more elif statements to handle other types, as long as there exists an operator to import said format.


Initially, Pywin32 must be installed via pip so that blender can use win32clipboard. The addon preferences has an operator which will attempt to do this. YMMV

If I can get access to a Mac I will add support for that platform. Linux, I just haven't gotten around to installing one lately but it's definitely on the agenda.



