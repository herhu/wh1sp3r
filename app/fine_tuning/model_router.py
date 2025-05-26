import os

def get_user_model_path(user_id: str, model_type: str, language: str = None) -> str:
    if model_type == "private":
        path = f"data/users/{user_id}/model"
        return path if os.path.exists(path) else "small"
    
    elif model_type == "internal":
        if not language:
            raise ValueError("Language is required for internal model")
        path = f"data/internal/{language}/model"
        return path if os.path.exists(path) else "small"

    return "small"
