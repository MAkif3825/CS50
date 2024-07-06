# Call & R Web Application

#### Video Demo:  <URL HERE>
#### Description
    The **Call & R** web application is designed to help users manage their schedules effectively, offering features like event tracking, task management, habit monitoring, and editting them. It leverages technologies such as Flask, Jinja, Python, HTML, CSS, JavaScript, FullCalendar, and Bootstrap.

![Call & R Screenshot](ss/ss1.png) <!-- Replace with an actual screenshot if available -->

## Table of Contents

- [Pages](#pages)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Database](#database)
- [Server Side](#server)
- [Contributing](#contributing)
- [License](#license)

## Pages

- **Homepage**: Provides a visual calendar interface for users and add button in order to add new events, tasks and habits. Calendar interface displays the events, tasks and habits according to their chosen title, background color and time period. Add modal needs some features about the thing user trying to add like start date, end date, title. It also provides "mini today table" to ease visualising today's plan. It also has a profile section including an avatar, name and today's date. User can use the navigation bar in order to move another pages as well as the settings and logout buttons near the user name.

- **Settings**: Users can change most of the things about them in the data base such as name, surname, avatar, username and password. The user has to confirm the ccurrent password in order to apply the changes done in settings page.

- **Overview**: Users can reach all of the events in the database allocated for user them. They can also delete events, edit tasks and habits in terms of some features. Currently active elements and past elements are seperated form each other as well as the events, tasks and habits.

- **Log in and Register**: Allows users to log in or register to the Call & R web app.

- **Apology**: Throw an apology page for invalid or forbidden proccess.

## Screenshots

![Screenshot 1](ss/ss2.png)
![Screenshot 2](ss/ss3.png)
<!-- Add more screenshots if available -->

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/call-and-r.git
    cd call-and-r
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    flask run
    ```

4. Access the application in your web browser at the link occuring in the terminal.

## Usage

1. Register or log in to the application.
2. Navigate through the settings, overview and homepage pages.
3. Add, edit, and delete events, tasks, and habits.
4. Customize your schedule and make use of reminders.
5. Explore the various features and functionalities provided.

## Technologies Used

- **Flask:** To operate server side
- **Jinja:** To provide communicat,on between server side and user side
- **Python:** To work collaborately with flask
- **HTML:** To generate user side pages
- **CSS:** To make the site more appealing
- **JavaScript:** To give more interactivity to page
- **FullCalendar:** To use calendar in site
- **Bootstrap:** To make the site more appealing

## Database

The application uses an SQLite3 database to store user data, including events, tasks, habits, and user account details. There are some tables storing the information of users:


## Server Side

The application uses python in the server side. Flsak implamentation in python operates the process.

## Contributing

Contributions are welcome! If you find a bug or have an enhancement in mind, please submit an issue or a pull request following the project's guidelines.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to expand this README with more detailed information about your project's architecture, code structure, and any specific instructions for contributors. Make sure to include information on how to set up the database, how to work with Flask, and any other important aspects of your application.