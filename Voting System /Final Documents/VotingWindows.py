# Created by Aniket Basu and Joao Jesus
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import datetime
import VotingSystemDatabase
import Students


class SystemWindow:

    def __init__(self, vsd: object):
        self._window = tk.Tk()
        self._VSD = vsd
        self._window_properties = {}
        self.next_page_to_navigate = ""
        self._window.protocol("WM_DELETE_WINDOW", self._window_closed)  # Function call when red cross is pressed

    def _create_window(self) -> None:
        """Abstract Method"""
        pass

    def _create_button(self, text: str, font: tuple, command: (), bg_color="#0040FF", fg_color="#FFFFFF",
                       active_bg="#0030FF", active_fg="#FFFFFF", border_width=0):
        """Creates a tkinter button"""
        return tk.Button(self._window, text=text, font=font, bg=bg_color, fg=fg_color,
                         activebackground=active_bg, activeforeground=active_fg, bd=border_width,
                         command=command)

    def _window_closed(self) -> None:
        """Function that is called when the user closes the GUI window"""
        user_want_to_exit = messagebox.askyesno("Exit Voting System", "Are you sure you wish to exit the Voting "
                                                                      "System?")
        if user_want_to_exit:
            self.next_page_to_navigate = "Exit"
            self.close_window()

    @staticmethod
    def _create_message_box(title: str, text: str) -> object:
        """Creates a tkinter message box object"""
        return messagebox.showinfo(title, text)

    # PUBLIC
    def open_window(self) -> None:
        """Displays the tkinter GUI"""
        self._window.mainloop()

    # PUBLIC
    def close_window(self) -> None:
        """Destroys the tkinter GUI Window"""
        self._window.destroy()

    # PUBLIC
    def create_image(self) -> None:
        """Creates the background for the GUI"""
        self._background_image = tk.PhotoImage(master=self._window, file="uni.gif")
        self._background_label = tk.Label(self._window, image=self._background_image)
        self._background_label.place(relwidth=1, relheight=1, relx=0, rely=0)


class LoginWindow(SystemWindow):

    def __init__(self, vsd: object):
        super().__init__(vsd)
        self._window_properties = {
            "LOC_X": 0.375,
            "LOC_Y": 0.05,
            "HEIGHT": 0.2,
            "WIDTH": 0.65,
            "TEXT_BG": "#3C6BDB",
            "TEXT_FG": "#FFFFFF"
        }
        self._window.title("LogIn Page")
        self._username = tk.StringVar()
        self._password = tk.StringVar()
        self._student_ID = None
        self._background_image = None
        self._create_window()

    def _create_window(self) -> None:
        """Creates and applies all the GUI elements onto the window"""
        self._canvas = tk.Canvas(self._window, width=1200, height=600)
        self._canvas.pack()
        self._background_image = tk.PhotoImage(master=self._window, file="uni.gif")
        self._background_label = tk.Label(self._window, image=self._background_image)
        self._background_label.place(relwidth=1, relheight=1, relx=0, rely=0)
        self._username_label = tk.Label(self._window,
                                        text="Username:",
                                        font=("Helvetica", 30, "bold"),
                                        background=self._window_properties["TEXT_BG"],
                                        foreground=self._window_properties["TEXT_FG"])
        self._username_label.place(relwidth=self._window_properties["WIDTH"] - 0.4,
                                   relheight=self._window_properties["HEIGHT"] - 0.1,
                                   relx=self._window_properties["LOC_X"], rely=self._window_properties["LOC_Y"])
        self._password_label = tk.Label(self._window,
                                        text="Password:",
                                        font=("Helvetica", 30, "bold"),
                                        background=self._window_properties["TEXT_BG"],
                                        foreground=self._window_properties["TEXT_FG"])
        self._password_label.place(relwidth=self._window_properties["WIDTH"] - 0.4,
                                   relheight=self._window_properties["HEIGHT"] - 0.1,
                                   relx=self._window_properties["LOC_X"], rely=self._window_properties["LOC_Y"] + 0.35)
        self._username_entry = tk.Entry(self._window,
                                        justify="center",
                                        font=("Helvetica", 28),
                                        textvariable=self._username)
        self._username_entry.place(relx=self._window_properties["LOC_X"] - 0.175,
                                   rely=self._window_properties["LOC_Y"] + 0.13,
                                   relwidth=self._window_properties["WIDTH"],
                                   relheight=self._window_properties["HEIGHT"])
        self._user_password_entry = tk.Entry(self._window,
                                             show="*",
                                             justify="center",
                                             font=("Helvetica", 28),
                                             textvariable=self._password)
        self._user_password_entry.place(relx=self._window_properties["LOC_X"] - 0.175,
                                        rely=self._window_properties["LOC_Y"] + 0.48,
                                        relwidth=self._window_properties["WIDTH"],
                                        relheight=self._window_properties["HEIGHT"])
        self._login_button = self._create_button("Log  In", ("Helvetica", 28, "normal"),
                                                 self._validate_username_password)
        self._login_button.place(relx=self._window_properties["LOC_X"] - 0.075,
                                 rely=self._window_properties["LOC_Y"] + 0.75,
                                 relwidth=self._window_properties["WIDTH"] - 0.2,
                                 relheight=self._window_properties["HEIGHT"] - 0.1)

    def _check_for_already_votes(self) -> None:
        messagebox.showerror("Error Info", "You have already Voted, you cannot vote twice")
        self.next_page_to_navigate = "Timer"
        self.close_window()

    def _validate_username_password(self) -> None:
        """Checks to see if the user has been able to log in correctly"""
        username = self._username.get()
        password = self._password.get()
        login_details_valid = self._VSD.get_login_details_valid(username, password)
        if login_details_valid:
            # self._create_message_box("Login Result", "You are eligible to Vote.")
            self.close_window()
            self.next_page_to_navigate = "President"
            self._student_ID = self._VSD.get_index_of_username(username)
            self._info = self._VSD.get_student_information(self._student_ID)
        else:
            messagebox.showerror("Login Result", "You are not eligible to Vote or incorrect details, Try Again.")

    # PUBLIC
    def get_student_id(self) -> int:
        """Returns the ID of the student"""
        return self._student_ID


