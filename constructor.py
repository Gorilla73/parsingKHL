import db_KHL as db
from prettytable import PrettyTable
from main import ALL_TEAM
from create_table_with_average_values import ALL_NAME_STATISTICS
from datetime import datetime as DT


def get_date(x, format="%d.%m.%Y"):
    return DT.strptime(x[1], format)


def filling_negative_handicap_passability_table(value_handicap, dict_passability_handicap, count_matches):
    res_handicap = 0
    for key in dict_passability_handicap:
        if float(key) > float(value_handicap):
            res_handicap += dict_passability_handicap[key]

    return ["-" + value_handicap, f"{res_handicap}/{count_matches}"]

def filling_positive_handicap_passability_table(value_handicap, dict_passability_handicap, count_matches):
    res_handicap = 0
    for key in dict_passability_handicap:
        if -float(key) < float(value_handicap):
            res_handicap += dict_passability_handicap[key]

    return ["+" + value_handicap, f"{res_handicap}/{count_matches}"]


def filling_total_passability_table(value_total, dict_passability_total, count_matches):
    res_total_over = 0
    for key in dict_passability_total:
        if float(key) > float(value_total):
            res_total_over += dict_passability_total[key]

    return [value_total, f"{res_total_over}/{count_matches}", f"{count_matches - res_total_over}/{count_matches}"]

