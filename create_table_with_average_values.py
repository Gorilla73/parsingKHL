import db_KHL as db
import math

ALL_NAME_STATISTICS = ["Броски_в_створ", "Голы_в_большинстве",
                       "Выигранные_вбрасывания", "Количество_двухминутных_удалений"]


def quantity_win(team, all_statistics):
    team = team.replace("_", " ")
    count_win = 0

    for element in all_statistics:
        match = element[0].split("-")

        if match[0] == team:
            if int(element[1].split("-")[0]) > int(element[1].split("-")[1]):
                count_win += 1
        else:
            if int(element[1].split("-")[1]) > int(element[1].split("-")[0]):
                count_win += 1

    return count_win


def quantity_lose(team, all_statistics):
    team = team.replace("_", " ")
    count_win = 0

    for element in all_statistics:
        match = element[0].split("-")

        if match[0] == team:
            if int(element[1].split("-")[1]) > int(element[1].split("-")[0]):
                count_win += 1
        else:
            if int(element[1].split("-")[0]) > int(element[1].split("-")[1]):
                count_win += 1

    return count_win


def quantity_draw(team, all_statistics):
    return len(all_statistics) - quantity_win(team, all_statistics) - quantity_lose(team, all_statistics)


def average_individual_total(team, all_statistics):
    team = team.replace("_", " ")
    amount_total = 0
    counter_matches = len(all_statistics)

    for element in all_statistics:
        match = element[0].split("-")

        if match[0] == team:
            total_in_one_match = int(element[1].split("-")[0])
            amount_total += total_in_one_match
        else:
            total_in_one_match = int(element[1].split("-")[1])
            amount_total += total_in_one_match

    return float(amount_total/counter_matches)


def average_individual_total_opponent(team, all_statistics):
    team = team.replace("_", " ")
    counter_matches = len(all_statistics)
    amount_total = 0

    for element in all_statistics:
        match = element[0].split("-")

        if match[0] == team:
            total_in_one_match = int(element[1].split("-")[1])
            amount_total += total_in_one_match
        else:
            total_in_one_match = int(element[1].split("-")[0])
            amount_total += total_in_one_match

    return float(amount_total/counter_matches)



def average_total(team, all_statistics):
    team = team.replace("_", " ")
    counter_matches = len(all_statistics)
    amount_total = 0

    for element in all_statistics:
        match = element[0].split("-")

        total_in_one_match = int(element[1].split("-")[0]) + int(element[1].split("-")[1])
        amount_total += total_in_one_match

    return float(amount_total / counter_matches)


def average_difference(team, all_statistics):
    team = team.replace("_", " ")
    counter_matches = len(all_statistics)
    amount_difference = 0

    for element in all_statistics:
        match = element[0].split("-")

        if match[0] == team:
            difference_in_one_match = int(element[1].split("-")[0]) - int(element[1].split("-")[1])
            amount_difference += difference_in_one_match
        else:
            difference_in_one_match = int(element[1].split("-")[1]) - int(element[1].split("-")[0])
            amount_difference += difference_in_one_match

    return float(amount_difference / counter_matches)

def mean_square_deviation_total(team, all_statistics):

    av_total = average_total(team, all_statistics)
    sum_squares_deviation_mean = 0

    for element in all_statistics:

        total_in_one_match = int(element[1].split("-")[0]) + int(element[1].split("-")[1])
        sum_squares_deviation_mean = (float(total_in_one_match) - av_total)**2

    variance = sum_squares_deviation_mean / len(all_statistics)

    return float(math.sqrt(variance))


def mean_square_deviation_individual_total(team, all_statistics):
    av_total = average_individual_total(team, all_statistics)
    sum_squares_deviation_mean = 0

    for element in all_statistics:
        match = element[0].split("-")

        if match[0] == team:
            ind_total_in_one_match = int(element[1].split("-")[0])
            sum_squares_deviation_mean = (float(ind_total_in_one_match) - av_total) ** 2
        else:
            ind_total_in_one_match = int(element[1].split("-")[1])
            sum_squares_deviation_mean = (float(ind_total_in_one_match) - av_total) ** 2

    variance = sum_squares_deviation_mean / len(all_statistics)

    return float(math.sqrt(variance))


def mean_square_deviation_individual_total_opponent(team, all_statistics):
    av_total = average_individual_total_opponent(team, all_statistics)
    sum_squares_deviation_mean = 0

    for element in all_statistics:
        match = element[0].split("-")

        if match[0] == team:
            ind_total_in_one_match = int(element[1].split("-")[1])
            sum_squares_deviation_mean = (float(ind_total_in_one_match) - av_total) ** 2
        else:
            ind_total_in_one_match = int(element[1].split("-")[0])
            sum_squares_deviation_mean = (float(ind_total_in_one_match) - av_total) ** 2

    variance = sum_squares_deviation_mean / len(all_statistics)

    return float(math.sqrt(variance))


def create_or_update_table_with_average_values(name_statistic):

    db.create_table_with_average_statistic(name_statistic)

    conn, cur = db.connect_db()
    set_all_teams = cur.execute("SELECT team_name FROM Таблица_всех_команд").fetchall()
    all_teams = [team[0] for team in set_all_teams]
    table_name_with_average_statistics = "Таблица_со_средними_показателями_" + name_statistic

    for team in all_teams:

        table_name = "Статистика_всех_матчей_" + team
        all_statistic = cur.execute(f"SELECT Матч, {name_statistic} FROM {table_name}").fetchall()

        av_ind_total = round(average_individual_total(team, all_statistic), 2)
        av_ind_total_opponent = round(average_individual_total_opponent(team, all_statistic), 2)
        av_total = round(average_total(team, all_statistic), 2)
        av_difference = round(average_difference(team, all_statistic), 2)
        total_deviation = round(mean_square_deviation_total(team, all_statistic), 2)
        ind_total_deviation = round(mean_square_deviation_individual_total(team, all_statistic), 2)
        ind_total_deviation_opponent = round(mean_square_deviation_individual_total_opponent(team, all_statistic), 2)
        count_win = quantity_win(team, all_statistic)
        count_lose = quantity_lose(team, all_statistic)
        count_draw = quantity_draw(team, all_statistic)

        date_for_db = (team, count_win, count_draw, count_lose, av_ind_total, av_ind_total_opponent, av_total,
                         av_difference, total_deviation, ind_total_deviation, ind_total_deviation_opponent)

        if cur.execute(f"""SELECT id FROM {table_name_with_average_statistics} WHERE Название_команды = ?""",
                       [team]).fetchone() == None:
            cur.execute(f"""INSERT OR IGNORE INTO {table_name_with_average_statistics}(Название_команды, Побед, Ничьих, Поражений,
            Ср_инд_тотал, Ср_инд_тотал_соп, Ср_Тотал, Ср_разница, Cр_квадр_откл_тотала, 
            Cр_квадр_откл_инд_тотала, Cр_квадр_откл_инд_тотала_соп) VALUES(?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?)""", date_for_db)
        else:
            cur.execute(f"""UPDATE {table_name_with_average_statistics} SET(Побед, Ничьих, Поражений,
            Ср_инд_тотал, Ср_инд_тотал_соп, Ср_Тотал, Ср_разница, Cр_квадр_откл_тотала,
            Cр_квадр_откл_инд_тотала, Cр_квадр_откл_инд_тотала_соп) = {date_for_db[1::]} WHERE Название_команды = ?""",
                        [team]
                        )
        conn.commit()


def create_or_update_all_stat_all_table():

    for el in ALL_NAME_STATISTICS:
        create_or_update_table_with_average_values(el)

create_or_update_all_stat_all_table()