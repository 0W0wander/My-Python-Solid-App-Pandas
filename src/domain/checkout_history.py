from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import uuid

@dataclass
class CheckoutHistory:
    book_id: str
    checked_out_time: str
    checked_in_time: Optional[str] = None
    checkout_history_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def check_in(self, check_in_time: Optional[str] = None):
        if self.checked_in_time is not None:
            raise Exception('This checkout has already been checked in.')
        if check_in_time is None:
            check_in_time = datetime.now().isoformat()
        self.checked_in_time = check_in_time

    def is_checked_out(self) -> bool:
        return self.checked_in_time is None

    @classmethod
    def from_dict(cls, data: dict) -> 'CheckoutHistory':
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            "checkout_history_id": self.checkout_history_id,
            "book_id": self.book_id,
            "checked_out_time": self.checked_out_time,
            "checked_in_time": self.checked_in_time,
        }
