CC=g++
CFLAGS=-c -Wall
LDFLAGS=
SOURCES=xagitated.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=xagitated

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf $(OBJECTS) $(EXECUTABLE)