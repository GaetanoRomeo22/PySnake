#include <cstdlib>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
  fs::current_path(fs::current_path() / "Snake");

  const char* commands[] = {
    "pip install -r requirements.txt",
    "python main.py"
  };

  for (const auto* command : commands) {
    std::system(command);
  }
  return 0;
}
