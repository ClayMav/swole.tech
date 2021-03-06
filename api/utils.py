"""All of the util functions"""
from datetime import datetime

from playhouse.shortcuts import model_to_dict

from models import (Buddies, LiveWorkouts, Post, Posted, Team, TeamMembers,
                    User, Workout)


def get_workout(workout_id):
    return Workout.get(Workout.id == workout_id)


def post_workout(workout_values):
    try:
        workout = Workout.create(
            name=workout_values['name'],
            creator=workout_values['creator'],
            category=workout_values['category'],
            exercises=workout_values['exercises'])
        LiveWorkouts.create(user=workout_values['creator'], workout=workout)
        return model_to_dict(workout)
    except Exception as e:
        print("ERROR", str(e))
        return e


def update_workout(id):
    try:
        workout = Workout.update({
            'end_time': datetime.now()
        }).where(Workout.id == id)
        workout.execute()
        return Workout.get(Workout.id == id)
    except Exception as e:
        print("HUGE", str(e))
        return str(e)


def list_posts(username):
    posts = []
    buddies = [
        str(buddy.my_friend)
        for buddy in Buddies.select().where(Buddies.myself == username)
    ]
    buddies.append(username)
    for buddy in buddies:
        for post in Posted.select().where(Posted.user == buddy):
            post = model_to_dict(post.post)
            post["name"] = buddy
            posts.append(post)
    print(posts)
    return posts


def list_live(username):
    lives = []
    buddies = [
        str(buddy.my_friend)
        for buddy in Buddies.select().where(Buddies.myself == username)
    ]
    buddies.append(username)
    # print(buddies)
    for buddy in buddies:
        lives += [
            model_to_dict(workout.workout)
            for workout in LiveWorkouts.select().where(
                LiveWorkouts.user == buddy)
        ]
    return lives


def get_user_info(user_name):
    user = model_to_dict(User.get(User.name == user_name))
    user["buddies"] = [
        model_to_dict(buddy.my_friend)
        for buddy in Buddies.select().where(Buddies.myself == user["name"])
    ]
    user["posts"] = []

    for post in Posted.select().where(Posted.user == user["name"]):
        post = model_to_dict(post.post)
        post["name"] = user["name"]
        user["posts"].append(post)

    return user


def list_friends(username):
    buddies = [
        model_to_dict(buddy.my_friend)
        for buddy in Buddies.select().where(Buddies.myself == username)
    ]
    return buddies


def add_friend(username, data):
    other_guy = data["friend"]
    buddy = Buddies.create(myself=username, my_friend=other_guy)
    Buddies.create(myself=other_guy, my_friend=username)
    return model_to_dict(buddy)


def list_all_teams():
    return [model_to_dict(team) for team in TeamMembers.select().execute()]


def list_all_user_teams(member_name):
    user = User.select().where(User.name == member_name).execute()
    try:
        teams_and_managers = []
        teams = TeamMembers.select().where(
            TeamMembers.member == user[0].name).execute()
        for team in teams:
            manager = TeamMembers.select().where((TeamMembers.is_manager) &
                                                 (TeamMembers.team == team.team))
            teams_and_managers.append(str(team.team))
        return teams_and_managers
    except IndexError:
        return {}


def create_team(team_values):
    try:
        Team.create(name=team_values['name'])
        return {"name": team_values['name']}
    except Exception as e:
        return e


def add_user_to_team(request_values):
    try:
        TeamMembers.create(
            member=request_values['member'],
            team=request_values['team'],
            is_manager=request_values['is_manager'])
        return {
            request_values['team']:
            request_values['member'] - request_values['is_manager']
        }
    except Exception as e:
        return e


def list_users():
    return [model_to_dict(user) for user in User.select()]


def post_post(username, po):
    new_post = Post.create(
        photo=po["photo"],
        caption=po["caption"],
        original_workout=po["original_workout"])
    Posted.create(user=username, post=new_post)
    return model_to_dict(new_post)