class VotePageTemplate(SystemWindow):

    def __init__(self, vsd: object, running_position: str, student_obj: object):
        super().__init__(vsd)
        self._canvas = tk.Canvas(self._window, width=1700, height=1000)
        self._canvas.pack()
        self._student_obj = student_obj
        self._running_position = running_position
        self.next_page_to_navigate = ""
        self._scroll_bar_candidate_list = tk.Scrollbar(self._window)
        self._candidate_list = tk.Listbox(self._window, font=("Helvetica", 16),
                                          yscrollcommand=self._scroll_bar_candidate_list.set)
        self._all_selected_candidates = {
            "1st": "",
            "2nd": "",
            "3rd": "",
            "4th": ""
        }
        self._window_properties = {
            "LOC_X": 0.075,
            "LOC_Y": 0.125,
            "HEIGHT": 0.36,
            "WIDTH": 0.15,
            "TEXT_BG": "#3C6BDB",
            "TEXT_FG": "#FFFFFF"
        }

        # Create entry fields for all 4 options
        self._selected_candidate_1st_entry = tk.StringVar()
        self._selected_candidate_2nd_entry = tk.StringVar()
        self._selected_candidate_3rd_entry = tk.StringVar()
        self._selected_candidate_4th_entry = tk.StringVar()

        # Create images for all 4 options
        self._image_1st_position = tk.PhotoImage(file="1.gif")
        self._image_2nd_position = tk.PhotoImage(file="2.gif")
        self._image_3rd_position = tk.PhotoImage(file="3.gif")
        self._image_4th_position = tk.PhotoImage(file="4.gif")

        # Create labels for all 4 options
        self._label_candidate_1st = tk.Label(self._window, image=self._image_1st_position, bg="black", fg="blue")
        self._label_candidate_2nd = tk.Label(self._window, image=self._image_2nd_position, bg="black", fg="blue")
        self._label_candidate_3rd = tk.Label(self._window, image=self._image_3rd_position, bg="black", fg="blue")
        self._label_candidate_4th = tk.Label(self._window, image=self._image_4th_position, bg="black", fg="blue")

        # Create buttons for all 4 options
        self._select_candidate_1st_button = self._create_pick_candidate_button("Pick a Candidate",
                                                                               ("Helvetica", 14, "bold"),
                                                                               1, "#3C6BDB",
                                                                               "#FFFFFF",
                                                                               "#0000FF", "#0088FF")
        self._select_candidate_1st_button.config(justify="center")
        self._select_candidate_2nd_button = self._create_pick_candidate_button("Pick a Candidate",
                                                                               ("Helvetica", 14, "bold"),
                                                                               2, "#3C6BDB",
                                                                               "#FFFFFF",
                                                                               "#0000FF", "#0088FF")
        self._select_candidate_2nd_button.config(justify="center")
        self._select_candidate_3rd_button = self._create_pick_candidate_button("Pick a Candidate",
                                                                               ("Helvetica", 14, "bold"),
                                                                               3, "#3C6BDB",
                                                                               "#FFFFFF",
                                                                               "#0000FF", "#0088FF")
        self._select_candidate_3rd_button.config(justify="center")
        self._select_candidate_4th_button = self._create_pick_candidate_button("Pick a Candidate",
                                                                               ("Helvetica", 14, "bold"),
                                                                               4, "#3C6BDB",
                                                                               "#FFFFFF",
                                                                               "#0000FF", "#0088FF")
        self._select_candidate_4th_button.config(justify="center")
        self._create_candidate_list()
        self._candidate_names_label = tk.Label(self._window, text="Names of Candidates", font=("Helvetica", 20, "bold"))
        self._instruction_label = tk.Label(self._window, text="Choose your " + running_position,
                                           font=("Helvetica", 20, "bold"))

        # Create entry fields to hold values
        self._candidate_1_name = tk.Entry(self._window, textvariable=self._selected_candidate_1st_entry,
                                          font=("Helvetica", 16, "bold"), bg="white")
        self._candidate_2_name = tk.Entry(self._window, textvariable=self._selected_candidate_2nd_entry,
                                          font=("Helvetica", 16, "bold"), bg="white")
        self._candidate_3_name = tk.Entry(self._window, textvariable=self._selected_candidate_3rd_entry,
                                          font=("Helvetica", 16, "bold"), bg="white")
        self._candidate_4_name = tk.Entry(self._window, textvariable=self._selected_candidate_4th_entry,
                                          font=("Helvetica", 16, "bold"), bg="white")

        # Create Next and Skip Button
        self._next_button = self._create_button("Next", ("Helvetica", 18, "normal"), self._go_next_page)
        self._skip_button = self._create_button("Skip All", ("Helvetica", 18, "normal"), self._skip_all_pages)

        # Place everything
        self._candidate_names_label.place(relx=0.02, rely=0.05, relwidth=0.215, relheight=0.05)
        self._instruction_label.place(relx=0.525, rely=0.05, relwidth=0.215, relheight=0.0575)
        self._candidate_list.place(relx=0.025, rely=0.125, relwidth=0.2, relheight=0.5)

        self._label_candidate_1st.place(relx=self._window_properties["LOC_X"] + 0.225,
                                        rely=self._window_properties["LOC_Y"],
                                        relwidth=self._window_properties["WIDTH"],
                                        relheight=self._window_properties["HEIGHT"])

        self._label_candidate_2nd.place(relx=self._window_properties["LOC_X"] + 0.4,
                                        rely=self._window_properties["LOC_Y"],
                                        relwidth=self._window_properties["WIDTH"],
                                        relheight=self._window_properties["HEIGHT"])

        self._label_candidate_3rd.place(relx=self._window_properties["LOC_X"] + 0.575,
                                        rely=self._window_properties["LOC_Y"],
                                        relwidth=self._window_properties["WIDTH"],
                                        relheight=self._window_properties["HEIGHT"])

        self._label_candidate_4th.place(relx=self._window_properties["LOC_X"] + 0.75,
                                        rely=self._window_properties["LOC_Y"],
                                        relwidth=self._window_properties["WIDTH"],
                                        relheight=self._window_properties["HEIGHT"])

        # BX = 0.1 BY = 0.5
        # Labels to hold selected candidates
        self._candidate_1_name.place(relx=0.3, rely=0.5, relwidth=0.15, relheight=0.05)
        self._candidate_2_name.place(relx=0.475, rely=0.5, relwidth=0.15, relheight=0.05)
        self._candidate_3_name.place(relx=0.65, rely=0.5, relwidth=0.15, relheight=0.05)
        self._candidate_4_name.place(relx=0.825, rely=0.5, relwidth=0.15, relheight=0.05)

        # Buttons to pick candidates
        self._select_candidate_1st_button.place(relx=0.325, rely=0.6, relwidth=0.1, relheight=0.05)
        self._select_candidate_2nd_button.place(relx=0.5, rely=0.6, relwidth=0.1, relheight=0.05)
        self._select_candidate_3rd_button.place(relx=0.675, rely=0.6, relwidth=0.1, relheight=0.05)
        self._select_candidate_4th_button.place(relx=0.85, rely=0.6, relwidth=0.1, relheight=0.05)

        # Place Next and skip button
        self._next_button.place(relx=0.85, rely=0.775, relwidth=0.075, relheight=0.075)
        self._skip_button.place(relx=0.725, rely=0.775, relwidth=0.075, relheight=0.075)

    def _create_pick_candidate_button(self, text: str, font: tuple, param: int, bg_color="#0040FF", fg_color="#FFFFFF",
                                      active_bg="#0030FF", active_fg="#FFFFFF", border_width=0):
        """Creates a tkinter button"""
        return tk.Button(self._window, text=text, font=font, bg=bg_color, fg=fg_color,
                         activebackground=active_bg, activeforeground=active_fg, bd=border_width,
                         command=lambda: self._select_candidate(param))

    def _skip_all_pages(self) -> None:
        """Skips the renaming voting pages"""
        self._VSD.set_student_as_voted(self._student_obj.ID)
        self._confirmation_box = messagebox.askokcancel("Confirmation", "Are you sure you want to skip voting?"
                                                                        "Note:You won't be able to vote again.")
        if self._confirmation_box:
            self.next_page_to_navigate = "Results"
            self.close_window()

    def _go_next_page(self) -> None:
        """Tells the main system to go to the next page"""
        self._VSD.set_student_as_voted(self._student_obj.ID)
        if not self._duplicates_found() and self._first_position_set():
            if self._running_position == "President":
                self.next_page_to_navigate = "GSU Officer"
                self._apply_votes()
                self.close_window()
            elif self._running_position == "GSU Officer":
                self.next_page_to_navigate = "Faculty Officer"
                self._apply_votes()
                self.close_window()
            elif self._running_position == "Faculty Officer":
                self.next_page_to_navigate = "Results"
                self._apply_votes()
                self.close_window()
        else:
            messagebox.showerror("Next Page Error", "You must not have any duplicates and at least the first "
                                                    "position must be set")

    def _duplicates_found(self) -> bool:
        """Returns true if duplicates are found in the all_selected_candidates dictionary"""
        match_found = False
        all_values = list(self._all_selected_candidates.values())
        for item in all_values:
            if item != "" and all_values.count(item) > 1:
                match_found = True
                break
        return match_found

    def _first_position_set(self) -> bool:
        """Returns true if the first position has been provided"""
        return self._all_selected_candidates["1st"] != ""

    def _select_candidate(self, position: int) -> None:
        """Selects a candidate and sets it to the position specified"""
        users_choice = self._get_candidate_selected()
        if position == 1:
            self._all_selected_candidates["1st"] = users_choice
            self._selected_candidate_1st_entry.set(users_choice)
        elif position == 2:
            self._all_selected_candidates["2nd"] = users_choice
            self._selected_candidate_2nd_entry.set(users_choice)
        elif position == 3:
            self._all_selected_candidates["3rd"] = users_choice
            self._selected_candidate_3rd_entry.set(users_choice)
        elif position == 4:
            self._all_selected_candidates["4th"] = users_choice
            self._selected_candidate_4th_entry.set(users_choice)

    def _get_candidate_selected(self) -> str:
        """Gets the candidate selected in the list"""
        return self._candidate_list.get(tk.ACTIVE)

    def _create_candidate_list(self) -> None:
        """Adds the candidates to the list of candidates"""
        if self._running_position == "Faculty Officer":
            line_number = 1
            candidate_list = self._VSD.get_candidates(self._running_position, self._student_obj.faculty)
            if self._student_obj.user_type == "candidate":
                candidate_obj = Students.Candidate(self._VSD.get_index_of_username(self._student_obj.username))
                for candidate_info in candidate_list:
                    if candidate_info["candidate_name"] == candidate_obj.candidate_name:
                        candidate_list.remove(candidate_info)
            for candidate in candidate_list:
                self._candidate_list.insert(line_number, candidate["candidate_name"])
                line_number += 1
        else:
            line_number = 1
            candidate_list = self._VSD.get_candidates(self._running_position)
            if self._student_obj.user_type == "candidate":
                candidate_obj = Students.Candidate(self._VSD.get_index_of_username(self._student_obj.username))
                for candidate_info in candidate_list:
                    if candidate_info["candidate_name"] == candidate_obj.candidate_name:
                        candidate_list.remove(candidate_info)
            for candidate in candidate_list:
                self._candidate_list.insert(line_number, candidate["candidate_name"])
                line_number += 1

    def _apply_votes(self) -> None:
        """Applies the user's votes for the selected candidates to the database"""
        candidates = list(self._all_selected_candidates.values())
        candidate_positions = []
        for candidate in candidates:
            index = self._VSD.get_index_of_candidate_name(candidate)
            if index == -1:
                candidate_positions.append([])
            else:
                candidate_positions.append([index])
        if len(candidate_positions) < 4:
            while len(candidate_positions) != 4:
                candidate_positions.append([])
        self._VSD.apply_student_votes(candidate_positions[0], candidate_positions[1], candidate_positions[2],
                                      candidate_positions[3])

    # PUBLIC
    def get_all_candidates(self) -> list:
        """Returns a list of all the candidates the user has voted for"""
        return list(self._all_selected_candidates.values())


