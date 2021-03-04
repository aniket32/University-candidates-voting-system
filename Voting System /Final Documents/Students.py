# Created by Adnan Turan

from VotingSystemDatabase import VotingSystemDatabase

VSD = VotingSystemDatabase()


class StudentVoter:

    def __init__(self, position: int):
        student_data = VSD.get_student_information(position)
        self._username = student_data["username"]
        self._user_type = student_data["user_type"]
        self._has_voted = student_data["has_voted"]
        self._faculty = student_data["student_faculty"]
        self._position = position
        self._votes = {
            "1st_position": [],
            "2nd_position": [],
            "3rd_position": [],
            "4th_position": [],
        }

    # PUBLIC
    def add_vote_for_candidate(self, position: str, candidate_index_arg: int) -> [bool, str]:
        """Adds the user's vote to the appropriate array according to the position sp
        message = ""ecified.
        Returns True if successful"""
        was_successful = False
        has_candidate_already_been_added  = False
        for key in self._votes:
            if candidate_index_arg in self._votes[key]:
                has_candidate_already_been_added = True
        if not has_candidate_already_been_added:
            self._votes[position].append(candidate_index_arg)
            was_successful = True
        else:
            message = "You have already voted for this candidate."
        return was_successful, message

    # PUBLIC
    # Create Summary File
    def apply_students_votes(self) -> None:
        """Applies all of the student's votes to the FormattedInformation.txt file"""
        if not self._has_voted:
            VSD.apply_student_votes(self._votes["1st_position"], self._votes["2nd_position"], \
                                    self._votes["3rd_position"], self._votes["4th_position"])
            self._set_student_has_voted()

    def _set_student_has_voted(self) -> None:
        """Sets the student as voted and calls the method in VSD to save it in the FormattedInformation.txt file"""
        self._has_voted = True
        VSD.set_student_as_voted(self._position)

    @property
    def has_voted(self):
        return self._has_voted

    @has_voted.setter
    def has_voted(self, value):
        return None

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        return None

    @property
    def user_type(self):
        return self._user_type

    @user_type.setter
    def user_type(self, value):
        return None

    @property
    def faculty(self):
        return self._faculty

    @faculty.setter
    def faculty(self, value):
        return None

    @property
    def ID(self):
        return self._position

    @ID.setter
    def ID(self, value):
        return None


class Candidate(StudentVoter):

    def __init__(self, position: int):
        super().__init__(position)
        student_data = VSD.get_student_information(position)
        self._candidate_name = student_data["candidate_name"]
        self._number_of_votes = {
            "1st_position": student_data["number_of_votes_1st"],
            "2nd_position": student_data["number_of_votes_2nd"],
            "3rd_position": student_data["number_of_votes_3rd"],
            "4th_position": student_data["number_of_votes_4th"]
        }

    # PUBLIC
    def get_number_of_votes_in_position(self, position: str) -> int:
        """Gets the number of votes the candidate has in a specific position e.g 1st_position, 2nd_position, etc"""
        return self._number_of_votes[position]

    @property
    def candidate_name(self):
        return self._candidate_name

    @candidate_name.setter
    def candidate_name(self, value):
        return None


if __name__ == "__main__":
    stu = StudentVoter(VSD.get_index_of_username("wingedCurlew4"))
    print(stu.user_type)

