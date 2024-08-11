# FameSocialNetwork - Big Data Engineering Project

## Project Overview

### Background and Motivation
The concept of social networks has evolved significantly, but they continue to face challenges such as the spread of misinformation, hate speech, and the lack of quality control. This project aims to tackle these challenges by integrating a "fame profile" system into a social network. Inspired by the novel *Fameland* by Tom J. Petersson, the fame profile tracks users' skills and expertise, assigning them positive or negative fame based on their contributions. This approach is envisioned as a way to ensure that knowledgeable voices are amplified while misinformation is minimized.

### General Idea: Fame Profiles
In this project, we aim to create a social network where every user's contributions are filtered and judged based on their "fame profile." The fame profile is a record of a user's skills and expertise, which evolves based on their actions on the platform. The more expertise a user demonstrates in a particular area, the more their fame increases. Conversely, spreading misinformation or making unsubstantiated claims will negatively impact their fame.

## Installation

### Prerequisites
- Python 3.8+
- Django 3.2+
- PostgreSQL or any other preferred RDBMS
- Pip (Python package manager)

### Setup Instructions

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/FameSocialNetwork.git
   cd FameSocialNetwork
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Database Setup**
   - Create a PostgreSQL database:
     ```sql
     CREATE DATABASE famesocialnetwork;
     ```
   - Update the `settings.py` file with your database credentials:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql_psycopg2',
             'NAME': 'famesocialnetwork',
             'USER': 'yourusername',
             'PASSWORD': 'yourpassword',
             'HOST': 'localhost',
             'PORT': '',
         }
     }
     ```

4. **Apply Migrations**
   ```sh
   python manage.py migrate
   ```

5. **Create a Superuser**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the Development Server**
   ```sh
   python manage.py runserver
   ```

7. **Access the Application**
   - Open your web browser and navigate to `http://127.0.0.1:8000/`

## Features

### Existing Functionality
- **Social Network App (`socialnetwork`):**
  - Data models, internal API, and basic HTML views.
  - User authentication, timelines, and search.
  - Simple textual posts and fake data generation.
  - Users can follow and unfollow each other.

- **Fame Profile App (`fame`):**
  - Data models and HTML views for fame profiles.
  - Creation of fake data and basic unit tests.
  - Integration with the `socialnetwork` app, allowing fame profiles to be accessed directly from user timelines.

### Tasks Implemented
1. **API Enhancements:**
   - Prevent publishing of posts in areas where the user's fame is negative.
   - Automatically adjust fame based on the truthfulness of posts.
   - Implement endpoints to retrieve experts and bullshitters in specific areas.

2. **Additional Views:**
   - HTML views for listing experts and bullshitters.
   - Follow and unfollow users directly from the timeline.

3. **Extensions:**
   - Creative ideas to further enhance the fame profile concept (details in `extensions.txt`).

## Testing

### Running Unit Tests
To ensure the correctness of your implementation, you can run the provided unit tests:
```sh
python manage.py test famesocialnetwork
```

## Contribution Guidelines
- Fork the repository and create a new branch for your feature.
- Submit a pull request with a detailed description of your changes.
- Ensure that your code passes all unit tests and follows PEP 8 guidelines.

## Acknowledgments
This project was developed as part of the Big Data Engineering course at Saarland University under the supervision of Prof. Dr. Jens Dittrich.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README further based on specific details or additional features of your project.
