# PY FLOWS BY SAM CABREREA

# Project Description

Py Flows is a Python application that allows users to generate personalized yoga flows based on specified criteria such as chakra, duration, and difficulty. The application utilizes SQLite as the database to store information about yoga flows and poses, and it provides functionalities for creating, deleting, and generating yoga flows.

# Project Structure

.
├── Pipfile
├── Pipfile.lock
├── README.md
└── lib
├── cli.py
├── db
│   ├── models.py
│   └── seed.py
├── debug.py
└── helpers.py

# How to Run

1. $ pipenv install && pipenv shell
2. $ python lib/db/seed.py
3. $ python lib/cli.py

# Database Schema

The application utilizes SQLite as the database to store information about yoga flows and poses. The database schema includes the following tables:

flows: Stores information about yoga flows including chakra, duration, and difficulty level.

poses: Stores information about yoga poses including name, chakra alignment, and difficulty level.

flow_pose: Establishes a many-to-many relationship between flows and poses, allowing multiple poses to be associated with each flow based on shared chakras.

# Usage

To generate a personalized yoga flow, follow these steps:

1. Run the application by executing $ python lib/cli.py in the terminal.
2. Select the option: 'Begin Practice'.
3. Choose whether you would like to view all yoga flow templates or filter through flows based on chakra, duration, or difficulty.
4. Enter the id of the flow template you would like to generate.
5. The app will generate a customized yoga flow based on your preferences.

To add a new yoga flow template, follow these steps:

1. Run the application by executing $ python lib/cli.py in the terminal.
2. Select the option 'Manage flows'.
3. Select the option 'Create new flow'.
4. Provide the required information such as desired chakra, duration, and difficulty level.
5. If successful, the new flow will be added to the flows database.

To manage yoga flow templates, follow these steps:

1. Run the application by executing $ python lib/cli.py in the terminal.
2. Select the option: 'Manage flows'.
3. Choose from options such as adding a new flow, deleting a flow (by id), or viewing all poses.

To a manage yoga poses, follow these steps:

1. Run the application by executing $ python lib/cli.py in the terminal.
2. Select the option: 'Manage poses'.
3. Choose from options such as adding a new pose, deleting a pose, or viewing all poses.

# License

This project is licensed under the MIT License.
