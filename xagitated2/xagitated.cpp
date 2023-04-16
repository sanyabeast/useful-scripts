#include <iostream>
#include <chrono>
#include <thread>
#include <csignal>
#include <map>

using namespace std;

// Global debug flag
bool debug_mode = false;

bool timer_gate(std::string id, int timeout) {
    static std::map<std::string, std::chrono::steady_clock::time_point> last_called_map;

    auto current_time = std::chrono::steady_clock::now();

    if (last_called_map.find(id) != last_called_map.end()) {
        auto last_called_time = last_called_map[id];
        auto elapsed_time = std::chrono::duration_cast<std::chrono::seconds>(current_time - last_called_time).count();
        if (elapsed_time < timeout) {
            return false;
        }
    }

    last_called_map[id] = current_time;
    return true;
}

std::string run_command(const std::string& command) {
    // Open the command as a subprocess using popen()
    FILE* pipe = popen(command.c_str(), "r");
    if (!pipe) {
        std::cerr << "Failed to open pipe for command: " << command << std::endl;
        return "";
    }

    // Read the output of the command from the pipe
    std::string result = "";
    char buffer[128];
    while (fgets(buffer, sizeof(buffer), pipe)) {
        result += buffer;
    }

    // Close the pipe and return the output
    pclose(pipe);
    return result;
}

// Mockup tick function
void tick()
{
    if (debug_mode)
    {
        cout << "Hello World" << endl;
    }

    if (timer_gate("unique_id1", 3)) {
        std::cout << "This code runs once per 3 seconds" << std::endl;
        std::cout << run_command("xprintidle") << std::endl;
    }

    if (timer_gate("unique_id2", 9)) {
        std::cout << "This code runs once per 9 seconds" << std::endl;
    }
}

// Signal handler for Ctrl+C
void on_finish(int signal)
{
    cout << "Program terminated with signal " << signal << endl;
    exit(0);
}

int main(int argc, char* argv[])
{
    // Register signal handler for Ctrl+C
    signal(SIGINT, on_finish);

    // Parse command-line arguments
    if (argc > 1)
    {
        string arg = argv[1];
        if (arg == "--debug" || arg == "-d")
        {
            debug_mode = true;
            cout << "Debug mode enabled" << endl;
        }
    }

    // Main loop
    while (true)
    {
        tick();
        this_thread::sleep_for(chrono::seconds(1));
    }

    return 0;
}