class TimerPage(SystemWindow):

    def __init__(self, vsd: object):
        super().__init__(vsd)
        self._window.title("Count Down")
        self._canvas = tk.Canvas(self._window, width=1200, height=600)
        self._canvas.pack()
        self._current_date = datetime.datetime.now()
        self._remaining_time = ""
        self._create_window()

    def _set_time(self) -> None:
        """Sets the remaining time for results page to show"""
        self._current_date = datetime.datetime.now()
        self._remaining_time = (self._VSD.RESULTS_DATE - self._current_date)
        self._window.after(200, self._set_time)
        self._set_remaining_time = self._remaining_time - datetime.timedelta(
            microseconds=self._remaining_time.microseconds)
        self._timer_label["text"] = self._set_remaining_time

    def _create_window(self) -> None:
        """Displays teh tkinter GUI of the page"""
        # Create Elements
        self.create_image()
        self._info_label = tk.Label(self._window, text="Thank you for voting the results will be given out in:",
                                    font=("Helvetica", 20, "bold"), background="#3C6BDB",
                                    foreground="white")
        self._ok_button = self._create_button("OK", ("Helvetica", 20, "bold"), command=self._close_timer)
        self._timer_label = tk.Label(self._window, text="", font=("Helvetica", 25, "bold"), background="#3C6BDB",
                                     foreground="white")
        # Place Elements
        self._info_label.place(relx=0.225, rely=0.25, relwidth=0.6, relheight=0.125)
        self._ok_button.place(relx=0.7, rely=0.8, relwidth=0.15, relheight=0.1)
        self._timer_label.place(relx=0.4, rely=0.4, relwidth=0.25, relheight=0.125)
        self._set_time()

    def _close_timer(self) -> None:
        """Prepares the page for closing"""
        self.next_page_to_navigate = "Exit"
        self.close_window()


