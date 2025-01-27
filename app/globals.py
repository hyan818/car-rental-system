from dataclasses import dataclass
from typing import Optional


@dataclass
class CurrentUser:
    user_id: Optional[int]
    username: Optional[str]
    role_name: Optional[str]
