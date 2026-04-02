from typing import Union
from src.Common.utils import parse_boolean


class Team:

    def __init__(
        self,
        id: int,
        team_api_id: int | None,
        full_name: str,
        abbreviation: str,
        nickname: str | None,
        city: str | None,
        state: str | None,
        country: str | None,
        region: str | None
    ) -> None:

        self.id = id
        self.team_api_id = team_api_id
        self.full_name = full_name
        self.abbreviation = abbreviation
        self.nickname = nickname
        self.city = city
        self.state = state
        self.country = country
        self.region = region