class ResultsPageTemplate(SystemWindow):

    def __init__(self, vsd: object, student_obj: object):
        super().__init__(vsd)
        self._window.title("Results Page")
        self._student_obj = student_obj
        self._canvas = tk.Canvas(self._window, width=1500, height=900)
        self._canvas.pack()
        self._title_label_text = ("Candidate:", "1st", "2nd", "3rd", "4th")
        self._VSD = vsd
        self._all_labels_for_positions = []
        self._selected_position = ""
        self._top_candidate = ""
        self._votes_for_top_candidate = 0
        self._total_votes = 0
        self._create_window()
        self._set_all_candidate_data("President")
        self.open_window()

    def _box_choice(self):
        """"Acts according to the user input on the box"""
        choice = self._option_box.get()
        self._set_all_candidate_data(choice)

    def _set_all_candidate_data(self, running_position: str) -> None:
        """Changes the results to show the top 4 candidates running in the current selected position"""
        if running_position == "Faculty Officer":
            candidates = self._VSD.get_top_four_candidates(running_position, self._student_obj.faculty)
        else:
            candidates = self._VSD.get_top_four_candidates(running_position)
        for row in range(4):
            self._all_labels_for_positions[row][0]["text"] = candidates[row]["candidate_name"]
            self._all_labels_for_positions[row][1]["text"] = candidates[row]["number_of_votes_1st"]
            self._all_labels_for_positions[row][2]["text"] = candidates[row]["number_of_votes_2nd"]
            self._all_labels_for_positions[row][3]["text"] = candidates[row]["number_of_votes_3rd"]
            self._all_labels_for_positions[row][4]["text"] = candidates[row]["number_of_votes_4th"]
        self._set_winner(candidates)

    def _set_winner(self, candidates: list) -> None:
        """Displays the winner of the selected running positions"""
        self._total_votes = 0
        for candidate in candidates:
            self._total_votes += int(candidate["number_of_votes_1st"])
            self._total_votes += int(candidate["number_of_votes_2nd"])
            self._total_votes += int(candidate["number_of_votes_3rd"])
            self._total_votes += int(candidate["number_of_votes_4th"])
        self._top_candidate = candidates[0]["candidate_name"]
        self._votes_for_top_candidate = candidates[0]["number_of_votes_1st"] + candidates[0]["number_of_votes_2nd"] + \
                                        candidates[0]["number_of_votes_3rd"] + candidates[0]["number_of_votes_4th"]

        # Condition to prevent ZeroDivisionError when total votes is 0
        if self._total_votes != 0:
            self._percentage = round((self._votes_for_top_candidate / self._total_votes) * 100, 0)
            self._name_label["text"] = self._top_candidate
            self._no_of_vote_label["text"] = str(self._votes_for_top_candidate) + "   (" + str(self._percentage) + "%)"
            self._total_no_label["text"] = self._total_votes

    def _close_results_window(self):
        self.next_page_to_navigate = "Exit"
        self.close_window()

    def _create_window(self) -> None:
        """Creates the GUI elements to display for this page"""
        # Option Field to select which running position results to display
        self._option_box = ttk.Combobox(self._window, values=["President", "GSU Officer", "Faculty Officer"],
                                        font=("Helvetica", 15))
        self._option_box.current(0)
        self._option_box.place(relx=0.4, rely=0.01, relwidth=0.2, relheight=0.06)

        # Button to change the running position that the results are displaying
        self._confirm_button = self._create_button("OK", font=("Helvetica", 20, "bold"), command=self._box_choice)
        self._confirm_button.place(relx=0.7, rely=0.01, relwidth=0.1, relheight=0.08)

        # Label to show the top winner for each running position
        self._winner_label = tk.Label(self._window, text="Winner :", font=("Helvetica", 20, "bold"))
        self._winner_label.place(relx=0.03, rely=0.6, relwidth=0.15, relheight=0.1)
        self._name_label = tk.Label(self._window, text="Winner's Name", font=("Helvetica", 20, "bold"))
        self._name_label.place(relx=0.25, rely=0.6, relwidth=0.15, relheight=0.1)

        # Exit button to leave the page
        self._exit_button = self._create_button("Exit", font=("Helvetica", 20, "bold"),
                                                command=self._close_results_window)
        self._exit_button.place(relx=0.7, rely=0.8, relwidth=0.15, relheight=0.1)

        # Label to show the number of votes the winner has received
        self._vote_label = tk.Label(self._window, text="Votes Received:", font=("Helvetica", 20, "bold"))
        self._vote_label.place(relx=0.01, rely=0.75, relwidth=0.25, relheight=0.1)
        self._no_of_vote_label = tk.Label(self._window, text="0", font=("Helvetica", 20, "bold"))
        self._no_of_vote_label.place(relx=0.25, rely=0.75, relwidth=0.15, relheight=0.1)

        # Label to show total number of votes given in the current running_position
        self._total_votes_label = tk.Label(self._window, text="Total vote cast over all:",
                                           font=("Helvetica", 20, "bold"))
        self._total_votes_label.place(relx=0.01, rely=0.85, relwidth=0.25, relheight=0.1)
        self._total_no_label = tk.Label(self._window, text="0", font=("Helvetica", 20, "bold"))
        self._total_no_label.place(relx=0.25, rely=0.85, relwidth=0.15, relheight=0.1)

        # Display the results on the page for the top 4 candidates in the selected running position
        self._candidate_label = tk.Label(self._window, text=self._title_label_text[0], font=("Helvetica", 22, "bold"))
        self._candidate_label.place(relx=0.18, rely=0.1, relwidth=0.1, relheight=0.1)
        for i in range(1, 5):
            x = (0.15 * i)
            self._title_label = tk.Label(self._window, text=self._title_label_text[i], font=("Helvetica", 22, "bold"))
            self._title_label.place(relx=0.2 + x, rely=0.1, relwidth=0.1, relheight=0.1)
        for row in range(4):
            self._all_labels_for_positions.append([])
            candidate_name = tk.Label(self._window, text="Candidate Names", font=("Helvetica", 20, "bold"))
            position1_value = tk.Label(self._window, text="VAL", font=("Helvetica", 20, "bold"))
            position2_value = tk.Label(self._window, text="VAL", font=("Helvetica", 20, "bold"))
            position3_value = tk.Label(self._window, text="VAL", font=("Helvetica", 20, "bold"))
            position4_value = tk.Label(self._window, text="VAL", font=("Helvetica", 20, "bold"))
            self._all_labels_for_positions[row].extend([candidate_name, position1_value, position2_value,
                                                        position3_value, position4_value])
            candidate_name.place(relx=0.04, rely=0.2 + (0.1 * row), relwidth=0.35, relheight=0.1)
            position1_value.place(relx=0.35, rely=0.2 + (0.1 * row), relwidth=0.10, relheight=0.1)
            position2_value.place(relx=0.5, rely=0.2 + (0.1 * row), relwidth=0.10, relheight=0.1)
            position3_value.place(relx=0.65, rely=0.2 + (0.1 * row), relwidth=0.10, relheight=0.1)
            position4_value.place(relx=0.8, rely=0.2 + (0.1 * row), relwidth=0.10, relheight=0.1)


