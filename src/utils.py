def parse_response(response: str) -> int:
    raw_response = response.split(":")[-1].strip()

    try:
        return int(raw_response)
    except ValueError:
        raw_response = raw_response.lower()
        map = {
            "disagree": 1,
            "slightly disagree": 2,
            "neutral": 3,
            "slightly agree": 4,
            "agree": 5
        }

        return map[raw_response]
