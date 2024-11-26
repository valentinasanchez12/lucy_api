from typing import Dict


def validate_data(data: Dict, required_fields: list) -> Dict:
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {"is_valid": False, "missing": missing_fields}
    return {"is_valid": True}