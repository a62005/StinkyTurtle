# -*- coding: utf-8 -*-
"""YFPY demo.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import os
import glob
import sys
from logging import DEBUG
from pathlib import Path
import json
import ast

from datetime import datetime, time, timedelta

from dotenv import load_dotenv

project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

from yfpy import Data
from yfpy.logger import get_logger
from yfpy.query import YahooFantasySportsQuery

"""
Example public Yahoo league URL: "https://archive.fantasysports.yahoo.com/nfl/2014/729259"

Example vars using public Yahoo leagues still require auth through a personal Yahoo account: see README.md
"""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ENVIRONMENT SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# load .env file in order to read local environment variables
load_dotenv(dotenv_path=project_dir / "auth" / ".env")

# set directory location of private.json for authentication
auth_dir = project_dir / "auth"

# set target directory for data output
data_dir = Path(__file__).parent / "output"

# create YFPY Data instance for saving/loading data
data = Data(data_dir)

league_setting_current_dir = f"{os.getcwd()}/StinkyTurtle/config/"
league_setting_file_path = glob.glob(os.path.join(league_setting_current_dir, 'league_setting.txt'))[0]
league_setting_str = open(league_setting_file_path, 'r').read()
league_setting = ast.literal_eval(league_setting_str)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# VARIABLE SETUP  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# set desired season year
def get_season():
    # season = 2012
    # season = 2013
    # season = 2014
    # season = 2015
    # season = 2016
    # season = 2017
    # season = 2018
    # season = 2019
    # season = 2020
    # season = 2021
    # season = 2022
    # season = 2023
    return league_setting.get('year')


season = get_season()


# set desired week
def get_chosen_week():
    chosen_week = 6
    return chosen_week


chosen_week = get_chosen_week()


# set desired date
def get_chosen_date():
    # HOCKEY
    # chosen_date = "2013-04-15"  # NHL - 2013 (for 2012 season)
    chosen_date = "2021-10-25"  # NHL - 2021

    # BASEBALL
    # chosen_date = "2021-04-01"  # MLB - 2021
    # chosen_date = "2022-04-10"  # MLB - 2022

    return chosen_date


chosen_date = get_chosen_date()


# set desired Yahoo Fantasy Sports game code
def get_game_code():
    # FOOTBALL
    game_code = "nba"  # NFL

    # HOCKEY
    # game_code = "nhl"  # NHL

    # BASEBALL
    # game_code = "mlb"  # MLB

    return game_code


game_code = get_game_code()


# set desired Yahoo Fantasy Sports game ID (see the get_all_yahoo_fantasy_game_keys query to retrieve values)
def get_game_id():
    # FOOTBALL
    # game_id = 331  # NFL - 2014
    # game_id = 348  # NFL - 2015 (divisions)
    # game_id = 359  # NFL - 2016
    # game_id = 371  # NFL - 2017
    # game_id = 380  # NFL - 2018
    # game_id = 390  # NFL - 2019
    # game_id = 399  # NFL - 2020
    # game_id = 406  # NFL - 2021
    # game_id = 414  # NFL - 2022 (divisions)
    game_id = 428  # NFL - 2023

    # HOCKEY
    # game_id = 303  # NHL - 2012
    # game_id = 411  # NHL - 2021
    # game_id = 427  # NHL - 2023

    # BASEBALL
    # game_id = 404  # MLB - 2021
    # game_id = 412  # MLB - 2022

    return game_id


game_id = get_game_id()


# set desired Yahoo Fantasy Sports game key (see the get_all_yahoo_fantasy_game_keys query to retrieve values)
def get_game_key():
    # FOOTBALL
    # game_key = "331"  # NFL - 2014
    # game_key = "348"  # NFL - 2015 (divisions)
    # game_key = "359"  # NFL - 2016
    # game_key = "371"  # NFL - 2017
    # game_key = "380"  # NFL - 2018
    # game_key = "390"  # NFL - 2019
    # game_key = "399"  # NFL - 2020
    # game_key = "406"  # NFL - 2021
    # game_key = "414"  # NFL - 2022 (divisions)
    game_key = "428"  # NFL - 2023

    # HOCKEY
    # game_key = "303"  # NHL - 2012
    # game_key = "411"  # NHL - 2021
    # game_key = "427"  # NHL - 2023

    # BASEBALL
    # game_key = "404"  # MLB - 2021
    # game_key = "412"  # MLB - 2022

    return game_key


game_key = get_game_key()


# set desired league ID (see README.md for finding value)
def get_league_id():
    # FOOTBALL
    # league_id = "907359"  # NFL - 2015 (divisions)
    # league_id = "79230"  # NFL - 2019
    # league_id = "655434"  # NFL - 2020
    # league_id = "413954"  # NFL - 2021
    # league_id = "791337"  # NFL - 2022 (divisions)
    # league_id = "186918"  # NFL - 2023

    # HOCKEY
    # league_id = "69624"  # NHL - 2012
    # league_id = "101592"  # NHL - 2021
    # league_id = "6546"  # NHL - 2021 (draft pick trading)
    # league_id = "22827"  # NHL - 2023
    # league_id = "1031"  # NHL - 2023 (FAAB)

    # BASEBALL
    # league_id = "40134"  # MLB - 2021

    return league_setting.get('league_id')


league_id = get_league_id()


# set desired team ID within desired league
def get_team_id():
    # FOOTBALL
    team_id = 1  # NFL

    # HOCKEY
    # team_id = 2  # NHL (2012)

    return team_id


team_id = get_team_id()


# set desired team name within desired league
def get_team_name():
    # FOOTBALL
    team_name = "Legion"  # NFL

    # HOCKEY
    # team_name = "The Bateleurs"  # NHL (2012)

    return team_name


team_name = get_team_name()


# set desired team ID within desired league
def get_player_id():
    # FOOTBALL
    player_id = 30123  # NFL: Patrick Mahomes - 2020/2021/2023

    # HOCKEY
    # player_id = 4588  # NHL: Braden Holtby - 2012
    # player_id = 8205  # NHL: Jeffrey Viel - 2021
    # player_id = 3637  # NHL: Alex Ovechkin - 2021

    # BASEBALL
    # player_id = 9897  # MLB: Tim Anderson - 2021/2022

    return player_id


player_id = get_player_id()


# set the maximum number players you wish the get_league_players query to retrieve
def get_league_player_limit():
    league_player_limit = 101

    return league_player_limit


league_player_limit = get_league_player_limit()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# QUERY SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# configure the Yahoo Fantasy Sports query (change all_output_as_json_str=True if you want to output JSON strings)
yahoo_query = YahooFantasySportsQuery(
    auth_dir,
    league_id,
    game_code,
    game_id=game_id,
    offline=False,
    all_output_as_json_str=False
)

# Manually override league key for example code to work
yahoo_query.league_key = f"{game_id}.l.{league_id}"

def parse_stat_id(id):
  return {
      '9004003': 'FGM/A',
      '5': 'FG%',
      '9007006': 'FTM/A',
      '8': 'FT%',
      '10': '3PTM',
      '12': 'PTS',
      '15': 'REB',
      '16': 'AST',
      '17': 'ST',
      '18': 'BLK',
      '19': 'TO'
  }.get(id, "default") 
    

def check_time():
    current_time = datetime.now().time()
    start_time = time(14, 0)  # 14:00
    end_time = time(4, 0)  # 04:00

    if start_time < end_time:
        if start_time <= current_time <= end_time:
            return False
    else:  # crosses midnight
        if start_time <= current_time or current_time <= end_time:
            return False

    return True

def get_person_data(team_id):
    if (check_time() or not os.path.isfile(f'{team_id}.txt')):
        data = yahoo_query.get_team_week_data(team_id, chosen_week)
        with open(f'{team_id}.txt', 'w') as f:
            f.write(json.dumps(data, ensure_ascii=False))
        return data
    else:
        with open(f'{team_id}.txt', 'r') as f:
            data = f.read()
        return data
    
def get_data_by_stat_id(hit):
    stat = parse_stat_id(hit)
    if (check_time() or not os.path.isfile(f'{stat}.txt')):
        data = yahoo_query.get_team_data_by_stat_id(hit, chosen_week)
        data['teams'] = sorted(data['teams'], key=lambda x: int(list(x.values())[0]), reverse=True)
        with open(f'{stat}.txt', 'w') as f:
            f.write(json.dumps(data, ensure_ascii=False))
        return data
    else:
        with open(f'{stat}.txt', 'r') as f:
            data = f.read()
        return data
    
def remove_yesterday_played_txt(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    # 計算前一天的日期
    previous_date = date - timedelta(days=1)

    # 將日期轉換回字串
    previous_date_str = previous_date.strftime('%Y-%m-%d')

    # 檔案的路徑
    file_path = f"today_player_{previous_date_str}.txt"
    # 檢查檔案是否存在
    if os.path.isfile(file_path):
    # 如果檔案存在，則刪除它
        os.remove(file_path)

def remove_last_week_played_txt(week):
    # 檔案的路徑
    file_path = f"played_for_{week - 1}_week.txt"
    # 檢查檔案是否存在
    if os.path.isfile(file_path):
    # 如果檔案存在，則刪除它
        os.remove(file_path)
    

def get_all_data(week, date):
    data = yahoo_query.get_all_data(week, True)
    now = datetime.now()
    games_palyed_txt_name = f"played_for_{week}_week.txt"
    today_played_txt_name = f"today_player_{date}.txt"
    print(f"data {data}")
    if now.hour >= 14 and now.hour < 24:
        result = {'Games Played': {}}
        if os.path.isfile(games_palyed_txt_name):
            if not os.path.isfile(today_played_txt_name):
                with open(games_palyed_txt_name, 'r', encoding='utf-8') as f:
                    tmp = json.load(f)
                    yesterday_played = tmp['Games Played']
                today_played = data['Games Played']
                temp = {'Games Played': today_played}
                for key in today_played.keys():
                # 取出兩個字典中的值
                    value_yesterday = yesterday_played[key]
                    value_today = today_played[key]

                    # 分割值並取出分母
                    denominator_yesterday = int(value_yesterday.split('/')[0])
                    denominator_today = int(value_today.split('/')[0])

                # 計算分母的差並儲存結果
                    result['Games Played'][key] = denominator_today - denominator_yesterday
                with open(today_played_txt_name, 'w', encoding='utf-8') as w:
                    w.write(json.dumps(result, ensure_ascii=False))
                with open(games_palyed_txt_name, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(temp, ensure_ascii=False))    
        else:
            today_played = data['Games Played']
            with open(games_palyed_txt_name, 'w') as f:
                temp = {'Games Played': today_played}
                f.write(json.dumps(temp, ensure_ascii=False))
            for key in today_played.keys():
                # 取出字典中的值
                value = today_played[key]

                # 分割值並取出分子
                numerator = int(value.split('/')[0])

                # 儲存結果
                result['Games Played'][key] = numerator
            with open(today_played_txt_name, 'w', encoding='utf-8') as w:
                w.write(json.dumps(result, ensure_ascii=False))
            remove_last_week_played_txt(week)
        remove_yesterday_played_txt(date)
    return data

def get_today_all_data(date, week):
    data = yahoo_query.get_all_data(date, False)
    txt_str =f"today_player_{date}.txt"
    if os.path.isfile(txt_str):
        with open(txt_str, 'r', encoding='utf-8') as f:
            today_played = json.load(f)['Games Played']
            data['Today Played'] = dict(sorted(today_played.items(), key=lambda item: int(item[1]), reverse=True))
    return data

#{
    #"week": 2,
    #"date": "2021-10-25",
#     "Today Played": {
#        ...
#      }
#}


    


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# RUN QUERIES # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# print(repr(yahoo_query.get_all_yahoo_fantasy_game_keys()))
# print(repr(yahoo_query.get_game_key_by_season(season)))
# print(repr(yahoo_query.get_current_game_info()))
# print(repr(yahoo_query.get_current_game_metadata()))
# print(repr(yahoo_query.get_game_info_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_metadata_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_weeks_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_stat_categories_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_position_types_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_roster_positions_by_game_id(game_id)))
# print(repr(yahoo_query.get_league_key(season)))
# print(repr(yahoo_query.get_current_user()))
# print(repr(yahoo_query.get_user_games()))
# print(repr(yahoo_query.get_user_leagues_by_game_key(game_key)))
# print(repr(yahoo_query.get_user_teams()))
# print(repr(yahoo_query.get_league_info()))
# print(repr(yahoo_query.get_league_metadata()))
# print(repr(yahoo_query.get_league_settings()))
# print(repr(yahoo_query.get_league_standings()))
# print(repr(yahoo_query.get_league_teams()))
# print(repr(yahoo_query.get_league_players(player_count_limit=10, player_count_start=0)))
# print(repr(yahoo_query.get_league_draft_results()))
# print(repr(yahoo_query.get_league_transactions()))
# print(repr(yahoo_query.get_league_scoreboard_by_week(chosen_week)))
# print(repr(yahoo_query.get_league_matchups_by_week(chosen_week)))
# print(repr(yahoo_query.get_team_info(team_id)))
# print(repr(yahoo_query.get_team_metadata(team_id)))
# print(repr(yahoo_query.get_team_stats(team_id)))
# print(repr(yahoo_query.get_team_stats_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_standings(team_id)))
# print(repr(yahoo_query.get_team_roster_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_roster_player_info_by_week(team_id, chosen_week)))
# # print(repr(yahoo_query.get_team_roster_player_info_by_date(team_id, chosen_date)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_team_roster_player_stats(team_id)))
# print(repr(yahoo_query.get_team_roster_player_stats_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_draft_results(team_id)))
# print(repr(yahoo_query.get_team_matchups(team_id)))
# print(repr(yahoo_query.get_player_stats_for_season(player_key)))
# print(repr(yahoo_query.get_player_stats_for_season(player_key, limit_to_league_stats=False)))
# print(repr(yahoo_query.get_player_stats_by_week(player_key, chosen_week)))
# print(repr(yahoo_query.get_player_stats_by_week(player_key, chosen_week, limit_to_league_stats=False)))
# print(repr(yahoo_query.get_player_stats_by_date(player_key, chosen_date)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_player_stats_by_date(player_key, chosen_date, limit_to_league_stats=False)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_player_ownership(player_key)))
# print(repr(yahoo_query.get_player_percent_owned_by_week(player_key, chosen_week)))
# print(repr(yahoo_query.get_player_draft_analysis(player_key)))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CHECK FOR MISSING DATA FIELDS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

logger = get_logger("yfpy.models", DEBUG)

# yahoo_query.get_all_yahoo_fantasy_game_keys()
# yahoo_query.get_game_key_by_season(season)
# yahoo_query.get_current_game_info()
# yahoo_query.get_current_game_metadata()
# yahoo_query.get_game_info_by_game_id(game_id)
# yahoo_query.get_game_metadata_by_game_id(game_id)
# yahoo_query.get_game_weeks_by_game_id(game_id)
# yahoo_query.get_game_stat_categories_by_game_id(game_id)
# yahoo_query.get_game_position_types_by_game_id(game_id)
# yahoo_query.get_game_roster_positions_by_game_id(game_id)
# yahoo_query.get_league_key(season)
# yahoo_query.get_current_user()
# yahoo_query.get_user_games()
# yahoo_query.get_user_leagues_by_game_key(game_key)
# yahoo_query.get_user_teams()
# yahoo_query.get_league_info()
# yahoo_query.get_league_metadata()
# yahoo_query.get_league_settings()
# yahoo_query.get_league_standings()
# yahoo_query.get_league_teams()
# yahoo_query.get_league_players(player_count_limit=10, player_count_start=0)
# yahoo_query.get_league_draft_results()
# yahoo_query.get_league_transactions()
# yahoo_query.get_league_scoreboard_by_week(chosen_week)
# yahoo_query.get_league_matchups_by_week(chosen_week)
# yahoo_query.get_team_info(team_id)
# yahoo_query.get_team_metadata(team_id)
# yahoo_query.get_team_stats(team_id)
# yahoo_query.get_team_stats_by_week(team_id, chosen_week)
# yahoo_query.get_team_standings(team_id)
# yahoo_query.get_team_roster_by_week(team_id, chosen_week)
# yahoo_query.get_team_roster_player_info_by_week(team_id, chosen_week)
# yahoo_query.get_team_roster_player_info_by_date(team_id, chosen_date)  # NHL/MLB/NBA
# yahoo_query.get_team_roster_player_stats(team_id)
# yahoo_query.get_team_roster_player_stats_by_week(team_id, chosen_week)
# yahoo_query.get_team_draft_results(team_id)
# yahoo_query.get_team_matchups(team_id)
# yahoo_query.get_player_stats_for_season(player_key))
# yahoo_query.get_player_stats_for_season(player_key, limit_to_league_stats=False))
# yahoo_query.get_player_stats_by_week(player_key, chosen_week)
# yahoo_query.get_player_stats_by_week(player_key, chosen_week, limit_to_league_stats=False)
# yahoo_query.get_player_stats_by_date(player_key, chosen_date,)  # NHL/MLB/NBA
# yahoo_query.get_player_stats_by_date(player_key, chosen_date, limit_to_league_stats=False)  # NHL/MLB/NBA
# yahoo_query.get_player_ownership(player_key)
# yahoo_query.get_player_percent_owned_by_week(player_key, chosen_week)
# yahoo_query.get_player_draft_analysis(player_key)
