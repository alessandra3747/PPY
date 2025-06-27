import time

from functools import wraps
from typing import Callable, Optional, Dict

from utils.exceptions import AuthorizationError, UsersFileNotFoundError
from utils.file_utils import load_users



def limit_login_attempts(max_attempts: int = 3, block_seconds: int = 30) -> Callable:
    attempts = {}

    def decorator(func):
        @wraps(func)
        def wrapper(self, username, password):
            now = time.time()
            user_data = attempts.get(username, {"count": 0, "first_attempt_time": now})

            if user_data["count"] > max_attempts:
                elapsed = now - user_data["first_attempt_time"]
                if elapsed < block_seconds:
                    return ["blocked", int(block_seconds - elapsed)]
                else:
                    user_data = {"count": 0, "first_attempt_time": now}

            elif now - user_data["first_attempt_time"] > block_seconds:
                user_data = {"count": 0, "first_attempt_time": now}

            result = func(self, username, password)

            if result:
                user_data = {"count": 0, "first_attempt_time": now}
                attempts[username] = user_data
                return ["success",0]
            else:
                user_data["count"] += 1
                if user_data["count"] == 1:
                    user_data["first_attempt_time"] = now
                attempts[username] = user_data
                if user_data["count"] > max_attempts:
                    return ["blocked", int(block_seconds)]
                raise AuthorizationError("Incorrect login or password.")

        return wrapper
    return decorator



class AuthService:

    def __init__(self) -> None:
        try:
            self.users = load_users()
        except UsersFileNotFoundError:
            self.users = None


    @limit_login_attempts(max_attempts=3, block_seconds=30)
    def authenticate(self, username: str, password: str) -> bool:
        if self.users is None:
            return False
        user = self.users.get(username)
        if user is None:
            return False
        return user.get("password") == password



    def get_user_data(self, username: str) -> Optional[Dict[str, str]]:
        return self.users.get(username)
