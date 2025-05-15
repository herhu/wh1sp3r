"""
Model router that determines the path to the user's model
"""

import os

def get_user_model_path(user_id: str, model_type: str, language: str = None) -> str:
    if model_type == "private":
        return f"data/users/{user_id}/model"
    elif model_type == "internal":
        if not language:
            raise ValueError("Language is required for internal model")
        return f"data/internal/{language}/model"
    else:
        # Cloud/default
        return "small"
