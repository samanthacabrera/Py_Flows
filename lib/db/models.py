# This file defines the structure and behavior of the database models. It contains classes that represent tables or collections in the database schema. 

import sqlite3
import random
import time

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
    def find_by_id(cls, flow_id):
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flows WHERE id = ?", (flow_id,))
            return cursor.fetchone()

        
    @classmethod
    def get_all(cls):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flows")
            return cursor.fetchall()

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

        total_time = 0
        for pose_index, pose in enumerate(selected_poses, start=1):
            print(f"Starting pose {pose_index}: {pose[1]}")

            total_time += 10  # Pose duration is 10 seconds

            # Show countdown timer for each pose
            for countdown in range(10, 0, -1):
                print(f"Pose {pose_index} time remaining: {countdown} seconds ", end="\r")
                time.sleep(1)
            print("\n")

        # Add rounds of breaths
        breath_rounds = total_time // 30  
        for i in range(breath_rounds):
            print(f"Round {i+1} of breath: Inhale")
            time.sleep(5)
            print(f"Round {i+1} of breath: Exhale")
            time.sleep(5)

        # End every flow with Savasana
        print("Savasana: A time to honor our bodies, minds, and spirits with well-deserved rest.")
        time.sleep(1)
        print("You have completed your practice!!")
        time.sleep(1)
        print("Namaste")

    @classmethod
    def search_flows_menu(cls):
        print("Select a flow:")
        print("ID | Chakra | Duration | Difficulty")
        flows = cls.get_all()
        for flow in flows:
            print(f"{flow['id']} | {flow['chakra']} | {flow['duration']} minutes | {flow['difficulty']}")
        flow_id = input("Enter the ID of the flow you want to generate: ")
        if flow_id.lower() == "take me home":
            return
        cls.generate_selected_flow(flow_id)

    @classmethod
    def generate_selected_flow(cls, flow_id):
        flow = cls.find_by_id(flow_id)
        if flow:
            print("Generating your own unique yoga flow...")
            cls.generate_flow_with_timers(flow['chakra'], flow['duration'])
        else:
            print("Flow not found.")
