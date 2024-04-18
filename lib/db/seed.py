# This file is used for populating the database with initial data.
# It contains scripts or functions that insert predefined data into the database tables.

import sqlite3
import random

DB_FILE = 'yoga.db'

def drop_tables():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS flows")
        cursor.execute("DROP TABLE IF EXISTS poses")
        cursor.execute("DROP TABLE IF EXISTS flow_poses")
        conn.commit()

def create_tables():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS flows (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            chakra TEXT NOT NULL,
                            duration INTEGER NOT NULL,
                            difficulty TEXT NOT NULL
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS poses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            chakra TEXT NOT NULL,
                            difficulty TEXT NOT NULL
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS flow_poses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            flow_id INTEGER,
                            pose_id INTEGER,
                            FOREIGN KEY(flow_id) REFERENCES flows(id),
                            FOREIGN KEY(pose_id) REFERENCES poses(id)
                        )''')
        conn.commit()

def insert_yoga_poses():
    yoga_poses = [
    ("Conquer Breath", "Root", "Easy"),
    ("Easy Pose", "Sacral", "Easy"),
    ("Staff Pose", "Solar Plexus", "Easy"),
    ("Cat Pose", "Heart", "Easy"),
    ("Sphinx Pose", "Throat", "Intermediate"),
    ("Warrior 1 Pose", "Third Eye", "Intermediate"),
    ("Gate Pose", "Crown", "Intermediate"),
    ("Extended Side Angle Pose", "Root", "Intermediate"),
    ("Wide Legged Forward Bend", "Sacral", "Intermediate"),
    ("Wide-Angle Seated Forward Bend", "Solar Plexus", "Intermediate"),
    ("Reclining Bound Angle Pose", "Heart", "Intermediate"),
    ("Hero Pose", "Throat", "Intermediate"),
    ("Chair Pose", "Third Eye", "Intermediate"),
    ("Mountain Pose", "Crown", "Easy"),
    ("Bharadvaja's Twist", "Root", "Intermediate"),
    ("Salutation Seal", "Sacral", "Easy"),
    ("Corpse Pose", "Solar Plexus", "Easy"),
    ("Standing Forward Bend", "Heart", "Intermediate"),
    ("Seated Forward Bend", "Throat", "Intermediate"),
    ("Childs Pose", "Third Eye", "Easy"),
    ("Cobra Pose", "Crown", "Intermediate"),
    ("Plank Pose", "Root", "Intermediate"),
    ("Happy Baby Pose", "Sacral", "Easy"),
    ("Low Lunge", "Solar Plexus", "Intermediate"),
    ("High Lunge", "Heart", "Intermediate"),
    ("Standing Half Forward Bend", "Throat", "Intermediate"),
    ("Root Bond", "Third Eye", "Intermediate"),
    ("Garland Pose", "Crown", "Intermediate"),
    ("Extended Puppy Pose", "Root", "Intermediate"),
    ("Lion Pose", "Sacral", "Intermediate"),
    ("Intense Side Stretch", "Solar Plexus", "Intermediate"),
    ("Locust Pose", "Heart", "Intermediate"),
    ("Heron Pose", "Throat", "Intermediate"),
    ("Fish Pose", "Third Eye", "Intermediate"),
    ("Legs-Up-The-Wall Pose", "Crown", "Easy"),
    ("Cow Face Pose", "Root", "Intermediate"),
    ("Warrior II Pose", "Sacral", "Intermediate"),
    ("Tree Pose", "Solar Plexus", "Intermediate"),
    ("Downward Facing Dog", "Heart", "Intermediate"),
    ("Half Lord of the Fishes Pose", "Throat", "Intermediate"),
    ("Bridge Pose", "Third Eye", "Intermediate"),
    ("Four Limbed Staff", "Crown", "Intermediate"),
    ("Standing Forward Bend", "Root", "Intermediate"),
    ("Pigeon Pose Head Down", "Sacral", "Intermediate"),
    ("Lotus Pose", "Solar Plexus", "Advanced"),
    ("Warrior III", "Heart", "Intermediate"),
    ("Cow Pose", "Throat", "Easy"),
    ("Upward Facing Dog", "Third Eye", "Intermediate"),
    ("Shoulder Stand", "Crown", "Intermediate"),
    ("Butterfly Pose", "Root", "Easy")
]

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO poses (name, chakra, difficulty) VALUES (?, ?, ?)", yoga_poses)
        conn.commit()

def insert_yoga_flows():
    yoga_flows = [
        ("Root", 30, "Easy"),
        ("Sacral", 20, "Easy"),
        ("Solar Plexus", 40, "Easy"),
        ("Heart", 30, "Easy"),
        ("Throat", 20, "Easy"),
        ("Third Eye", 40, "Intermediate"),
        ("Crown", 30, "Intermediate")
    ]

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO flows (chakra, duration, difficulty) VALUES (?, ?, ?)", yoga_flows)
        conn.commit()

def insert_flow_poses():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        
        # Retrieve the IDs of all flows
        cursor.execute("SELECT id FROM flows")
        flow_ids = [row[0] for row in cursor.fetchall()]
        
        # Retrieve the IDs of all poses
        cursor.execute("SELECT id FROM poses")
        pose_ids = [row[0] for row in cursor.fetchall()]
        
        # Create mappings between flows and poses for each flow
        flow_poses = []
        for flow_id in flow_ids:
            # Retrieve the poses that match the chakra of the current flow
            cursor.execute("SELECT pose_id FROM flow_poses WHERE flow_id = ?", (flow_id,))
            poses_in_flow = [row[0] for row in cursor.fetchall()]
            
            # Ensure that each chakra flow has a unique set of poses
            available_poses = [pose_id for pose_id in pose_ids if pose_id not in poses_in_flow]
            
            # Randomly select poses for the flow
            selected_poses = random.sample(available_poses, 5)  # Adjust the number of poses as needed
            
            # Create mappings between the current flow and the selected poses
            flow_poses.extend([(flow_id, pose_id) for pose_id in selected_poses])
        
        # Insert the mappings into the flow_poses table
        cursor.executemany("INSERT INTO flow_poses (flow_id, pose_id) VALUES (?, ?)", flow_poses)
        conn.commit()


if __name__ == "__main__":
        drop_tables()
        create_tables()
        insert_yoga_poses()
        insert_yoga_flows()
        insert_flow_poses()
