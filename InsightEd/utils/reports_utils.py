from typing import List, Dict, Union

import pandas as pd

from utils.exceptions import NoGradesToAnalyzeError, AttendanceError


def calculate_average_grades(students: List[Dict]) -> List[Dict[str, Union[str, float]]]:
    result = []

    for student in students:
        grades = [g["value"] for g in student.get("grades", []) if isinstance(g.get("value"), (int, float))]
        if grades:
            avg = round(sum(grades) / len(grades), 2)
            result.append({"Student": f'{student["first_name"]} {student["last_name"]}', "Average Grade": avg})

    if not result:
        raise NoGradesToAnalyzeError

    return result



def gather_all_grades(students: List[Dict]) -> List[Union[int, float]]:
    all_grades = []

    for student in students:
        all_grades.extend([g["value"] for g in student.get("grades", []) if isinstance(g.get("value"), (int, float))])

    return all_grades



def count_attendance_summary(students: List[Dict]) -> Dict[str, int]:
    counts = {"Present": 0, "Absent": 0, "Late": 0, "Excused": 0}
    for student in students:
        for record in student.get("attendance_records", []):

            status = record.get("status")

            if status == "present":
                counts["Present"] += 1

            elif status == "absent":
                counts["Absent"] += 1

            elif status == "late":
                counts["Late"] += 1

            elif status == "excused":
                counts["Excused"] += 1

            else:
                raise AttendanceError

    return counts



def attendance_per_student(students: List[Dict]) -> List[Dict[str, Union[str, int]]]:
    data = []
    for student in students:

        records = student.get("attendance_records", [])

        data.append({
            "Student": f'{student["first_name"]} {student["last_name"]}',
            "Present": sum(1 for r in records if r.get("status") == "present"),
            "Absent": sum(1 for r in records if r.get("status") == "absent"),
            "Late": sum(1 for r in records if r.get("status") == "late"),
            "Excused": sum(1 for r in records if r.get("status") == "excused"),
        })

    return data



def grades_per_student(students: List[Dict]) -> List[Dict[str, Union[str, int]]]:
    all_possible_grades = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    data = []

    for student in students:
        name = f'{student["first_name"]} {student["last_name"]}'
        grade_counts = {str(g): 0 for g in all_possible_grades}

        for grade_entry in student.get("grades", []):
            val = grade_entry.get("value")
            if isinstance(val, (int, float)):
                val_str = str(float(val))
                if val_str in grade_counts:
                    grade_counts[val_str] += 1

        entry = {"Student": name}
        entry.update(grade_counts)
        data.append(entry)

    return data



def export_data_to_excel(data: List[Dict], filename: str) -> None:
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
