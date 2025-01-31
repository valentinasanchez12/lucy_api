from typing import Dict


def validate_data(data: Dict, required_fields: list) -> Dict:
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {"is_valid": False, "missing": missing_fields}
    return {"is_valid": True}


def convert_line_breaks_to_pipelines(text):
    return text.replace('\n', '||')

def convert_pipelines_to_line_breaks(text):
    return text.replace('||', '\n')
