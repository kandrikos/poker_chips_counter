test_cases = {
    "no_raise": {
        "PRE-FLOP": {
            "Player_3": ["call"],
            "Player_4": ["call"],
            "Player_0": ["call"],
            "Player_1": ["call"],
            "Player_2": ["check"]
        },
        "FLOP": {
            "Player_1": ["check"],
            "Player_2": ["check"],
            "Player_3": ["check"],
            "Player_4": ["check"],
            "Player_0": ["check"]
        },
        "TURN": {
            "Player_1": ["check"],
            "Player_2": ["check"],
            "Player_3": ["check"],
            "Player_4": ["check"],
            "Player_0": ["check"]
        },

        "RIVER": {
            "Player_1": ["check"],
            "Player_2": ["check"],
            "Player_3": ["check"],
            "Player_4": ["check"],
            "Player_0": ["check"]
        },
        "WINNER": "Player_0"
    }
}
