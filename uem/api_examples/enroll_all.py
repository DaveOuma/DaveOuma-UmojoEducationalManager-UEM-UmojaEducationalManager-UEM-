import requests

# Define the username and password for authentication
username = ''
password = ''
base_url = 'http://127.0.0.1:8000/api/'

def enroll_in_courses():
    """
    Enrolls the user in all available courses.

    This function retrieves all courses from the API, displays the available 
    courses, and attempts to enroll the user in each course using the 
    provided username and password for authentication.

    Returns:
        None
    """

    # Retrieve all courses from the API
    r = requests.get(f'{base_url}courses/')
    courses = r.json()

    # Create a comma-separated string of available course titles
    available_courses = ', '.join([course['title'] for course in courses])
    print(f'Available courses: {available_courses}')

    # Enroll in each course
    for course in courses:
        course_id = course['id']
        course_title = course['title']
        
        # Send a POST request to enroll in the course
        r = requests.post(f'{base_url}courses/{course_id}/enroll/', auth=(username, password))
        
        if r.status_code == 200:
            # Successful request
            print(f'Successfully enrolled in {course_title}')

# Call the function to enroll in courses
enroll_in_courses()
