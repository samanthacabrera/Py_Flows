# This file contains the main entry point (main menu) for the CLI application. It defines the command-line interface, including commands, options, arguments, and their corresponding actions or functions.

from db.models import Flow, Pose

DB_FILE = 'yoga.db'

def main():

    while True:
        print(
                '''\n Welcome to \n
    __    ___            
    |_)   |_ |  _       
    |  \/ |  | (_) \/\/ 
       /
                    ''')
        print("1. Begin Practice")
        print("2. Manage Flows")
        print("3. Manage Poses")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            search_flows()
        elif choice == '2':
            manage_flows()
        elif choice == '3':
            manage_poses()
        elif choice == '4':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def search_flows():
    while True:
        print("\nSearch Flow Template Options:")
        print("1. Display all templates")
        print("2. Filter templates by chakra")
        print("3. Filter templates by duration")
        print("4. Filter templates by difficulty")
        print("5. Back to Main Menu")

        search_choice = input("Enter your choice: ")

        if search_choice == '1':
            list_all_yoga_flows()
        elif search_choice == '2':
            filter_by_chakra()
        elif search_choice == '3':
            filter_by_duration()
        elif search_choice == '4':
            filter_by_difficulty()
        elif search_choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

        if search_choice in ['1', '2', '3', '4']:
            flow_id = input("Enter the ID of the flow template you want to generate: ")
            generate_flow(flow_id)

def generate_flow(flow_id):
    flow = Flow.find_by_id(flow_id)
    if flow:
        print("Generating your own unique yoga flow...")
        Flow.generate_flow_with_timers(flow['chakra'], flow['duration'])
    else:
        print("Flow not found.")

def manage_flows():
    while True:
        print("\nManage Flows Options:")
        print("1. Create a new flow template")
        print("2. Delete a flow template by ID")
        print("3. Back to Main Menu")

        manage_choice = input("Enter your choice: ")

        if manage_choice == '1':
            create_yoga_flow()
        elif manage_choice == '2':
            delete_yoga_flow_by_id()
        elif manage_choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def manage_poses():
    while True:
        print("\nManage Poses Options:")
        print("1. Display all poses")
        print("2. Create a new pose")
        print("3. Delete a pose by ID")
        print("4. Back to Main Menu")

        pose_choice = input("Enter your choice: ")

        if pose_choice == '1':
            list_all_yoga_poses()
        elif pose_choice == '2':
            create_yoga_pose()
        elif pose_choice == '3':
            delete_yoga_pose_by_id()
        elif pose_choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# FLOW METHODS 

def create_yoga_flow():
    chakra = input("Enter the chakra of the flow (Root, Sacral, Solar Plexus, Heart, Thoat, Third Eye, or Crown): ")
    duration = input("Enter the duration of the flow (10, 20, 30, 40, 50, or 60 minutes): ")
    difficulty = input("Enter the difficulty of the flow (Easy, Intermediate, or Advanced): ")
    Flow.create(chakra, duration, difficulty)
    print("Yoga flow created successfully!")

def delete_yoga_flow_by_id():
    flow_id = input("Enter the ID of the flow template you want to delete: ")
    Flow.delete(flow_id)
    print("Yoga flow deleted successfully!")

def list_all_yoga_flows():
    flows = Flow.get_all()
    if flows:
        print("All Yoga Flows:")
        for flow in flows:
            print(flow)
    else:
        print("No yoga flows found.")

def filter_by_chakra():
    chakra = input("Enter the chakra to filter by (Root, Sacral, Solar Plexus, Heart, Thoat, Third Eye, or Crown): ")
    flows = Flow.filter_by_chakra(chakra)
    if flows:
        print(f"Yoga Flows with Chakra '{chakra}':")
        for flow in flows:
            print(flow)
    else:
        print(f"No yoga flows found with Chakra '{chakra}'.")

def filter_by_duration():
    duration = input("Enter the duration to filter by: ")
    flows = Flow.filter_by_duration(duration)
    if flows:
        print(f"Yoga Flows with Duration '{duration}' minutes:")
        for flow in flows:
            print(flow)
    else:
        print(f"No yoga flows found with Duration '{duration}' minutes.")

def filter_by_difficulty():
    difficulty = input("Enter the difficulty level to filter by: ")
    flows = Flow.filter_by_difficulty(difficulty)
    if flows:
        print(f"Yoga Flows with Difficulty Level '{difficulty}':")
        for flow in flows:
            print(flow)
    else:
        print(f"No yoga flows found with Difficulty '{difficulty}'.")

# POSE METHODS 

def create_yoga_pose():
    name = input("Enter the name of the pose: ")
    chakra = input("Enter the chakra of the pose (Root, Sacral, Solar Plexus, Heart, Thoat, Third Eye, or Crown): ")
    difficulty = input("Enter the difficulty of the pose (Easy, Intermediate, Advanced): ")
    Pose.create(name, chakra, difficulty)
    print("Yoga pose added successfully!")

def delete_yoga_pose_by_id():
    pose_id = input("Enter the ID of the pose you want to delete: ")
    Pose.delete(pose_id)
    print("Yoga pose deleted successfully!")

def list_all_yoga_poses():
    poses = Pose.get_all()
    if poses:
        print("All Yoga Poses:")
        for pose in poses:
            print(pose)
    else:
        print("No yoga poses found.")

if __name__ == "__main__":
    main()


