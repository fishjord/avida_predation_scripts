PYTHON_VERSION = $(shell python -c 'import sys; print "python%s.%s" % (sys.version_info[0], sys.version_info[1])')
PYTHON_INC = $(shell python -c 'import sys; print "%s/include/python%s.%s" % (sys.prefix, sys.version_info[0], sys.version_info[1])')

alignment.so: alignment.cpp
	g++ -fPIC -Wall -shared -I${PYTHON_INC} -l${PYTHON_VERSION} -o alignment.so alignment.cpp