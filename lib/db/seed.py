# This file is used for populating the database with initial data. It contains scripts or functions that insert predefined data into the database tables.

import sqlite3

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
    ("Standing Two-Legged Forward Bend", "Root", "Intermediate"),
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

if __name__ == "__main__":
        drop_tables()
        create_tables()
        insert_yoga_poses()
        insert_yoga_flows()
