from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager

import db_KHL as db
from main import ALL_STATISTICS, ALL_TEAM
import create_table_with_average_values as update_table_averange


def update_collect_penalty_time():
    global driver

    time.sleep(2)

    penalty_time_home_team = 0
    penalty_time_away_team = 0

    event_home_team = driver.find_elements(By.CSS_SELECTOR, ".smv__participantRow.smv__homeParticipant")
    event_away_team = driver.find_elements(By.CSS_SELECTOR, ".smv__participantRow.smv__awayParticipant")

    for event_in_match in event_home_team:
        penalty_times = event_in_match.find_elements(By.CLASS_NAME, "penalty-2-min ")
        for penalty_time_in_match in penalty_times:
            penalty_time_home_team += 1

    for event_in_match in event_away_team:
        penalty_times = event_in_match.find_elements(By.CLASS_NAME, "penalty-2-min ")
        for penalty_time_in_match in penalty_times:
            penalty_time_away_team += 1

    return [penalty_time_home_team, "Кол-во 2-х минутных удалений", penalty_time_away_team]


def update_collect_statistics(team_name):
    global driver

    name_table = "Статистика_всех_матчей_" + str(team_name).replace(" ", "_")
    flag = True
    match_statistics = []
    driver.execute_script("window.scrollTo(0, 300)")
    match_time = driver.find_element(By.CLASS_NAME, "duelParticipant__startTime").text.split()[0]

    conn, cur = db.connect_db()
    if cur.execute(f"SELECT Дата FROM {name_table} WHERE Дата = ?", [match_time]).fetchone() != None:
        flag = False

    match_score = driver.find_element(By.CLASS_NAME, "detailScore__wrapper").text.splitlines()
    match_score = "".join(match_score)

    penalty_time = update_collect_penalty_time()

    driver.find_element(By.CSS_SELECTOR, "#detail > div.tabs.tabs__detail > div > a:nth-child(2)").click()
    time.sleep(5)
    # odds_selector = []
    # odd_selector = driver.find_element(By.XPATH, '//*[@id="detail"]/div[8]/div[3]/div/div[2]/div/a[1]')
    # odds_selector.append(odd_selector)
    # odds_selector.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[8]/div[3]/div/div[2]/div/a[2]'))
    # odds_selector.append(odd_selector)
    # odds_selector.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[8]/div[3]/div/div[2]/div/a[3]'))
    # odds_selector.append(odd_selector)
    odds_selector = driver.find_elements(By.CSS_SELECTOR, ".oddsCell__odd.oddsCell__highlight ")
    #                                                       ".oddsCell__odd.oddsCell__highlight "
    collect_odds = odds_selector[0].text + " " + odds_selector[1].text + " " + odds_selector[2].text

    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#detail > div.tabs.tabs__detail > div > a:nth-child(1)").click()
    driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
    driver.find_element(By.CSS_SELECTOR, "#detail > div.tabs.tabs__detail--nav > div > a:nth-child(2)").click()
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 200)")

    driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
    all_statistics = driver.find_elements(By.CLASS_NAME, "stat__row")
    for el in all_statistics:
        if el.text.splitlines()[1] in ALL_STATISTICS:
            match_statistics.append(el.text.splitlines())

    draw_in_main = driver.find_element(By.CLASS_NAME, "fixedHeaderDuel__detailStatus").text

    if draw_in_main == "ПОСЛЕ ОВЕРТАЙМА" or draw_in_main == "ПОСЛЕ БУЛЛИТОВ":
        driver.find_elements(By.CSS_SELECTOR, ".subTabs__tab")[-1].click()

        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        all_statistics_overtime = driver.find_elements(By.CLASS_NAME, "stat__row")
        lst_all_statistics_overtime = []

        for i in range(len(all_statistics_overtime)):
            if all_statistics_overtime[i].text.splitlines()[1] in ALL_STATISTICS:
                lst_all_statistics_overtime.append(all_statistics_overtime[i].text.splitlines())

        for i in range(0, len(match_statistics)):
            match_statistics[i][0] = str(int(match_statistics[i][0]) - int(lst_all_statistics_overtime[i][0]))
            match_statistics[i][2] = str(int(match_statistics[i][2]) - int(lst_all_statistics_overtime[i][2]))

    match_statistics.append(penalty_time)

    return match_time, match_score, collect_odds, match_statistics, flag


def update_team_research(counter_matches):
    global driver

    team_name = driver.find_element(By.CLASS_NAME, "heading__name").text

    driver.find_element(By.CSS_SELECTOR, "#li2").click()
    window_with_matches = driver.window_handles[len(driver.window_handles) - 1]
    driver.execute_script("window.scrollTo(0, 300)")

    all_matches = driver.find_elements(By.CSS_SELECTOR, ".event__match.event__match--static.event__match--twoLine")[
                  0:int(counter_matches)]
    statistics_matches_for_one_team = []
    for i in range(len(all_matches)):
        separate_team_match = []
        lst = all_matches[i].text.splitlines()

        team_match = []
        for l in lst:
            if l in ALL_TEAM:
                team_match.append(l)
        string_match = team_match[0] + '-' + team_match[1]
        separate_team_match.append(string_match)

        all_matches[i].click()
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        temp = update_collect_statistics(team_name)

        flag = temp[4]
        if flag == False:
            driver.close()
            driver.switch_to.window(window_with_matches)
            break

        separate_team_match.append(temp[0])
        separate_team_match.append(temp[1])
        separate_team_match.append(temp[2])
        separate_team_match.append(temp[3])
        statistics_matches_for_one_team.append(separate_team_match)
        driver.close()
        driver.switch_to.window(window_with_matches)

        db.add_stat_match_in_table_matches_team(statistics_matches_for_one_team[-1], team_name)


def update():
    global driver
    #url_KHL = "https://www.flashscore.com.ua/khl/standings/"
    url = "https://www.flashscore.com.ua/khl/standings/#/jF3yFJXm/table/overall"
    driver = webdriver.Chrome(ChromeDriverManager().install())

    #driver = webdriver.Chrome(executable_path="C:\\Users\\mi\\PycharmProjects\\parsingKHL\\chromedriver\\chromedriver.exe")

    driver.get(url=url)
    time.sleep(10)
    driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()
    time.sleep(5)
    elements = driver.find_elements(By.CLASS_NAME, "ui-table__row")
    elements = elements[0:22]
    driver.execute_script("window.scrollTo(0, 500)")
    time.sleep(5)
    main_window = driver.window_handles[0]

    for i in range(len(elements)):
        if i == 10:
            driver.execute_script("window.scrollTo(0, 950)")

        counter_matches = elements[i].text.splitlines()[2]
        elements[i].find_elements(By.CLASS_NAME, "tableCellParticipant__image")[0].click()
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])

        update_team_research(counter_matches)

        driver.close()
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])

    time.sleep(5)
    driver.close()
    driver.quit()


update()
update_table_averange.create_or_update_all_stat_all_table()