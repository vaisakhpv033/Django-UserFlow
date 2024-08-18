# UserFlow

UserFlow is a web application built with Django, focused on managing user accounts, including authentication (login and signup), user data storage, and administration. The project includes a comprehensive admin panel for managing users, with features such as searching, creating, editing, and deleting user data. The application also handles sessions and cookies securely.

## Features

- **User Authentication**
  - User Signup and Login with validation
  - Custom `SignupForm` and `LoginForm` for flexible user management
  - Session and cookie management for secure authentication
  - Home page for authenticated users

- **Admin Panel**
  - Secure admin login with validation
  - View, search, create, edit, and delete user data
  - Manage user sessions

- **Database**
  - Store and manage user data in a relational database
  - User data including username, email, and passwords (hashed)

## Getting Started

### Prerequisites

- Python 3.10.6
- Django 5.1
- PostgreSQL or another supported database
- psycopg2==2.9.9
- python-decouple==3.8

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vaisakhpv033/Django-UserFlow.git
  
