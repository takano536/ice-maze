CXX = g++
CXXFLAGS = -std=gnu++17 -Wall -Wextra -O2
SRCS = $(shell find * -name "*.cpp")
OBJS := $(SRCS:.cpp=.o)
TARGET = main.out

$(TARGET): $(OBJS)
	$(CXX) -o $@ $(OBJS)

clean:
	rm -f $(TARGET) $(OBJS)