#!/usr/bin/env python3
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Field()
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def check_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if (self.contact_type == ContactType.PHYSICAL
                and not self.is_verified):
            raise ValueError("Physical contact must be verified")
        if (self.contact_type == ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")
        if (self.signal_strength > 7.0 and not self.message_received):
            raise ValueError("Signal higher than 7.0 needs a message")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)
    try:
        contact1 = AlienContact(
            contact_id="AC_2024_001",
            contact_type=ContactType.RADIO,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            timestamp=datetime(2024, 2, 13, 10, 59),
            is_verified=True
        )
        print("Valid contact report:")
        print(f"ID: {contact1.contact_id}")
        print(f"Type: {contact1.contact_type.value}")
        print(f"Location: {contact1.location}")
        print(f"Signal: {contact1.signal_strength}/10")
        print(f"Duration: {contact1.duration_minutes} minutes")
        print(f"Witnesses: {contact1.witness_count}")
        print(f"Message: '{contact1.message_received}'")
    except ValidationError as e:
        print("Validation error:")
        for error in e.errors():
            print(error["msg"].removeprefix("Value error, "))
    print()
    print("=" * 40)
    try:
        AlienContact(
            contact_id="AC_2024_002",
            contact_type=ContactType.TELEPATHIC,
            location="Area 51, Nevada",
            signal_strength=6.9,
            duration_minutes=42,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli",
            timestamp=datetime(2026, 2, 13, 10, 59),
            is_verified=True
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"].removeprefix("Value error, "))


if __name__ == "__main__":
    main()
