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
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flows")
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

    # Generate unique flow
    @classmethod
    def generate_flow_with_timers(cls, chakra, duration_minutes):
        # Convert duration from minutes to seconds
        duration_seconds = duration_minutes * 60

        # Get poses that match the specified chakra
        poses = Pose.get_all()
        matching_poses = [pose for pose in poses if pose[2] == chakra]

        if len(matching_poses) < 3:
            raise ValueError("There are not enough poses matching the chakra")

        # Randomly select poses for the flow
        selected_poses = random.sample(matching_poses, 3)

        # Initial 2 rounds of breath
        print("Starting your yoga flow...\n")
        for round_num in range(1, 3):
            print(f"Round {round_num} of breath: Inhale")
            time.sleep(1)
            print("\n")
            time.sleep(1)
            print(f"Round {round_num} of breath: Exhale")
            time.sleep(1)
            print("\n")
            time.sleep(1)
        
        total_time = 0
        
        # Iterate over selected poses
        for pose_index, pose in enumerate(selected_poses, start=1):
            print(f"Pose {pose_index}: {pose[1]}")
            total_time += 10  # Pose duration is 10 seconds
            time.sleep(1)
            print("\n")

        # Add rounds of breaths
        breath_rounds = total_time // 30
        for i in range(breath_rounds):
            print(f"Round {i+1} of breath: Inhale")
            time.sleep(1)
            print("\n")
            time.sleep(1)
            print(f"Round {i+1} of breath: Exhale")
            time.sleep(1)
            print("\n")
            time.sleep(1)

        # End every flow with Savasana
        print("Savasana: A time to honor our bodies, minds, and spirits with well-deserved rest.\n")
        time.sleep(2)
        print("You have completed your practice!!\n")
        time.sleep(2)
        print("Namaste\n")



    @classmethod
    def generate_selected_flow(cls, flow_id):
        flow = cls.find_by_id(flow_id)
        if flow:
            print("\n\nGenerating your own unique yoga flow...\n\n")            
            cls.generate_flow_with_timers(flow['chakra'], flow['duration'])
        else:
            print("Flow not found.")
