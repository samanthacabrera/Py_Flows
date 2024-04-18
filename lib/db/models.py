# This file defines the structure and behavior of the database models. It contains classes that represent tables or collections in the database schema. 

import sqlite3
import random
import time
from colorama import init, Fore, Style
init()

DB_FILE = 'yoga.db'

class Pose:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty

    @classmethod
    def create(cls, name, difficulty):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO poses (name, difficulty) VALUES (?, ?)", (name, difficulty))
            conn.commit()

    @classmethod
    def delete(cls, pose_id):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM poses WHERE id = ?", (pose_id,))
            conn.commit()

    @classmethod
    def update(cls, pose_id, name=None, chakra=None, difficulty=None):
        update_query = "UPDATE poses SET "
        update_params = []

        if name is not None:
            update_query += "name = ?, "
            update_params.append(name)

        if chakra is not None:
            update_query += "chakra = ?, "
            update_params.append(chakra)
        
        if difficulty is not None:
            update_query += "difficulty = ?, "
            update_params.append(difficulty)

        # Remove the trailing comma and space
        update_query = update_query.rstrip(', ')

        update_query += " WHERE id = ?"
        update_params.append(pose_id)

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(update_query, tuple(update_params))
            conn.commit()

    @classmethod
    def get_all(cls):
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row  
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM poses")
            return cursor.fetchall()

    @classmethod
    def find_by_id(cls, pose_id):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM poses WHERE id = ?", (pose_id,))
            return cursor.fetchone()


class FlowPose:
    @classmethod
    def create(cls, flow_id, pose_id):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO flow_pose (flow_id, pose_id) VALUES (?, ?)", (flow_id, pose_id))
            conn.commit()

    @classmethod
    def delete(cls, flow_id, pose_id):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM flow_pose WHERE flow_id = ? AND pose_id = ?", (flow_id, pose_id))
            conn.commit()

    @classmethod
    def get_poses_for_flow(cls, flow_id):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT poses.* FROM poses JOIN flow_pose ON poses.id = flow_pose.pose_id WHERE flow_pose.flow_id = ?", (flow_id,))
            return cursor.fetchall()

    @classmethod
    def get_flows_for_pose(cls, pose_id):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT flows.* FROM flows JOIN flow_pose ON flows.id = flow_pose.flow_id WHERE flow_pose.pose_id = ?", (pose_id,))
            return cursor.fetchall()


class Flow:
    def __init__(self, chakra, duration, difficulty):
        self.chakra = chakra
        self.duration = duration
        self.difficulty = difficulty

    @classmethod
    def create(cls, chakra, duration, difficulty):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO flows (chakra, duration, difficulty) VALUES (?,?,?)",
                           (chakra, duration, difficulty))
            conn.commit()
    
    @classmethod
    def delete(cls, flow_id):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM flows WHERE id = ?", (flow_id,))
            conn.commit()
        
    @classmethod
    def get_all(cls):
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row  # Access columns by name
            cursor = conn.cursor()
            cursor.execute("SELECT id, chakra, duration, difficulty FROM flows")
            return cursor.fetchall()

    @classmethod
    def find_by_id(cls, flow_id):
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flows WHERE id = ?", (flow_id,))
            return cursor.fetchone()
    
    # Filter flow templates
    @classmethod
    def filter_by_chakra(cls, chakra):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flows WHERE chakra = ?", (chakra,))
            return cursor.fetchall()

    @classmethod
    def filter_by_duration(cls, duration):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flows WHERE duration = ?", (duration,))
            return cursor.fetchall()

    @classmethod
    def filter_by_difficulty(cls, difficulty):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flows WHERE difficulty = ?", (difficulty,))
            return cursor.fetchall()

    @classmethod
    def countdown_timer(cls, message, duration):
        for remaining in range(duration, 0, -1):
            print(f"{message}: {remaining}", end="\r")
            time.sleep(1)
        cls.clear_line()

    @classmethod
    def clear_line(cls):
        print("\033[K", end="\r")

    @classmethod
    def generate_flow_with_timers(cls, chakra, duration_minutes):
        # CHANGED FOR DEVELOPMENT
        duration_seconds = duration_minutes # * 60

        # Get all poses that match the specified chakra
        poses = Pose.get_all()
        matching_poses = [pose for pose in poses if pose[2] == chakra]

        if len(matching_poses) < 3:
            raise ValueError("There are not enough poses matching the chakra.")

        # Initial round of breath
        print("Inhale\n")     
        cls.countdown_timer("Remaining Time", 3)
        print("\nExhale\n")
        cls.countdown_timer("Remaining Time", 3)

        total_time = 0

        # Iterate over selected poses
        while total_time < duration_seconds:
            if not matching_poses:
                break  # If no poses left, exit loop
            selected_pose = random.choice(matching_poses)
            print(f"Pose: {selected_pose['name']}\n")
            matching_poses.remove(selected_pose)  # Remove selected pose
            cls.countdown_timer("Remaining Time", 3)
            total_time += 4  # Pose duration is 3 seconds plus 1 second pause
            time.sleep(1)  # Pause for 1 second between poses

        print("\nYou have completed your practice!!\n")
        time.sleep(1)
        print("Namaste\n")
        time.sleep(3)