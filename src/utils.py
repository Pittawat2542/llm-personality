def parse_response(response: str) -> int:
    raw_response = response.split(":")[-1].strip()

    try:
        return int(raw_response)
    except ValueError:
        raw_response = raw_response.lower()
        score_map = {
            "very inaccurate": 1,
            "moderately inaccurate": 2,
            "neither accurate nor inaccurate": 3,
            "moderately accurate": 4,
            "very accurate": 5
        }

        return score_map[raw_response]