class Constructor:

    def __init__(self, team1, team2, name_statistic):
        self.__team1 = team1.replace("_", " ")
        self.__team2 = team2.replace("_", " ")
        self.__name_statistic = name_statistic

        self.__average_table_team1 = PrettyTable()
        self.__average_table_team1.field_names = ["Название_команды", "Побед", "Ничьих", "Поражений", "Ср_инд_тотал",
                                                "Ср_инд_тотал_соп", "Ср_Тотал", "Ср_разница",
                                                "Cр_квадр_откл_тотала", "Cр_квадр_откл_инд_тотала",
                                                "Cр_квадр_откл_инд_тотала_соп"]

        self.__average_table_team2 = PrettyTable()
        self.__average_table_team2.field_names = ["Название_команды", "Побед", "Ничьих", "Поражений", "Ср_инд_тотал",
                                                "Ср_инд_тотал_соп", "Ср_Тотал", "Ср_разница",
                                                "Cр_квадр_откл_тотала", "Cр_квадр_откл_инд_тотала",
                                                "Cр_квадр_откл_инд_тотала_соп"]

        self.__all_matches_table_team1 = PrettyTable()
        self.__all_matches_table_team1.field_names = ["Дата", "Матч", "Счет", "Коэффициенты",
                                                    "Броски_в_створ", "Голы_в_большинстве",
                                                    "Выигранные_вбрасывания", "Количество_двухминутных_удалений"]

        self.__all_matches_table_team2 = PrettyTable()
        self.__all_matches_table_team2.field_names = ["Дата", "Матч", "Счет", "Коэффициенты",
                                                    "Броски_в_створ", "Голы_в_большинстве",
                                                    "Выигранные_вбрасывания", "Количество_двухминутных_удалений"]

        self.column_statistic = {"Броски_в_створ": 4, "Голы_в_большинстве": 5, "Выигранные_вбрасывания": 6,
                                  "Количество_двухминутных_удалений": 7}

        self.__table_with_total_passability_team1 = PrettyTable()
        self.__table_with_total_passability_team1.field_names = ["Тотал", "ТБ", "ТМ"]

        self.__table_with_ind_total_passability_team1 = PrettyTable()
        self.__table_with_ind_total_passability_team1.field_names = ["Инд тотал", "ИТБ", "ИТМ"]

        self.__table_with_ind_total_opponent_passability_team1 = PrettyTable()
        self.__table_with_ind_total_opponent_passability_team1.field_names = ["Инд тотал 2", "ИТБ", "ИТМ"]

        self.__table_with_handicap_team1 = PrettyTable()
        self.__table_with_handicap_team1.field_names = [" ", "Ф"]

        self.__table_with_handicap_opponent_team1 = PrettyTable()
        self.__table_with_handicap_opponent_team1.field_names = [" ", "Ф2"]

        self.__table_with_total_passability_team2 = PrettyTable()
        self.__table_with_total_passability_team2.field_names = ["Тотал", "ТБ", "ТМ"]

        self.__table_with_ind_total_passability_team2 = PrettyTable()
        self.__table_with_ind_total_passability_team2.field_names = ["Инд тотал", "ИТБ", "ИТМ"]

        self.__table_with_ind_total_opponent_passability_team2 = PrettyTable()
        self.__table_with_ind_total_opponent_passability_team2.field_names = ["Инд тотал 2", "ИТБ", "ИТМ"]

        self.__table_with_handicap_team2 = PrettyTable()
        self.__table_with_handicap_team2.field_names = [" ", "Ф"]

        self.__table_with_handicap_opponent_team2 = PrettyTable()
        self.__table_with_handicap_opponent_team2.field_names = [" ", "Ф2"]


    def team1_matches_with_odds_and_home_filter(self, home=False, odds=None):

        name_table = "Статистика_всех_матчей_" + str(self.__team1).replace(" ", "_")

        self.__all_matches_table_team1.clear_rows()

        if home == False:
            if odds == None:

                conn, cur = db.connect_db()
                all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
                sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)
                for match in sorted_all_matches:
                    temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                    self.__all_matches_table_team1.add_row(temp_lst)

                return self.__all_matches_table_team1
            else:
                conn, cur = db.connect_db()
                all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
                sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)
                for match in sorted_all_matches:

                    team_home = match[2].split("-")[0]
                    lst_odds_in_match = match[4].split()
                    if team_home == self.__team1:
                        if (float(lst_odds_in_match[0]) > float(odds[0])) and (float(lst_odds_in_match[0]) < float(odds[1])):
                            temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                            self.__all_matches_table_team1.add_row(temp_lst)
                    else:
                        if (float(lst_odds_in_match[2]) > float(odds[0])) and (float(lst_odds_in_match[2]) < float(odds[1])):
                            temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                            self.__all_matches_table_team1.add_row(temp_lst)

                return self.__all_matches_table_team1

        else:
            if odds == None:
                conn, cur = db.connect_db()
                all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
                sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)

                for match in sorted_all_matches:
                    team_home = match[2].split("-")[0]
                    if team_home == self.__team1:
                        temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                        self.__all_matches_table_team1.add_row(temp_lst)

                return self.__all_matches_table_team1

            else:
                conn, cur = db.connect_db()
                all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
                sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)
                for match in sorted_all_matches:

                    team_home = match[2].split("-")[0]
                    lst_odds_in_match = match[4].split()
                    if team_home == self.__team1:
                        if (float(lst_odds_in_match[0]) > float(odds[0])) and (
                                float(lst_odds_in_match[0]) < float(odds[1])):
                            temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                            self.__all_matches_table_team1.add_row(temp_lst)

                return self.__all_matches_table_team1


    def team2_matches_with_odds_and_away_filter(self, away=False, odds=None):

        name_table = "Статистика_всех_матчей_" + str(self.__team2).replace(" ", "_")

        self.__all_matches_table_team2.clear_rows()

        if away == False:
            if odds == None:

                conn, cur = db.connect_db()
                all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
                sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)
                for match in sorted_all_matches:
                    temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                    self.__all_matches_table_team2.add_row(temp_lst)

                return self.__all_matches_table_team2
            else:
                conn, cur = db.connect_db()
                all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
                sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)
                for match in sorted_all_matches:

                    team_home = match[2].split("-")[0]
                    lst_odds_in_match = match[4].split()
                    if team_home == self.__team2:
                        if (float(lst_odds_in_match[0]) > float(odds[0])) and (
                                float(lst_odds_in_match[0]) < float(odds[1])):
                            temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                            self.__all_matches_table_team2.add_row(temp_lst)
                    else:
                        if (float(lst_odds_in_match[2]) > float(odds[0])) and (
                                float(lst_odds_in_match[2]) < float(odds[1])):
                            temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                            self.__all_matches_table_team2.add_row(temp_lst)

                return self.__all_matches_table_team2

        else:
            if odds == None:
                conn, cur = db.connect_db()
                all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
                sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)
                for match in sorted_all_matches:
                    team_away = match[2].split("-")[1]
                    if team_away == self.__team2:
                        temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                        self.__all_matches_table_team2.add_row(temp_lst)

                return self.__all_matches_table_team2

            else:
                conn, cur = db.connect_db()
                all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
                sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)
                for match in sorted_all_matches:

                    team_away = match[2].split("-")[1]
                    lst_odds_in_match = match[4].split()
                    if team_away == self.__team2:
                        if (float(lst_odds_in_match[2]) > float(odds[0])) and (
                                float(lst_odds_in_match[2]) < float(odds[1])):
                            temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                            self.__all_matches_table_team2.add_row(temp_lst)

                return self.__all_matches_table_team2

    def add_data_in_average_table_team1(self):

        table_name = "Таблица_со_средними_показателями_" + self.__name_statistic
        conn, cur = db.connect_db()
        all_state = cur.execute(f"""SELECT * FROM {table_name} WHERE Название_команды = ?""", [self.__team1.replace
                                                                                               (" ", "_")]).fetchall()
        self.__average_table_team1.add_row([all_state[0][i+1] for i in range(len(all_state[0]) - 1)])

        return self.__average_table_team1

    def add_data_in_average_table_team2(self):

        table_name = "Таблица_со_средними_показателями_" + self.__name_statistic
        conn, cur = db.connect_db()
        all_state = cur.execute(f"""SELECT * FROM {table_name} WHERE Название_команды = ?""", [self.__team2.replace
                                                                                               (" ", "_")]).fetchall()

        self.__average_table_team2.add_row([all_state[0][i+1] for i in range(len(all_state[0]) - 1)])

        return self.__average_table_team2


    def table_with_average_value_from_parameters_team1(self):

        average_difference = 0
        average_total = 0
        average_ind_total = 0
        average_ind_total_opponent = 0
        count_win = 0
        count_draw = 0
        count_lose = 0

        self.__average_table_team1.clear_rows()

        column = self.column_statistic[self.__name_statistic]
        count_all_matches = len(self.__all_matches_table_team1.rows)

        if count_all_matches == 0:
            lst_average_state = [self.__team1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.__average_table_team1.add_row(lst_average_state)
            return self.__average_table_team1

        for i in range(len(self.__all_matches_table_team1.rows)):
            match = self.__all_matches_table_team1.rows[i][1].split("-")
            state = self.__all_matches_table_team1.rows[i][column].split("-")

            average_total += float(float(state[0]) + float(state[1]))
            if match[0] == self.__team1:
                average_difference += float(float(state[0]) - float(state[1]))
                average_ind_total += float(state[0])
                average_ind_total_opponent += float(state[1])

                if state[0] > state[1]: count_win += 1
                if state[0] < state[1]: count_lose += 1
                if state[0] == state[1]: count_draw += 1

            else:
                average_difference += float(float(state[1]) - float(state[0]))
                average_ind_total += float(state[1])
                average_ind_total_opponent += float(state[0])

                if state[1] > state[0]: count_win += 1
                if state[1] < state[0]: count_lose += 1
                if state[0] == state[1]: count_draw += 1

        lst_average_state = [self.__team1, count_win, count_draw, count_lose,
                             round(average_ind_total / count_all_matches, 2),
                             round(average_ind_total_opponent / count_all_matches, 2),
                             round(average_total / count_all_matches, 2),
                             round(average_difference / count_all_matches, 2),
                             None, None, None]

        self.__average_table_team1.add_row(lst_average_state)
        return self.__average_table_team1


    def table_with_average_value_from_parameters_team2(self):

        average_difference = 0
        average_total = 0
        average_ind_total = 0
        average_ind_total_opponent = 0
        count_win = 0
        count_draw = 0
        count_lose = 0

        self.__average_table_team2.clear_rows()

        column = self.column_statistic[self.__name_statistic]
        count_all_matches = len(self.__all_matches_table_team2.rows)

        if count_all_matches == 0:
            lst_average_state = [self.__team2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.__average_table_team2.add_row(lst_average_state)
            return self.__average_table_team2

        for i in range(len(self.__all_matches_table_team2.rows)):
            match = self.__all_matches_table_team2.rows[i][1].split("-")
            state = self.__all_matches_table_team2.rows[i][column].split("-")

            average_total += float(float(state[0]) + float(state[1]))
            if match[0] == self.__team2:
                average_difference += float(float(state[0]) - float(state[1]))
                average_ind_total += float(state[0])
                average_ind_total_opponent += float(state[1])

                if state[0] > state[1]: count_win += 1
                if state[0] < state[1]: count_lose += 1
                if state[0] == state[1]: count_draw += 1

            else:
                average_difference += float(float(state[1]) - float(state[0]))
                average_ind_total += float(state[1])
                average_ind_total_opponent += float(state[0])

                if state[1] > state[0]: count_win += 1
                if state[1] < state[0]: count_lose += 1
                if state[0] == state[1]: count_draw += 1

        lst_average_state = [self.__team2, count_win, count_draw, count_lose,
                             round(average_ind_total / count_all_matches, 2),
                             round(average_ind_total_opponent / count_all_matches, 2),
                             round(average_total / count_all_matches, 2),
                             round(average_difference / count_all_matches, 2),
                             None, None, None]

        self.__average_table_team2.add_row(lst_average_state)
        return self.__average_table_team2


    def table_with_identical_average_indicator_team1(self, name_statistic, average_indicator_name,
                                                     permissible_deviation, home=False, odds=None):


        table_name = "Таблица_со_средними_показателями_" + name_statistic
        table_name_team1 = "Статистика_всех_матчей_" + str(self.__team1).replace(" ", "_")
        self.__all_matches_table_team1.clear_rows()

        conn, cur = db.connect_db()
        average_indicator_team1 = cur.execute(f"""SELECT {average_indicator_name} FROM {table_name} WHERE 
                                                Название_команды = ?""",
                                              [str(self.__team1).replace(" ", "_")]).fetchone()[0]
        average_indicator_team2 = cur.execute(f"""SELECT {average_indicator_name} FROM {table_name} WHERE 
                                        Название_команды = ?""", [str(self.__team2).replace(" ", "_")]).fetchone()[0]

        all_team_with_identical_average_indicator = cur.execute(f"""SELECT Название_команды FROM {table_name}
                                                WHERE {average_indicator_name} > ? AND {average_indicator_name} < ?
                                                AND {average_indicator_name} != ?""",
                                                [average_indicator_team2 - permissible_deviation,
                                                 average_indicator_team2 + permissible_deviation,
                                                average_indicator_team1]).fetchall()



        all_team_with_identical_average_indicator = [str(team[0]).replace("_", " ")
                                                     for team in all_team_with_identical_average_indicator]

        conn, cur = db.connect_db()
        all_matches = cur.execute(f"""SELECT * FROM {table_name_team1}""").fetchall()
        sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)

        if home == False:
            if odds == None:


                for match in sorted_all_matches:
                    lst_team_in_match = match[2].split("-")
                    if lst_team_in_match[0] in all_team_with_identical_average_indicator or \
                        lst_team_in_match[1] in all_team_with_identical_average_indicator:
                        self.__all_matches_table_team1.add_row([match[i + 1] for i in range(len(match) - 2)])
                return self.__all_matches_table_team1

            else:
                for match in sorted_all_matches:
                    lst_team_in_match = match[2].split("-")
                    odds_in_match = match[4].split()
                    if lst_team_in_match[0] in all_team_with_identical_average_indicator or \
                        lst_team_in_match[1] in all_team_with_identical_average_indicator:

                        if lst_team_in_match[0] == self.__team1 and float(odds_in_match[0]) > odds[0] \
                                and float(odds_in_match[0]) < odds[1]:
                            self.__all_matches_table_team1.add_row([match[i + 1] for i in range(len(match) - 2)])
                        if lst_team_in_match[1] == self.__team1 and float(odds_in_match[2]) > odds[0] \
                                and float(odds_in_match[2]) < odds[1]:
                            self.__all_matches_table_team1.add_row([match[i + 1] for i in range(len(match) - 2)])
                return self.__all_matches_table_team1

        else:
            if odds == None:
                for match in sorted_all_matches:
                    lst_team_in_match = match[2].split("-")
                    if lst_team_in_match[0] in all_team_with_identical_average_indicator or \
                        lst_team_in_match[1] in all_team_with_identical_average_indicator:

                        if lst_team_in_match[0] == self.__team1:
                            self.__all_matches_table_team1.add_row([match[i + 1] for i in range(len(match) - 2)])
                return self.__all_matches_table_team1

            else:
                for match in sorted_all_matches:
                    lst_team_in_match = match[2].split("-")
                    odds_in_match = match[4].split()
                    if lst_team_in_match[0] in all_team_with_identical_average_indicator or \
                            lst_team_in_match[1] in all_team_with_identical_average_indicator:

                        if lst_team_in_match[0] == self.__team1:
                            if lst_team_in_match[0] == self.__team1 and float(odds_in_match[0]) > odds[0] \
                                    and float(odds_in_match[0]) < odds[1]:
                                self.__all_matches_table_team1.add_row([match[i + 1] for i in range(len(match) - 2)])
                return self.__all_matches_table_team1

    def table_with_identical_average_indicator_team2(self, name_statistic, average_indicator_name,
                                                     permissible_deviation, away=False, odds=None):

        table_name = "Таблица_со_средними_показателями_" + name_statistic
        table_name_team2 = "Статистика_всех_матчей_" + str(self.__team2).replace(" ", "_")
        self.__all_matches_table_team2.clear_rows()

        conn, cur = db.connect_db()
        average_indicator_team2 = cur.execute(f"""SELECT {average_indicator_name} FROM {table_name} WHERE 
                                                Название_команды = ?""",
                                              [str(self.__team2).replace(" ", "_")]).fetchone()[0]
        average_indicator_team1 = cur.execute(f"""SELECT {average_indicator_name} FROM {table_name} WHERE 
                                        Название_команды = ?""", [str(self.__team1).replace(" ", "_")]).fetchone()[0]

        all_team_with_identical_average_indicator = cur.execute(f"""SELECT Название_команды FROM {table_name}
                                                WHERE {average_indicator_name} > ? AND {average_indicator_name} < ?
                                                AND {average_indicator_name} != ?""",
                                                                [average_indicator_team1 - permissible_deviation,
                                                                 average_indicator_team1 + permissible_deviation,
                                                                 average_indicator_team2]).fetchall()

        all_team_with_identical_average_indicator = [str(team[0]).replace("_", " ")
                                                     for team in all_team_with_identical_average_indicator]

        conn, cur = db.connect_db()
        all_matches = cur.execute(f"""SELECT * FROM {table_name_team2}""").fetchall()
        sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)

        if away == False:
            if odds == None:

                for match in sorted_all_matches:
                    lst_team_in_match = match[2].split("-")
                    if lst_team_in_match[0] in all_team_with_identical_average_indicator or \
                            lst_team_in_match[1] in all_team_with_identical_average_indicator:
                        self.__all_matches_table_team2.add_row([match[i + 1] for i in range(len(match) - 2)])
                return self.__all_matches_table_team2

            else:
                for match in sorted_all_matches:
                    lst_team_in_match = match[2].split("-")
                    odds_in_match = match[4].split()
                    if lst_team_in_match[0] in all_team_with_identical_average_indicator or \
                            lst_team_in_match[1] in all_team_with_identical_average_indicator:

                        if lst_team_in_match[0] == self.__team2 and float(odds_in_match[0]) > odds[0] \
                                and float(odds_in_match[0]) < odds[1]:
                            self.__all_matches_table_team1.add_row([match[i + 1] for i in range(len(match) - 2)])
                        if lst_team_in_match[1] == self.__team2 and float(odds_in_match[2]) > odds[0] \
                                and float(odds_in_match[2]) < odds[1]:
                            self.__all_matches_table_team2.add_row([match[i + 1] for i in range(len(match) - 2)])
                return self.__all_matches_table_team2

        else:
            if odds == None:
                for match in sorted_all_matches:
                    lst_team_in_match = match[2].split("-")
                    if lst_team_in_match[0] in all_team_with_identical_average_indicator or \
                            lst_team_in_match[1] in all_team_with_identical_average_indicator:

                        if lst_team_in_match[1] == self.__team2:
                            self.__all_matches_table_team2.add_row([match[i + 1] for i in range(len(match) - 2)])
                return self.__all_matches_table_team2

            else:
                for match in sorted_all_matches:
                    lst_team_in_match = match[2].split("-")
                    odds_in_match = match[4].split()
                    if lst_team_in_match[0] in all_team_with_identical_average_indicator or \
                            lst_team_in_match[1] in all_team_with_identical_average_indicator:

                        if lst_team_in_match[1] == self.__team2:
                            if lst_team_in_match[1] == self.__team2 and float(odds_in_match[2]) > odds[0] \
                                    and float(odds_in_match[2]) < odds[1]:
                                self.__all_matches_table_team2.add_row([match[i + 1] for i in range(len(match) - 2)])
                return self.__all_matches_table_team2


    def face_to_face_matches_team1(self, home=False):

        name_table = "Статистика_всех_матчей_" + str(self.__team1).replace(" ", "_")

        self.__all_matches_table_team1.clear_rows()
        if home == True:
            conn, cur = db.connect_db()
            all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
            sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)
            for match in sorted_all_matches:
                check_match = match[2].split("-")
                if self.__team1 == check_match[0] and self.__team2 == check_match[1]:
                    temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                    self.__all_matches_table_team1.add_row(temp_lst)

            return self.__all_matches_table_team1
        else:
            conn, cur = db.connect_db()
            all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
            sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)
            for match in sorted_all_matches:
                check_match = match[2].split("-")
                if (self.__team1 == check_match[0] and self.__team2 == check_match[1]) or \
                        (self.__team1 == check_match[1] and self.__team2 == check_match[0]):
                    temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                    self.__all_matches_table_team1.add_row(temp_lst)

            return self.__all_matches_table_team1


    def face_to_face_matches_team2(self, away=False):

        name_table = "Статистика_всех_матчей_" + str(self.__team2).replace(" ", "_")

        self.__all_matches_table_team2.clear_rows()
        if away == True:
            conn, cur = db.connect_db()
            all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
            sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)
            for match in sorted_all_matches:
                check_match = match[2].split("-")
                if self.__team1 == check_match[0] and self.__team2 == check_match[1]:
                    temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                    self.__all_matches_table_team2.add_row(temp_lst)

            return self.__all_matches_table_team2
        else:
            conn, cur = db.connect_db()
            all_matches = cur.execute(f"""SELECT * FROM {name_table}""").fetchall()
            sorted_all_matches = sorted(all_matches, key=get_date, reverse=True)
            for match in sorted_all_matches:
                check_match = match[2].split("-")
                if (self.__team1 == check_match[0] and self.__team2 == check_match[1]) or \
                        (self.__team1 == check_match[1] and self.__team2 == check_match[0]):
                    temp_lst = [match[i + 1] for i in range(len(match) - 2)]
                    self.__all_matches_table_team2.add_row(temp_lst)

            return self.__all_matches_table_team2


    def all_tables_with_passability_team1(self):

        # name_table_team1 = "Статистика_всех_матчей_" + str(self.__team1).replace(" ", "_")

        self.__table_with_total_passability_team1.clear_rows()
        self.__table_with_ind_total_passability_team1.clear_rows()
        self.__table_with_ind_total_opponent_passability_team1.clear_rows()
        self.__table_with_handicap_team1.clear_rows()
        self.__table_with_handicap_opponent_team1.clear_rows()

        column = self.column_statistic[self.__name_statistic]
        count_matches = len(self.__all_matches_table_team1.rows)

        min_total = 1000
        max_total = 0
        min_ind_total = 1000
        max_ind_total = 0
        min_ind_total_opponent = 1000
        max_ind_total_opponent = 0
        max_negative_handicap = 1000      #максимальная ф +
        max_positive_handicap = -1000   #максимальная фора -

        dict_total = {}
        dict_ind_total = {}
        dict_ind_total_opponent = {}
        dict_handicap = {}

        for i in range(count_matches):
            match = self.__all_matches_table_team1.rows[i][1].split("-")
            state = [int(i) for i in self.__all_matches_table_team1.rows[i][column].split("-")]

            if sum(state) < min_total: min_total = sum(state)
            if sum(state) > max_total: max_total = sum(state)

            if str(sum(state)) not in dict_total:
                dict_total[str(sum(state))] = 1
            else:
                dict_total[str(sum(state))] += 1

            if match[0] == self.__team1:
                if state[0] < min_ind_total: min_ind_total = state[0]
                if state[0] > max_ind_total: max_ind_total = state[0]

                if state[1] < min_ind_total_opponent: min_ind_total_opponent = state[1]
                if state[1] > max_ind_total_opponent: max_ind_total_opponent = state[1]

                if state[0] - state[1] > max_positive_handicap: max_positive_handicap = state[0] - state[1]
                if state[0] - state[1] < max_negative_handicap: max_negative_handicap = state[0] - state[1]

            #print(max_total, min_total, max_ind_total, min_ind_total, max_ind_total_opponent,
                # max_positive_handicap, max_negative_handicap)
                if str(state[0]) not in dict_ind_total:
                    dict_ind_total[str(state[0])] = 1
                else:
                    dict_ind_total[str(state[0])] += 1

                if str(state[1]) not in dict_ind_total_opponent:
                    dict_ind_total_opponent[str(state[1])] = 1
                else:
                    dict_ind_total_opponent[str(state[1])] += 1

                if str(state[0] - state[1]) not in dict_handicap:
                    dict_handicap[str(state[0] - state[1])] = 1
                else:
                    dict_handicap[str(state[0] - state[1])] += 1

            else:
                if state[1] < min_ind_total: min_ind_total = state[1]
                if state[1] > max_ind_total: max_ind_total = state[1]

                if state[0] < min_ind_total_opponent: min_ind_total_opponent = state[0]
                if state[0] > max_ind_total_opponent: max_ind_total_opponent = state[0]

                if state[1] - state[0] > max_positive_handicap: max_positive_handicap = state[1] - state[0]
                if state[1] - state[0] < max_negative_handicap: max_negative_handicap = state[1] - state[0]

                if str(state[1]) not in dict_ind_total:
                    dict_ind_total[str(state[1])] = 1
                else:
                    dict_ind_total[str(state[1])] += 1

                if str(state[0]) not in dict_ind_total_opponent:
                    dict_ind_total_opponent[str(state[0])] = 1
                else:
                    dict_ind_total_opponent[str(state[0])] += 1

                if str(state[1] - state[0]) not in dict_handicap:
                    dict_handicap[str(state[1] - state[0])] = 1
                else:
                    dict_handicap[str(state[1] - state[0])] += 1

        #заполняем списки для таблиц
        lst_total_passability = [[str(float(min_total) - 0.5), f"{count_matches}/{count_matches}", f"0/{count_matches}"]]

        lst_ind_total_passability = [[str(float(min_ind_total) - 0.5), f"{count_matches}/{count_matches}",
                                      f"0/{count_matches}"]]

        lst_ind_total_opponent_passability = [[str(float(min_ind_total_opponent) - 0.5),
                                               f"{count_matches}/{count_matches}", f"0/{count_matches}"]]

        lst_handicap = [[str(-(float(max_positive_handicap) + 0.5)), f"0/{count_matches}",]]

        lst_handicap_opponent = []

        for i in range(min_total + 1, max_total + 2):
            lst_total_passability.append(filling_total_passability_table(str(float(i) - 0.5), dict_total, count_matches))

        for i in range(min_ind_total + 1, max_ind_total + 2):
            lst_ind_total_passability.append(filling_total_passability_table(str(float(i) - 0.5), dict_ind_total,
                                                                             count_matches))

        for i in range(min_ind_total_opponent + 1, max_ind_total_opponent + 2):
            lst_ind_total_opponent_passability.append(filling_total_passability_table(str(float(i) - 0.5),
                                                                                      dict_ind_total_opponent,
                                                                                      count_matches))

        index = 0
        for i in range(max_positive_handicap - 1, -1, -1):
            lst_handicap.append(filling_negative_handicap_passability_table(str(float(i) + 0.5), dict_handicap,
                                                                            count_matches))
            passability_counter_handicap = "".join(lst_handicap[index][1].split("/")[0])
            lst_handicap_opponent.append([str(-float(lst_handicap[index][0])),
                                          f"{count_matches - int(passability_counter_handicap)}/{count_matches}"])
            index += 1


        lst_handicap = lst_handicap[::-1]
        passability_counter_handicap = "".join(lst_handicap[0][1].split("/")[0])
        lst_handicap_opponent.append([str(-float(lst_handicap[0][0])),
                                      f"{count_matches - int(passability_counter_handicap)}/{count_matches}"])
        lst_handicap_opponent = lst_handicap_opponent[::-1]

        index = len(lst_handicap)
        for i in range(0, -max_negative_handicap + 1):
            lst_handicap.append(filling_positive_handicap_passability_table(str(float(i) + 0.5), dict_handicap,
                                                                            count_matches))
            passability_counter_handicap = "".join(lst_handicap[index][1].split("/")[0])
            lst_handicap_opponent.insert(i, [str(str(-(float(i) + 0.5))),
                                          f"{count_matches - int(passability_counter_handicap)}/{count_matches}"])
            index += 1

        for i in lst_total_passability:
            self.__table_with_total_passability_team1.add_row(i)


        for i in lst_ind_total_passability:
            self.__table_with_ind_total_passability_team1.add_row(i)

        for i in lst_ind_total_opponent_passability:
            self.__table_with_ind_total_opponent_passability_team1.add_row(i)

        for i in lst_handicap:
            self.__table_with_handicap_team1.add_row(i)

        for i in lst_handicap_opponent:
            self.__table_with_handicap_opponent_team1.add_row(i)

        return (self.__table_with_total_passability_team1, self.__table_with_ind_total_passability_team1,
              self.__table_with_ind_total_opponent_passability_team1, self.__table_with_handicap_team1,
              self.__table_with_handicap_opponent_team1)

    def all_tables_with_passability_team2(self):

        # name_table_team1 = "Статистика_всех_матчей_" + str(self.__team1).replace(" ", "_")

        self.__table_with_total_passability_team2.clear_rows()
        self.__table_with_ind_total_passability_team2.clear_rows()
        self.__table_with_ind_total_opponent_passability_team2.clear_rows()
        self.__table_with_handicap_team2.clear_rows()
        self.__table_with_handicap_opponent_team2.clear_rows()

        column = self.column_statistic[self.__name_statistic]
        count_matches = len(self.__all_matches_table_team2.rows)

        min_total = 1000
        max_total = 0
        min_ind_total = 1000
        max_ind_total = 0
        min_ind_total_opponent = 1000
        max_ind_total_opponent = 0
        max_negative_handicap = 1000  # максимальная ф +
        max_positive_handicap = -1000  # максимальная фора -

        dict_total = {}
        dict_ind_total = {}
        dict_ind_total_opponent = {}
        dict_handicap = {}

        for i in range(count_matches):
            match = self.__all_matches_table_team2.rows[i][1].split("-")
            state = [int(i) for i in self.__all_matches_table_team2.rows[i][column].split("-")]

            if sum(state) < min_total: min_total = sum(state)
            if sum(state) > max_total: max_total = sum(state)

            if str(sum(state)) not in dict_total:
                dict_total[str(sum(state))] = 1
            else:
                dict_total[str(sum(state))] += 1

            if match[0] == self.__team2:
                if state[0] < min_ind_total: min_ind_total = state[0]
                if state[0] > max_ind_total: max_ind_total = state[0]

                if state[1] < min_ind_total_opponent: min_ind_total_opponent = state[1]
                if state[1] > max_ind_total_opponent: max_ind_total_opponent = state[1]

                if state[0] - state[1] > max_positive_handicap: max_positive_handicap = state[0] - state[1]
                if state[0] - state[1] < max_negative_handicap: max_negative_handicap = state[0] - state[1]

                # print(max_total, min_total, max_ind_total, min_ind_total, max_ind_total_opponent,
                # max_positive_handicap, max_negative_handicap)
                if str(state[0]) not in dict_ind_total:
                    dict_ind_total[str(state[0])] = 1
                else:
                    dict_ind_total[str(state[0])] += 1

                if str(state[1]) not in dict_ind_total_opponent:
                    dict_ind_total_opponent[str(state[1])] = 1
                else:
                    dict_ind_total_opponent[str(state[1])] += 1

                if str(state[0] - state[1]) not in dict_handicap:
                    dict_handicap[str(state[0] - state[1])] = 1
                else:
                    dict_handicap[str(state[0] - state[1])] += 1

            else:
                if state[1] < min_ind_total: min_ind_total = state[1]
                if state[1] > max_ind_total: max_ind_total = state[1]

                if state[0] < min_ind_total_opponent: min_ind_total_opponent = state[0]
                if state[0] > max_ind_total_opponent: max_ind_total_opponent = state[0]

                if state[1] - state[0] > max_positive_handicap: max_positive_handicap = state[1] - state[0]
                if state[1] - state[0] < max_negative_handicap: max_negative_handicap = state[1] - state[0]

                if str(state[1]) not in dict_ind_total:
                    dict_ind_total[str(state[1])] = 1
                else:
                    dict_ind_total[str(state[1])] += 1

                if str(state[0]) not in dict_ind_total_opponent:
                    dict_ind_total_opponent[str(state[0])] = 1
                else:
                    dict_ind_total_opponent[str(state[0])] += 1

                if str(state[1] - state[0]) not in dict_handicap:
                    dict_handicap[str(state[1] - state[0])] = 1
                else:
                    dict_handicap[str(state[1] - state[0])] += 1

        # заполняем списки для таблиц
        lst_total_passability = [
            [str(float(min_total) - 0.5), f"{count_matches}/{count_matches}", f"0/{count_matches}"]]

        lst_ind_total_passability = [[str(float(min_ind_total) - 0.5), f"{count_matches}/{count_matches}",
                                      f"0/{count_matches}"]]

        lst_ind_total_opponent_passability = [[str(float(min_ind_total_opponent) - 0.5),
                                               f"{count_matches}/{count_matches}", f"0/{count_matches}"]]

        lst_handicap = [[str(-(float(max_positive_handicap) + 0.5)), f"0/{count_matches}", ]]

        lst_handicap_opponent = []

        for i in range(min_total + 1, max_total + 2):
            lst_total_passability.append(
                filling_total_passability_table(str(float(i) - 0.5), dict_total, count_matches))

        for i in range(min_ind_total + 1, max_ind_total + 2):
            lst_ind_total_passability.append(filling_total_passability_table(str(float(i) - 0.5), dict_ind_total,
                                                                             count_matches))

        for i in range(min_ind_total_opponent + 1, max_ind_total_opponent + 2):
            lst_ind_total_opponent_passability.append(filling_total_passability_table(str(float(i) - 0.5),
                                                                                      dict_ind_total_opponent,
                                                                                      count_matches))

        index = 0
        for i in range(max_positive_handicap - 1, -1, -1):
            lst_handicap.append(filling_negative_handicap_passability_table(str(float(i) + 0.5), dict_handicap,
                                                                            count_matches))

            passability_counter_handicap = "".join(lst_handicap[index][1].split("/")[0])
            lst_handicap_opponent.append([str(-float(lst_handicap[index][0])),
                                          f"{count_matches - int(passability_counter_handicap)}/{count_matches}"])
            index += 1

        lst_handicap = lst_handicap[::-1]
        passability_counter_handicap = "".join(lst_handicap[0][1].split("/")[0])
        lst_handicap_opponent.append([str(-float(lst_handicap[0][0])),
                                      f"{count_matches - int(passability_counter_handicap)}/{count_matches}"])
        lst_handicap_opponent = lst_handicap_opponent[::-1]

        index = len(lst_handicap)

        for i in range(0, -max_negative_handicap + 1):
            lst_handicap.append(filling_positive_handicap_passability_table(str(float(i) + 0.5), dict_handicap,
                                                                            count_matches))
            passability_counter_handicap = "".join(lst_handicap[index][1].split("/")[0])
            lst_handicap_opponent.insert(i, [str(str(-(float(i) + 0.5))),
                                             f"{count_matches - int(passability_counter_handicap)}/{count_matches}"])
            index += 1


        for i in lst_total_passability:
            self.__table_with_total_passability_team2.add_row(i)

        for i in lst_ind_total_passability:
            self.__table_with_ind_total_passability_team2.add_row(i)

        for i in lst_ind_total_opponent_passability:
            self.__table_with_ind_total_opponent_passability_team2.add_row(i)

        for i in lst_handicap:
            self.__table_with_handicap_team2.add_row(i)

        for i in lst_handicap_opponent:
            self.__table_with_handicap_opponent_team2.add_row(i)

        return (self.__table_with_total_passability_team2, self.__table_with_ind_total_passability_team2,
                self.__table_with_ind_total_opponent_passability_team2, self.__table_with_handicap_team2,
                self.__table_with_handicap_opponent_team2)


