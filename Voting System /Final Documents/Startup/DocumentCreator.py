import names
from random_username.generate import generate_username
import random

usernames = list(set(generate_username(280)))
used_names = []
pointer = 0

candidate_file_info = []
student_file_info = []


def add_candidates() -> None:
    """Creates the full version of the GSU Candidates file"""
    faculties = ["Computer Science", "Performing Arts", "Engineering", "Economics"]
    for faculty in faculties:
        create_candidate(faculty, "President")
        for _ in range(3):
            create_candidate(faculty, "GSU Officer")
        for _ in range(16):
            create_candidate(faculty, "Faculty Officer")


def get_name() -> str:
    """Used to generate a full name that has not been previously used"""
    global used_names
    name = names.get_full_name()
    while name in used_names:
        name = names.get_full_name()
    used_names.append(name)
    return name


def create_candidate(faculty: str, position: str) -> None:
    """Generic template used to create candidates"""
    global usernames, pointer, candidate_file_info
    name = get_name()
    username = usernames[pointer]
    password = username[:6][::-1]
    candidate_file_info.append([name, position, username, password, faculty])
    pointer += 1


def create_student(faculty: str) -> None:
    """Generic template used to create students"""
    global usernames, pointer, student_file_info
    username = usernames[pointer]
    password = username[:6][::-1]
    student_file_info.append([username, password, faculty])
    pointer += 1


def add_students() -> None:
    """Used to create all the student accounts"""
    faculties = ["Computer Science", "Performing Arts", "Engineering", "Economics"]
    for faculty in faculties:
        for _ in range(50):
            create_student(faculty)


if __name__ == "__main__":
    if len(usernames) == 280:
        add_candidates()
        random.shuffle(candidate_file_info)
        with open("GSUCandidates.txt", "w") as gsu_candidates_file:
            for candidate in candidate_file_info:
                data = ', '.join(candidate)
                gsu_candidates_file.write(data + "\n")
        add_students()
        random.shuffle(student_file_info)
        with open("StudentVoters.txt", "w") as student_voters_file:
            for student in student_file_info:
                data = ', '.join(student)
                student_voters_file.write(data + "\n")
        print("Done")
    else:
        print("Only ", len(usernames), " where provided")

