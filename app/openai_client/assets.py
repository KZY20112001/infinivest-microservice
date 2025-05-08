from .openai import get_response, format_message


def generate_assets_recommendations(profile: dict) -> list[tuple[str, str]]:
    system_message = """
    You are a helpful financial assistant. Based on the user's given profile, recommend 3 to 5 assets. 
    
    Your response must be a JSON-like dictionary with:
    - "assets": a list of [symbol, name] pairs
    - "reason": a paragraph explaining why these assets make sense

    If no profile is provided, give safe, diversified assets that are performing very well recently 
    suitable for a general investor.
    
    Output format:
    {
      "assets": [["AAPL", "Apple Inc."], ["VTI", "Vanguard Total Stock Market ETF"]],
      "reason": "Because ..."
    }
    """

    has_profile = bool(profile and any(profile.values()))
    if has_profile:
        profile_lines = [f"- {k}: {v}" for k, v in profile.items() if v is not None]
        profile_text = "\n".join(profile_lines)
        user_message = f"""
        Here is my investment profile:
        {profile_text}

        Recommend assets for my manual portfolio.
        """
    else:
        user_message = """
        I have not set up my profile yet. Please recommend assets that are broadly suitable for a typical beginner or average investor.
        """

    messages = [
        format_message("system", system_message.strip()),
        format_message("user", user_message.strip())
    ]

    raw_response = get_response(messages)

    try:
        response_dict = eval(raw_response)
        if (
            isinstance(response_dict, dict)
            and "assets" in response_dict
            and "reason" in response_dict
            and isinstance(response_dict["assets"], list)
            and all(isinstance(x, list) and len(x) == 2 for x in response_dict["assets"])
        ):
            return response_dict
    except Exception:
        pass
    return {
        "assets": [],
        "reason": "We couldn't generate recommendations at this time."
    }