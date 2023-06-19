import sqlite3

ALL_ID_TEAMS = {}


def connect_db():
    conn = sqlite3.connect("all_stat_KHL.db")
    cur = conn.cursor()
    return conn, cur


def add_stat_match_in_table_matches_team(stat_match, team):

    conn, cur = connect_db()

    team = str(team).replace(" ", "_")
    name_table = "Статистика_всех_матчей_" + str(team).replace(" ", "_")
    match = str(stat_match[0])
    date = str(stat_match[1])
    score = str(stat_match[2])
    odds = str(stat_match[3])
    shots_on_goals = str(stat_match[4][0][0]) + '-' + str(stat_match[4][0][2])
    power_play_goal = str(stat_match[4][1][0]) + '-' + str(stat_match[4][1][2])
    faceoffs_on = str(stat_match[4][2][0]) + '-' + str(stat_match[4][2][2])
    count_penalty_2_minutes_time = str(stat_match[4][3][0]) + '-' + str(stat_match[4][3][2])


    set_id_team = cur.execute("SELECT id FROM Таблица_всех_команд WHERE team_name = ?", [team]).fetchone()
    id_team = int(set_id_team[0])

    all_stat = (date, match, score, odds, shots_on_goals, power_play_goal, faceoffs_on, count_penalty_2_minutes_time,
                id_team)

    if cur.execute(f"SELECT Дата FROM {name_table} WHERE Дата = ?", [date]).fetchone() == None:
        cur.execute(f"""INSERT INTO {name_table}(Дата, Матч, Счет, Коэффициенты, Броски_в_створ, Голы_в_большинстве,
        Выигранные_вбрасывания, Количество_двухминутных_удалений, team_id)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", all_stat)
        conn.commit()


def create_table_all_matches_team(team):

    conn, cur = connect_db()
    name_table = "Статистика_всех_матчей_" + str(team).replace(" ", "_")
    table_for_team_sql = """
    CREATE TABLE IF NOT EXISTS {table}(
    id INTEGER PRIMARY KEY,
    Дата TEXT,
    Матч TEXT,
    Счет TEXT,
    Коэффициенты TEXT,
    Броски_в_створ TEXT,
    Голы_в_большинстве TEXT,
    Выигранные_вбрасывания TEXT,
    Количество_двухминутных_удалений TEXT,
    team_id INTEGER NOT_NULL,
    FOREIGN KEY(team_id) REFERENCES teams(id)
    )
    """
    cur.execute(table_for_team_sql.format(table=name_table))
    conn.commit()


def add_team_in_table_teams(team):

    conn, cur = connect_db()
    team = team.replace(" ", "_")
    if cur.execute("SELECT team_name FROM Таблица_всех_команд WHERE team_name = ?", [team]).fetchone() == None:
        cur.execute("INSERT INTO Таблица_всех_команд(team_name) VALUES (?)", (team, ))
        conn.commit()


def create_table_teams():

    table_name = "Таблица_всех_команд"
    conn, cur = connect_db()
    teams_sql = """
    CREATE TABLE IF NOT EXISTS {table}(
        id INTEGER PRIMARY KEY,
        team_name TEXT UNIQUE
    )
    """
    cur.execute(teams_sql.format(table=table_name))
    conn.commit()


def create_table_with_average_statistic(name_statistic):

    table_name = "Таблица_со_средними_показателями_" + name_statistic
    conn, cur = connect_db()
    table_sql = """
    CREATE TABLE IF NOT EXISTS {table}(
        id INTEGER PRIMARY KEY,
        Название_команды TEXT,
        Побед INTEGER,
        Ничьих INTEGER,
        Поражений INTEGER,
        Ср_инд_тотал REAL,
        Ср_инд_тотал_соп REAL,
        Ср_Тотал Real,
        Ср_разница REAL,
        Cр_квадр_откл_тотала REAL,
        Cр_квадр_откл_инд_тотала REAL,
        Cр_квадр_откл_инд_тотала_соп REAL
    )
    """
    cur.execute(table_sql.format(table=table_name))
    conn.commit()

