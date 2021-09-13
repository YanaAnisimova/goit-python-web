from abc import ABC, abstractmethod


class InterfaceControllerNotifications(ABC):
    @abstractmethod
    def start_view(self):
        pass

    @abstractmethod
    def displays_key_error(self, command):
        pass

    @abstractmethod
    def requests_command(self):
        pass


class InterfaceBirthdayCommandNotifications(ABC):
    @abstractmethod
    def requests_days_left_to_the_birthday(self):
        pass

    @abstractmethod
    def requests_input_number(self):
        pass

    @abstractmethod
    def display_who_to_wish_happy_birthday(self, user):
        pass

    @abstractmethod
    def reports_no_birthdays(self):
        pass


class InterfaceCreateCommandNotifications(ABC):
    @abstractmethod
    def requests_enter_the_note(self):
        pass

    @abstractmethod
    def requests_enter_birthday(self):
        pass

    @abstractmethod
    def requests_enter_email(self):
        pass

    @abstractmethod
    def requests_re_entry_of_the_data(self):
        pass

    @abstractmethod
    def requests_enter_name(self):
        pass

    @abstractmethod
    def requests_enter_phone(self):
        pass

    @abstractmethod
    def reports_the_existence_of_name_in_database(self, name):
        pass


class InterfaceDeleteCommandNotifications(ABC):
    @abstractmethod
    def reports_the_deletion_of_a_contact(self, user_name):
        pass

    @abstractmethod
    def requests_enter_name_to_changes_data(self):
        pass


class InterfaceEditCommandNotifications(ABC):
    @abstractmethod
    def requests_what_edit(self):
        pass

    @abstractmethod
    def requests_re_entry_of_the_data(self):
        pass

    @abstractmethod
    def reports_the_updated_of_a_contact(self, user_name):
        pass

    @abstractmethod
    def requests_command_edit_note(self):
        pass

    @abstractmethod
    def requests_enter_name_to_changes_data(self):
        pass

    @abstractmethod
    def reports_the_not_exist_of_name_in_database(self, name):
        pass

    @abstractmethod
    def requests_enter_the_note(self):
        pass

    @abstractmethod
    def requests_enter_birthday(self):
        pass

    @abstractmethod
    def requests_enter_email(self):
        pass

    @abstractmethod
    def requests_enter_name(self):
        pass

    @abstractmethod
    def requests_enter_phone(self):
        pass


class InterfaceHelpCommandNotifications(ABC):
    @abstractmethod
    def describes_commands(self):
        pass


class InterfaceExitCommandNotifications(ABC):
    @abstractmethod
    def displays_see_ya(self):
        pass


class InterfaceSearchCommandNotifications(ABC):
    @abstractmethod
    def requests_key_word_for_search(self):
        pass

    @abstractmethod
    def displays_matches(self, key_word, users):
        pass

    @abstractmethod
    def reports_no_matches(self):
        pass


class InterfaceShowCommandNotifications(ABC):
    @abstractmethod
    def displays_users(self, users):
        pass


class ConsoleControllerNotifications(InterfaceControllerNotifications):
    def start_view(self):
        print('Salut! Enter \'help\' to see the commands')

    def displays_key_error(self, command):
        print(f'Command "{command}" does not exist. Please try again')

    def requests_command(self):
        print('Enter your request: ', end='')


class ConsoleBirthdayCommandNotifications(InterfaceBirthdayCommandNotifications):
    def requests_days_left_to_the_birthday(self):
        print('Please enter days left to the needed date: ', end='')

    def requests_input_number(self):
        print('Please enter a valid number!', end='')

    def display_who_to_wish_happy_birthday(self, users):
        print(f'Please do not forget to tell them happy birthday!\n')
        ConsoleShowCommandNotifications().displays_users(users)

    def reports_no_birthdays(self):
        print('No congrats on this day!')


class ConsoleCreateCommandNotifications(InterfaceCreateCommandNotifications):
    def requests_enter_the_note(self):
        print('Enter the note: ', end='')

    def requests_enter_birthday(self):
        print('Enter your B-Day (YYYY-MM-DD): ', end='')

    def requests_enter_email(self):
        print('Enter your email: ', end='')

    def requests_re_entry_of_the_data(self):
        print('Incorrect, once more please!')

    def requests_enter_name(self):
        print('Enter your name: ', end='')

    def requests_enter_phone(self):
        print('Enter your phone number: ', end='')

    def reports_the_existence_of_name_in_database(self, name):
        print(f'Name "{name}" already exists in contact book!')


