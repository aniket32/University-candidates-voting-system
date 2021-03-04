# Created by Adnan Turan, Arbaaz Sheikh, Aniket Basu and Joao Jesus
import VotingSystemDatabase
import Students
import VotingWindows


def next_object(page_name: str, vsd: object, student_obj_param: object) -> object:
    """Gives the next object needed to navigate to another page"""
    new_object = None
    if vsd.RESULTS_DATE <= vsd.CURRENT_DATE and page_name != "Exit":
        new_object = VotingWindows.ResultsPageTemplate(vsd, student_obj)
    elif student_obj.has_voted and page_name != "Exit":
        new_object = VotingWindows.TimerPage(vsd)
    else:
        if page_name == "President" or page_name == "GSU Officer" or page_name == "Faculty Officer":
            new_object = VotingWindows.VotePageTemplate(vsd, page_name, student_obj_param)
        elif page_name == "Timer":
            new_object = VotingWindows.TimerPage(vsd)
        elif page_name == "Results":
            if vsd.RESULTS_DATE > vsd.CURRENT_DATE:
                new_object = VotingWindows.TimerPage(vsd)
            else:
                new_object = VotingWindows.ResultsPageTemplate(vsd, student_obj)
        elif page_name == "Exit":
            new_object = VotingWindows.SystemWindow
            new_object.next_page_to_navigate = "Exit"
        else:
            print("An error has occurred with the next page. Unknown page: " + page_name)
    return new_object


VSD = VotingSystemDatabase.VotingSystemDatabase()
studentObj = None
object_var = VotingWindows.LoginWindow(VSD)
object_var.open_window()

if VSD.RESULTS_DATE <= VSD.CURRENT_DATE:
    VSD.create_votes_file()
    VSD.create_summary_file()
    VSD.create_bottom_3_gsu_file()
    VSD.get_gsu_candidates_no_vote()
while object_var.next_page_to_navigate == "":
    pass
# When the loop has finished that means the page is logged in

if object_var.next_page_to_navigate != "Exit":
    student_obj = Students.StudentVoter(object_var.get_student_id())
    object_var = next_object(object_var.next_page_to_navigate, VSD, student_obj)


while object_var.next_page_to_navigate != "Exit":
    object_var.open_window()
    while object_var.next_page_to_navigate == "":
        pass
    object_var = next_object(object_var.next_page_to_navigate, VSD, student_obj)

exit()
