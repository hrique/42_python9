#!/usr/bin/env python3

from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime = Field()
    is_operational: bool = Field(default=True)
    notes: str = Field(default=None, max_length=200)


def main() -> None:
    try:
        station = SpaceStation(
                    station_id="ISS001",
                    name="International Space Station",
                    crew_size=6,
                    power_level=85.5,
                    oxygen_level=92.3,
                    is_operational=True,
                    last_maintenance="2026-11-13T08:52:00"
                    )
        print("Space Station Data Validation")
        print("="*40)
        print("Valid station created:")
        print(f"ID: {station.station_id}")
        print(f"Name: {station.name}")
        print(f"Crew: {station.crew_size} people")
        print(f"Power: {station.power_level}%")
        print(f"Oxygen: {station.oxygen_level}%")
        if station.is_operational:
            print("Status: Operational")
        else:
            print("Status: Inoperative")
        print()
        print("="*40)
        SpaceStation(
            station_id="ISS002",
            name="International Space Station",
            crew_size=30,
            power_level=85.5,
            oxygen_level=92.3,
            is_operational=True,
            last_maintenance="2026-11-13T08:52:00"
            )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"])


if __name__ == "__main__":
    main()