def writing_data_to_file(team1, team2, odds_team1, odds_team2):

    file_names = ["shots_on_goal.txt", "power_plays_goals.txt", "faceoffs_won.txt", "penalties.txt"]
    index = 0
    for file_name in file_names:

        f_name_statistic = open(file_name, "w")

        obj = Constructor(team1, team2, ALL_NAME_STATISTICS[index])

        f_name_statistic.write(obj.add_data_in_average_table_team1().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(obj.team1_matches_with_odds_and_home_filter().get_string())
        f_name_statistic.write("\n")

        for i in obj.all_tables_with_passability_team1():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")


        f_name_statistic.write(obj.add_data_in_average_table_team2().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(obj.team2_matches_with_odds_and_away_filter().get_string())
        f_name_statistic.write("\n")
        for i in obj.all_tables_with_passability_team2():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")

        f_name_statistic.write("\n" + "ОЧНЫЕ ВСТРЕЧИ " + "=" * 100 + "\n")
        f_name_statistic.write("\n")

        _team1 = obj.face_to_face_matches_team1(home=False)
        f_name_statistic.write(obj.table_with_average_value_from_parameters_team1().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(_team1.get_string())
        f_name_statistic.write("\n")

        for i in obj.all_tables_with_passability_team1():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")

        _team2 = obj.face_to_face_matches_team2(away=False)
        f_name_statistic.write(obj.table_with_average_value_from_parameters_team2().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(_team2.get_string())
        f_name_statistic.write("\n")

        for i in obj.all_tables_with_passability_team2():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")

        f_name_statistic.write("\n" + "ОЧНЫЕ ВСТРЕЧИ ПО ФИЛЬТРУ ДОМ/ВЫЕЗД" + "=" * 100 + "\n")
        f_name_statistic.write("\n")

        _team1 = obj.face_to_face_matches_team1(home=True)
        f_name_statistic.write(obj.table_with_average_value_from_parameters_team1().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(_team1.get_string())
        f_name_statistic.write("\n")

        for i in obj.all_tables_with_passability_team1():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")

        _team2 = obj.face_to_face_matches_team2(away=True)
        f_name_statistic.write(obj.table_with_average_value_from_parameters_team2().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(_team2.get_string())
        f_name_statistic.write("\n")

        for i in obj.all_tables_with_passability_team2():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")

        f_name_statistic.write("\n" + "ФИЛЬТР ПО ДОМ/ВЫЕЗД " + "="*100 + "\n")
        f_name_statistic.write("\n")

        home_matches_team1 = obj.team1_matches_with_odds_and_home_filter(home=True)
        f_name_statistic.write(obj.table_with_average_value_from_parameters_team1().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(home_matches_team1.get_string())
        f_name_statistic.write("\n")

        for i in obj.all_tables_with_passability_team1():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")

        away_matches_team2 = obj.team2_matches_with_odds_and_away_filter(away=True)
        f_name_statistic.write(obj.table_with_average_value_from_parameters_team2().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(away_matches_team2.get_string())
        f_name_statistic.write("\n")

        for i in obj.all_tables_with_passability_team2():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")

        f_name_statistic.write("\n" + "ФИЛЬТР ПО ДОМ/ВЫЕЗД C ПОХОЖИМИ КОЭФФИЦИЕНТАМИ " + "=" * 100 + "\n")
        f_name_statistic.write("\n")

        _team1 = obj.team1_matches_with_odds_and_home_filter(home=True, odds=odds_team1)
        f_name_statistic.write(obj.table_with_average_value_from_parameters_team1().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(_team1.get_string())
        f_name_statistic.write("\n")

        for i in obj.all_tables_with_passability_team1():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")

        _team2 = obj.team2_matches_with_odds_and_away_filter(away=True, odds=odds_team2)
        f_name_statistic.write(obj.table_with_average_value_from_parameters_team2().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(_team2.get_string())
        f_name_statistic.write("\n")

        for i in obj.all_tables_with_passability_team2():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")

        f_name_statistic.write("\n" + "ФИЛЬТР C ПОХОЖИМИ КОЭФФИЦИЕНТАМИ " + "=" * 100 + "\n")
        f_name_statistic.write("\n")

        _team1 = obj.team1_matches_with_odds_and_home_filter(home=False, odds=odds_team1)
        f_name_statistic.write(obj.table_with_average_value_from_parameters_team1().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(_team1.get_string())
        f_name_statistic.write("\n")

        for i in obj.all_tables_with_passability_team1():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")

        _team2 = obj.team2_matches_with_odds_and_away_filter(away=False, odds=odds_team2)
        f_name_statistic.write(obj.table_with_average_value_from_parameters_team2().get_string())
        f_name_statistic.write("\n")
        f_name_statistic.write(_team2.get_string())
        f_name_statistic.write("\n")

        for i in obj.all_tables_with_passability_team2():
            f_name_statistic.write(i.get_string())
            f_name_statistic.write("\n")

        index += 1
        f_name_statistic.close()


def all_matches_with_identical_average_indicator(team1, team2, name_statistic, permissible_deviation,
                                                 average_indicator_name, home=False, away=False,
                                                 odds_team1=None, odds_team2=None):
    f = open("average_indicator_statistic.txt", "w")

    obj = Constructor(team1, team2, name_statistic)

    matches_team1 = obj.table_with_identical_average_indicator_team1(name_statistic, average_indicator_name,
                                                                     permissible_deviation, home=home, odds=odds_team1)

    f.write(obj.table_with_average_value_from_parameters_team1().get_string())
    f.write("\n")
    f.write(matches_team1.get_string())
    f.write("\n")

    for i in obj.all_tables_with_passability_team1():
        f.write(i.get_string())
        f.write("\n")

    matches_team2 = obj.table_with_identical_average_indicator_team2(name_statistic, average_indicator_name,
                                                                     permissible_deviation, away=away, odds=odds_team2)
    f.write(obj.table_with_average_value_from_parameters_team2().get_string())
    f.write("\n")
    f.write(matches_team2.get_string())
    f.write("\n")

    for i in obj.all_tables_with_passability_team2():
        f.write(i.get_string())
        f.write("\n")


# odd_team1 = float(1.55)
# odd_team2 = float(6.)
# odds = [[odd_team1 - 0.4, odd_team1 + 0.4], [odd_team2 - 0.4, odd_team2 + 0.4]]
# team1 = "Ак Барс"
# team2 = "Адмирал"


# odd_team1 = float(1.6)
# odd_team2 = float(5.3)
# odds = [[odd_team1 - 0.4, odd_team1 + 0.4], [odd_team2 - 0.4, odd_team2 + 0.4]]
# team1 = "СКА"
# team2 = "Торпедо"

# odd_team1 = float(1.55)
# odd_team2 = float(5.7)
# odds = [[odd_team1 - 0.4, odd_team1 + 0.4], [odd_team2 - 0.4, odd_team2 + 0.4]]
# team1 = "Локомотив"
# team2 = "Витязь"

# odd_team1 = float(2.05)
# odd_team2 = float(3.6)
# odds = [[odd_team1 - 0.4, odd_team1 + 0.4], [odd_team2 - 0.4, odd_team2 + 0.4]]
# team1 = "СКА"
# team2 = "ЦСКА"
#
# odd_team1 = float(2.15)
# odd_team2 = float(3.5)
# odds = [[odd_team1 - 0.4, odd_team1 + 0.4], [odd_team2 - 0.4, odd_team2 + 0.4]]
# team1 = "ЦСКА"
# team2 = "Локомотив"

# odd_team1 = float(2.15)
# odd_team2 = float(3.15)
# odds = [[odd_team1 - 0.4, odd_team1 + 0.4], [odd_team2 - 0.4, odd_team2 + 0.4]]
# team1 = "Металлург Магнитогорск"
# team2 = "Автомобилист"

# odd_team1 = float(3.8)
# odd_team2 = float(1.9)
# odds = [[odd_team1 - 0.4, odd_team1 + 0.4], [odd_team2 - 0.4, odd_team2 + 0.4]]
# team1 = "Северсталь"
# team2 = "ЦСКА"

# odd_team1 = float(1.8)
# odd_team2 = float(4.1)
# odds = [[odd_team1 - 0.4, odd_team1 + 0.4], [odd_team2 - 0.4, odd_team2 + 0.4]]
# team1 = "Динамо Москва"
# team2 = "Торпедо"

# odds = [[1.7, 2.3], [2.7, 3.3]]
# team1 = "Динамо Минск"
# team2 = "Спартак Москва"

# odds = [[3, 4], [1.7, 2.3]]
# team1 = "Спартак Москва"
# team2 = "ЦСКА"



writing_data_to_file(team1, team2, odds[0], odds[1])

all_matches_with_identical_average_indicator(team1, team2, ALL_NAME_STATISTICS[2],
                                             2, "Ср_разница", home=True, away=True,
                                             odds_team1=None, odds_team2=None)

