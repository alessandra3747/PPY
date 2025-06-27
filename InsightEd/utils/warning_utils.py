from typing import Dict, Any, List

from utils.exceptions import NoWarningsFoundException


def is_student_at_risk(student: Dict[str, Any]) -> bool:
    grades = student.get("grades", [])
    attendance = student.get("attendance_records", [])

    numeric_grades = [g["value"] for g in grades if isinstance(g["value"], (int, float))]
    avg = sum(numeric_grades) / len(numeric_grades) if numeric_grades else None

    absences = sum(1 for a in attendance if a.get("status") == "absent")
    lates = sum(1 for a in attendance if a.get("status") == "late")
    total_misses = absences + lates

    is_low_avg = avg is not None and avg < 3.0
    is_too_many_absences = total_misses > 2

    return is_low_avg or is_too_many_absences



def generate_warnings(students: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    warnings = []

    for student in students:
        if is_student_at_risk(student):
            name = f"{student.get('first_name', '')} {student.get('last_name', '')}"
            index = student.get("pesel", "")
            grades = student.get("grades", [])
            attendance = student.get("attendance_records", [])

            numeric_grades = [g["value"] for g in grades if isinstance(g["value"], (int, float))]
            avg = sum(numeric_grades) / len(numeric_grades) if numeric_grades else None

            absences = sum(1 for a in attendance if a.get("status") == "absent")
            lates = sum(1 for a in attendance if a.get("status") == "late")
            total_misses = absences + lates

            reason_parts = []
            if avg is not None and avg < 3.0:
                reason_parts.append(f"Low average: ({avg:.2f})")
            if total_misses > 2:
                reason_parts.append(f"Total of {total_misses} absences / late arrivals")

            warnings.append({"name": name, "index": index, "reason": ", ".join(reason_parts)})

    if not warnings:
        raise NoWarningsFoundException

    return warnings
