import re
from typing import TypedDict


class StudyUriUuids(TypedDict):
    project_id: str
    patient_id: str
    study_id: str


def extract_uuids(uri: str) -> list[str]:
    # Regular expression to match UUIDs
    uuid_pattern = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
    # Find all matches in the URI
    return uuid_pattern.findall(uri)


def extract_uuids_from_study_uri(study_uri: str) -> StudyUriUuids:
    uuids = extract_uuids(study_uri)
    if len(uuids) != 3:
        raise Exception("invalid study_uri")

    return {"project_id": uuids[0], "patient_id": uuids[1], "study_id": uuids[2]}
