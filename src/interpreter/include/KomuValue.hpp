#include <stdexcept>
#include <string>
#include <variant>

/**
 * @brief A struct that can hold any value in the Komu language.
 *
 * It uses std::variant to safely store one of the possible types.
 */
struct KomuValue
{
    // Komu value can be one of these types
    std::variant<std::monostate, double, bool, std::string> value;

    KomuValue() : value(std::monostate{}) {}
    KomuValue(double d) : value(d) {}
    KomuValue(bool b) : value(b) {}
    KomuValue(const std::string& s) : value(s) {}
    KomuValue(const char* s) : value(std::string(s)) {}
};