class Job_description(SystemWindow):

    def __init__(self, vsd: object):
        super().__init__(vsd)
        self._window.title("Job Description")
        self._canvas = tk.Canvas(height=600, width=1200)
        self._canvas.pack()
        self.create_image()
        self._VSD = vsd

        self.name_list = tk.Listbox(self._window, font=("Helvetica", 15, "bold"))
        self.check_for_no_job_descriptions()
        self.name_list.place(relx=0.1, rely=0.25, relheight=0.7, relwidth=0.25)


        name_label = tk.Label(self._window, text="Candidates with no job details:", font=("Helvetica", 25, "bold"))
        name_label.place(relx=0.075, rely=0.1, relheight=0.1, relwidth=0.35)

        ok_button = self._create_button("OK", font=("Helvetica", 20, "bold"), command=self._window.destroy)
        ok_button.place(relx=0.8, rely=0.8, relheight=0.1, relwidth=0.15)

        #exit_button = self._create_button("Exit", font=("Helvetica", 20, "bold"), command=self._close_job_page)
        #exit_button.place(relx=0.8, rely=0.8, relwidth=0.15, relheight=0.1)

    def check_for_no_job_descriptions(self) -> list:
        """Reads all the names in """
        with open("GSU_job_description.txt", "r") as file:
            line_number =1
            for line in file:
                sentence = line.replace("\n", "")
                components = sentence.split(":")
                print(components)
                if components[1] == "":
                    print(True)
                    self.name_list.insert(line_number, components[0])
                    line_number += 1




    def _close_job_page(self):
        self.close_window()


if __name__ == "__main__":
    s = Students.StudentVoter(59)
    y = VSD = VotingSystemDatabase.VotingSystemDatabase()
    x = Job_description(s)
    x.open_window()
