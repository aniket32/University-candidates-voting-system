# Created by Adnan Turan and Arbaaz Sheikh

import os

import json
import hashlib
from datetime import datetime


class VotingSystemDatabase:
    def __init__(self):
        self._formatted_information = []
        self._LOCAL_SETUP_PATH = os.path.dirname(__file__) + "/Startup/"
        self.RESULTS_DATE = datetime(2020, 1, 27, 0, 0)  # TODO change to date after election, YYYY-MM-DD
        self.CURRENT_DATE = datetime.now()
        if os.path.exists(self._LOCAL_SETUP_PATH + "FormattedInformation.txt"):
            self._set_formatted_information_from_formatted_file()
        elif os.path.exists(self._LOCAL_SETUP_PATH + "GSUCandidates.txt") and \
                os.path.exists(self._LOCAL_SETUP_PATH + "StudentVoters.txt"):
            self._set_formatted_information_from_files()
        else:
            print("Startup files not found")

    def _set_formatted_information_from_formatted_file(self) -> None:
        """Decodes the contents stored in FormattedInformation.txt as JSON to an array and stores the
        contents in the array formatted_information"""
        with open(self._LOCAL_SETUP_PATH + "FormattedInformation.txt", "r") as formatted_file:
            self._formatted_information = json.loads(formatted_file.read())

    def _set_formatted_information_from_files(self) -> None:
        """Used for initial setup, sets the formatted_information variable to the contents of the GSUCandidates.txt
        and StudentVoters.txt after it has been formatted. The files are then deleted and the formatted contents
        are saved in the FormattedInformation.txt file"""
        self._add_candidates_from_file()
        self._add_student_voters_from_file()
        self._formatted_information = self._remove_duplicate_entries_for_in_of("username", self._formatted_information)
        self._remove_initial_files()
        self._upload_formatted_information_as_json()

    def _add_candidates_from_file(self) -> None:
        """Retrieves the candidates information from GSUCandidates.txt and formats it into a dictionary
        which is stored in the variable formatted_information"""
        candidates = []
        with open(self._LOCAL_SETUP_PATH + "GSUCandidates.txt", "r") as candidate_file:
            for line in candidate_file:
                candidate_data = line.split(", ")
                hashed_password = self._get_hashed_password(candidate_data[3])
                temp_dict = {
                    "user_type": "candidate",
                    "candidate_name": candidate_data[0],
                    "candidate_position": candidate_data[1],
                    "username": candidate_data[2],
                    "student_faculty": candidate_data[4].replace("\n", "").replace("\r", ""),
                    "password": hashed_password,
                    "has_voted": False,
                    "number_of_votes_1st": 0,
                    "number_of_votes_2nd": 0,
                    "number_of_votes_3rd": 0,
                    "number_of_votes_4th": 0,
                }
                candidates.append(temp_dict)
        candidates = self._remove_duplicate_entries_for_in_of("candidate_name", candidates, "candidate")
        self._formatted_information.extend(candidates[:80])

    @staticmethod
    def _remove_duplicate_entries_for_in_of(key: str, arr: list, user_type="student voter") -> list:
        """removes any duplicates entries for a specific key in formatted_information. If the user_type is set to
        candidate, it will only check the candidate records"""
        entries = {}
        for student in arr:
            if student["user_type"] == user_type or user_type == "student voter":
                if student[key] in entries.keys():
                    entries[student[key]].append(student)
                else:
                    entries[student[key]] = [student]
        for entry in entries:
            if len(entries[entry]) > 1:
                print("Duplicate Found: ", entries[entry])
                for student in entries[entry]:
                    # TODO Ask if they want both entries to be removed or just the duplicate
                    arr.remove(student)
        return arr

    @staticmethod
    def _get_hashed_password(password_arg: str) -> str:
        """Returns the hashed form of the password"""
        hash_object = hashlib.sha512()
        hash_object.update(password_arg.encode("utf-8"))
        return hash_object.hexdigest()

    def _add_student_voters_from_file(self) -> None:
        """Retrieves the student voters information from StudentVoters.txt and formats it into a dictionary
        which is stored in a variable called formatted_information"""
        with open(self._LOCAL_SETUP_PATH + "StudentVoters.txt", "r") as student_voters_file:
            for line in student_voters_file:
                student_voters_file = line.split(", ")
                hashed_password = self._get_hashed_password(student_voters_file[1])
                temp_dict = {
                    "user_type": "student voter",
                    "username": student_voters_file[0],
                    "password": hashed_password,
                    "student_faculty": student_voters_file[2].replace("\n", "").replace("\r", ""),
                    "has_voted": False
                }
                self._formatted_information.append(temp_dict)

    def _remove_initial_files(self) -> None:
        """Removes files needed for the initial setup"""
        os.remove(self._LOCAL_SETUP_PATH + "GSUCandidates.txt")
        os.remove(self._LOCAL_SETUP_PATH + "StudentVoters.txt")

    def _upload_formatted_information_as_json(self) -> None:
        """Encodes the variable formatted_information as JSON and saves it in the text file FormattedInformation.txt"""
        with open(self._LOCAL_SETUP_PATH + "FormattedInformation.txt", "w") as formatted_file:
            formatted_file.write(json.dumps(self._formatted_information))

    # PUBLIC
    def get_index_of_username(self, username_arg: str) -> int:
        """Gets the index position where the username is located in the formatted_information array and returns -1 if
        not found"""
        index_position = -1
        for index in range(len(self._formatted_information)):
            temp_username = self._formatted_information[index]["username"]
            if temp_username == username_arg:
                index_position = index
        return index_position

    # PUBLIC
    def get_index_of_candidate_name(self, name: str) -> int:
        """Returns the index position of the candidate name that is located in the formatted_information array
         and returns -1 if not found"""
        index_position = -1
        for index in range(len(self._formatted_information)):
            student = self._formatted_information[index]
            if student["user_type"] == "candidate":
                if student["candidate_name"] == name:
                    index_position = index
        return index_position

    #  PUBLIC
    def get_login_details_valid(self, username_arg: str, password_arg: str) -> bool:
        """Returns True if the password provided matches the password for the associated username"""
        username_index = self.get_index_of_username(username_arg)
        account_hashed_password = self._formatted_information[username_index]["password"]
        hashed_provided_password = self._get_hashed_password(password_arg)
        return account_hashed_password == hashed_provided_password

    # PUBLIC
    def apply_student_votes(self, position_1: list, position_2: list, position_3: list, position_4: list) -> None:
        """Applies the student's votes to the the specified candidates"""
        position_1 = list(set(position_1))
        position_2 = list(set(position_2))
        position_3 = list(set(position_3))
        position_4 = list(set(position_4))
        for candidate_index in position_1:
            self._formatted_information[candidate_index]["number_of_votes_1st"] += 1
        for candidate_index in position_2:
            self._formatted_information[candidate_index]["number_of_votes_2nd"] += 1
        for candidate_index in position_3:
            self._formatted_information[candidate_index]["number_of_votes_3rd"] += 1
        for candidate_index in position_4:
            self._formatted_information[candidate_index]["number_of_votes_4th"] += 1
        self._upload_formatted_information_as_json()
        self.create_votes_file()

    # PUBLIC
    def get_student_information(self, username_index: int) -> dict:
        """Returns all the information for a specific user, using the index of the user"""
        return self._formatted_information[username_index]

    # PUBLIC
    def set_student_as_voted(self, username_index: int):
        """Sets the has_voted attribute of the student as True in the FormattedInformation.txt file"""
        self._formatted_information[username_index]["has_voted"] = True
        self._upload_formatted_information_as_json()

    # PUBLIC
    def get_top_four_candidates(self, running_position: str, faculty="any") -> list:
        """Returns the top 4 candidates running for a specific position in a specific faculty"""
        candidates = self.get_candidates(running_position, faculty)
        candidates_1st_position = sorted(candidates, key=lambda x: x["number_of_votes_1st"], reverse=True)
        top_4_candidates = candidates_1st_position
        vote_positions = ["number_of_votes_1st", "number_of_votes_2nd", "number_of_votes_3rd", "number_of_votes_4th"]
        loop_count, changes_made = 0, True
        while loop_count < len(top_4_candidates) and changes_made:
            changes_made = False
            for index in range(len(top_4_candidates) - 1):
                score1, score2 = 0, 0
                position = -1
                temp_candidate_1 = top_4_candidates[index]
                temp_candidate_2 = top_4_candidates[index + 1]
                while position < 3 and score1 == score2:
                    position += 1
                    score1 = temp_candidate_1[vote_positions[position]]
                    score2 = temp_candidate_2[vote_positions[position]]
                if score2 > score1:
                    top_4_candidates[index] = temp_candidate_2
                    top_4_candidates[index + 1] = temp_candidate_1
                    changes_made = True
            loop_count += 1
        return top_4_candidates[:4]

    # PUBLIC
    def get_candidates(self, running_position: str, faculty="any") -> list:
        """Gets all the candidates that are running for a specific position or are in a specific faculty.
        Returns a list of dictionaries"""
        selected_candidates = []
        for student in self._formatted_information:
            if student["user_type"] == "candidate":
                if student["candidate_position"] == running_position and \
                        (faculty == "any" or student["student_faculty"] == faculty):
                    selected_candidates.append(student)
        return selected_candidates

    # PUBLIC
    def create_votes_file(self) -> None:
        """Creates the file Voters.txt"""
        president_candidates = self.get_candidates("President")
        gsu_candidates = self.get_candidates("GSU Officer")
        faculty_candidates = self.get_candidates("Faculty Officer")
        with open("Votes.txt", "w") as file:
            for candidate in president_candidates:
                sentence = candidate["candidate_name"] + " " + str(candidate["number_of_votes_1st"]) + " " + \
                           str(candidate["number_of_votes_2nd"]) + " " + str(candidate["number_of_votes_3rd"]) + " " + \
                           str(candidate["number_of_votes_4th"])
                file.write(sentence + "\n")
            for candidate in gsu_candidates:
                sentence = candidate["candidate_name"] + " " + str(candidate["number_of_votes_1st"]) + " " + \
                           str(candidate["number_of_votes_2nd"]) + " " + str(candidate["number_of_votes_3rd"]) + " " + \
                           str(candidate["number_of_votes_4th"])
                file.write(sentence + "\n")
            for candidate in faculty_candidates:
                sentence = candidate["candidate_name"] + " " + str(candidate["number_of_votes_1st"]) + " " + \
                           str(candidate["number_of_votes_2nd"]) + " " + str(candidate["number_of_votes_3rd"]) + " " + \
                           str(candidate["number_of_votes_4th"])
                file.write(sentence + "\n")

    # PUBLIC
    def create_summary_file(self) -> None:
        """Create a summary file"""
        president_name = self.get_top_four_candidates("President")[0]["candidate_name"]
        gsu_officers = self.get_top_four_candidates("GSU Officer")
        faculty_officers_cs = self.get_top_four_candidates("Faculty Officer", "Computer Science")
        faculty_officers_pa = self.get_top_four_candidates("Faculty Officer", "Performing Arts")
        faculty_officers_eng = self.get_top_four_candidates("Faculty Officer", "Engineering")
        faculty_officers_eco = self.get_top_four_candidates("Faculty Officer", "Economics")
        with open("Summary.txt", "w") as file:
            file.write("President Name: " + president_name + "\n")
            file.write("\n")
            for candidate in gsu_officers:
                file.write("GSU Officer: " + candidate["candidate_name"] + "\n")
            file.write("\n")
            for candidate in faculty_officers_cs:
                file.write("Computer Science: " + candidate["candidate_name"] + "\n")
            file.write("\n")
            for candidate in faculty_officers_pa:
                file.write("Performing Arts: " + candidate["candidate_name"] + "\n")
            file.write("\n")
            for candidate in faculty_officers_eng:
                file.write("Engineering: " + candidate["candidate_name"] + "\n")
            file.write("\n")
            for candidate in faculty_officers_eco:
                file.write("Economics: " + candidate["candidate_name"] + "\n")

    # PUBLIC
    def create_bottom_3_gsu_file(self) -> None:
        """Gets the alst 3 candidates with the lowest frist position scores"""
        candidates = self.get_candidates("GSU Officer")
        candidates_orderd = sorted(candidates, key=lambda x: x["number_of_votes_1st"])[:3]
        for candidate in candidates_orderd:
            print(candidate["candidate_name"])

    # PUBLIC
    def get_gsu_candidates_no_vote(self) -> None:
        """Returns all candidates with no votes applied at all"""
        positions = ["President", "GSU Officer", "Faculty Officer"]
        for position in positions:
            candidates_list = self.get_candidates(position)
            for candidate in candidates_list:
                if candidate["number_of_votes_1st"] == 0 and candidate["number_of_votes_2nd"] == 0 and candidate[
                    "number_of_votes_3rd"] == 0 and candidate["number_of_votes_4th"] == 0:
                    print(candidate["candidate_name"], position)


if __name__ == "__main__":
    VSD = VotingSystemDatabase()
    entry = input("Do you want to add job Description?\n")
    if entry.lower() == "yes":
        print("Enter GSU position: 1- President, 2- Faculty Officer, 3- GSU Officer")
        job_description = int(input("Please select a choice between 1-3: "))
        job_title = '"'
        if job_description == 1:
            job_title = "President"
        elif job_description == 2:
            job_title = "GSU Officer"
        elif job_description == 3:
            job_title = "Faculty Officer"
        else:
            print("This option does not exist ")
            exit()

        with open("GSU_job_description.txt", "a") as f:
            message = input("Enter job description: ")
            f.write(job_title + ": " + message + "\n");