class ConsoleDeleteCommandNotifications(InterfaceDeleteCommandNotifications):
    def reports_the_deletion_of_a_contact(self, user_name):
        print(f'The contact named "{user_name}" has been deleted.')

    def requests_enter_name_to_changes_data(self):
        print('Enter a name to make data changes: ', end='')


class ConsoleEditCommandNotifications(InterfaceEditCommandNotifications):
    def requests_what_edit(self):
        print(f'What edit? (name/phone/email/birthday/note):  ', end='')

    def requests_re_entry_of_the_data(self):
        print('Incorrect, once more please!')

    def reports_the_updated_of_a_contact(self, user_name):
        print(f'Updated contact details with name "{user_name}".')

    def requests_command_edit_note(self):
        print('Change, add or delete notes?:  ', end='')

    def requests_enter_name_to_changes_data(self):
        print('Enter a name to make data changes: ', end='')

    def reports_the_not_exist_of_name_in_database(self, name):
        print(f'Name "{name}" does not exist in the contact book.')

    def requests_enter_name(self):
        print('Enter your name: ', end='')

    def requests_enter_phone(self):
        print('Enter your phone number: ', end='')

    def requests_enter_the_note(self):
        print('Enter the note: ', end='')

    def requests_enter_birthday(self):
        print('Enter your B-Day (DD.MM.YYYY): ', end='')

    def requests_enter_email(self):
        print('Enter your email: ', end='')


class ConsoleHelpCommandNotifications(InterfaceHelpCommandNotifications):
    def describes_commands(self):
        print('Hi, I\'m\' a bot. And I can:')
        print('<create>   /save contacts with names, addresses, phone numbers, '
              'emails and birthdays to the contact book;')
        print('<birthday> /display a list of contacts who have a birthday after a '
              'specified number of days from the current date;')
        print('<search>   /search for contacts and notes from the contact book. '
              'NOT LOOKING FOR BY DATE OF BIRTH !!!;')
        print('<edit>     /edit entries from the contact book, edit and delete notes;')
        print('<delete>   /delete entries from the contact book;')
        print('<show>     /display all contents of the contact book;')
        print('<exit>     /exit the program')


class ConsoleExitCommandNotifications(InterfaceExitCommandNotifications):
    def displays_see_ya(self):
        print(f'See ya!')


class ConsoleSearchCommandNotifications(InterfaceSearchCommandNotifications):
    def requests_key_word_for_search(self):
        print('Please, enter the key word: ', end='')

    def displays_matches(self, key_word, users):
        print(f'Found some users with matching key word "{key_word}":\n')
        ConsoleShowCommandNotifications().displays_users(users)

    def reports_no_matches(self):
        print('No matches!')


class ConsoleShowCommandNotifications(InterfaceShowCommandNotifications):
    def make_string_from_obj(self, arr, field):
        str_data = []
        for elem in arr:
            str_data.append(getattr(elem, field))
        return '\n'.join(str_data)

    def displays_users(self, users):
        """
        Function prints from user list
        :param users: a list with lines from data-file.txt
        :return: prints formatted table with user information from list
        """
        print('-' * 149)
        header = "| {:^5} | {:^25} | {:^25} | {:^30} | {:^15} | {:^30} |".format('#', 'name', 'phone', 'e-mail',
                                                                                 'birthday', 'note')
        print(header)
        print('-' * 149)
        # Getting user data
        count = 0
        for user in users:
            count += 1
            name = user.name
            phone = self.make_string_from_obj(user.phones, 'phone')
            e_mail = self.make_string_from_obj(user.emails, 'email')
            birthday = str(user.birthday)
            note = user.note if user.note else ''
            user_data = "| {:^5} | {:<25} | {:<25} | {:<30} | {:<15} | {:<30} |".format(count, name, phone, e_mail,
                                                                                        birthday, note)
            print(user_data)
        print('-' * 149)
