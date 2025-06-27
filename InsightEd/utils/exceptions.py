# 1
class AuthorizationError(Exception):
    """Raised when there is a problem during login authorization."""

# 2
class JsonFileEmptyError(Exception):
    """Raised when the json file does not contain any data."""

# 3
class UsersFileNotFoundError(Exception):
    """Raised when the users file was not found."""

# 4
class NoGradesToAnalyzeError(Exception):
    """Raised when no grades were found."""

# 5
class AttendanceError(Exception):
    """Raised when the given attendance is wrong."""

# 6
class WrongGradeError(Exception):
    """Raised when a wrong grade is given."""

# 7
class LogoFileNotFoundError(Exception):
    """Raised when the logo file was not found."""

# 8
class NoWarningsFoundException(Exception):
    """Raised when no warnings were found."""

# 9
class UnknownWindowError(Exception):
    """Raised when an unknown window was passed as an argument of the dashboard window."""

# 10
class MyTclError(Exception):
    """Raised when there is an error in tcl execution."""
