# Secure Auth API

A Django-Based Authentication REST API with JWT and Social Login Integration
Tools & technologies used: Python, Django, REST API, JWT, MySQL

## Description

Created a robust authentication REST API using Django and Django REST Framework. 
Integrated JWT tokens for secure and scalable user authentication.– Developed social login features to streamline user access via popular platforms.
Ensured comprehensive security and ease of use with modern authentication protocols.

## Installation

To install necessary modules and packages, follow these steps:

### Backend Side

1. Clone the repository:
    ```bash
    
    cd Secure-Auth-API
    ```

2. Create a virtual environment:
    ```bash
    virtualenv myenv
    ```

3. Activate the virtual environment:
    ```bash
    source ./myenv/Scripts/activate
    ```

4. Install all required modules from requirements.txt:
    ```bash
    pip install -r requirements.txt
    ```

## Starting the Application

To start the application, follow these steps:

### Starting the Server

1. Run the following command to make migrations:
    ```bash
    python manage.py makemigrations
    ```

2. Apply migrations:
    ```bash
    python manage.py migrate
    ```

3. Load initial country data:
    ```bash
    python manage.py load_country_data ./countryData.json
    ```

4. Start the server:
    ```bash
    python manage.py runserver
    ```

## Usage

Explain how to use your application or provide examples here.

## Contributing

If you would like to contribute to the project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Hat tip to anyone whose code was used.

## Contact

If you have any questions, suggestions, or feedback, feel free to contact [rhtknt01@gmail.com](mailto:rhtknt01@gmail.com).
