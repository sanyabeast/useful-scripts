#include <iostream>
#include <cstring>
#include <X11/Xlib.h>
#include <X11/Xatom.h>
#include <X11/Xutil.h>

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " \"command\" program_name" << std::endl;
        return 1;
    }

    const char* command = argv[1];
    const char* program_name = argv[2];

    Display* display = XOpenDisplay(nullptr);
    if (!display) {
        std::cerr << "Could not open display" << std::endl;
        return 1;
    }

    // Get the root window
    Window root = XDefaultRootWindow(display);

    // Get the window manager atom
    Atom wm_atom = XInternAtom(display, "_NET_SUPPORTING_WM_CHECK", False);
    Atom wm_check_atom = XInternAtom(display, "_NET_WM_NAME", False);

    // Loop through all windows to find the program's window
    Window window = 0;
    Window root_return = 0;
    Window parent_return = 0;
    Window* children_return = nullptr;
    unsigned int num_children_return = 0;
    for (;;) {
        if (XQueryTree(display, root, &root_return, &parent_return, &children_return, &num_children_return)) {
            for (unsigned int i = 0; i < num_children_return; i++) {
                XTextProperty wm_name_prop;
                if (XGetTextProperty(display, children_return[i], &wm_name_prop, wm_check_atom) == Success) {
                    if (wm_name_prop.value) {
                        printf("Data: %s\n", wm_name_prop.value);
                        char** wm_name_list;
                        int count;
                        if (Xutf8TextPropertyToTextList(display, &wm_name_prop, &wm_name_list, &count) == Success) {
                            for (int j = 0; j < count; j++) {
                                if (strcmp(wm_name_list[j], program_name) == 0) {
                                    window = children_return[i];
                                    break;
                                }
                            }
                            XFreeStringList(wm_name_list);
                        }
                        XFree(wm_name_prop.value);
                    }
                }
                if (window != 0) {
                    break;
                }
            }
            if (children_return != nullptr) {
                XFree(children_return);
            }
            if (window != 0) {
                break;
            }
        }
        if (root == root_return) {
            break;
        }
        root = root_return;
    }

    if (window != 0) {
        // The program is already running, focus its window
        XEvent event;
        memset(&event, 0, sizeof(event));
        event.type = ClientMessage;
        event.xclient.window = window;
        event.xclient.message_type = XInternAtom(display, "_NET_ACTIVE_WINDOW", False);
        event.xclient.format = 32;
        event.xclient.data.l[0] = 2; // Message data: 2 = source indication
        event.xclient.data.l[1] = CurrentTime;
        XSendEvent(display, root, False, SubstructureRedirectMask | SubstructureNotifyMask, &event);
    } else {
        // The program is not running, run the command
        system(command);
    }

    XCloseDisplay(display);

    return 0;
}