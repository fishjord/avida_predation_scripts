alignment.so: alignment.cpp
	g++ -fPIC -Wall -shared -I/usr/include/python2.7/ -lpython2.7 -o alignment.so alignment.cpp