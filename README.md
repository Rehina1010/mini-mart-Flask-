# Mini Mart - E-commerce Website

Mini Mart is a small e-commerce website built using Flask, designed to provide a seamless shopping experience with a focus on simplicity and ease of use. This project includes user registration, login, password reset, and email verification functionalities, all powered by SMTP. Additionally, the website integrates Stripe for secure payment processing.

## Features

- **User Authentication:**
  - User registration and login.
  - Password reset functionality.
  - Email verification using SMTP.

- **Payment Processing:**
  - Integration with Stripe for secure and seamless payment transactions.

- **Styling:**
  - Utilizes Bootstrap 5 for responsive and modern UI design.
  - Custom CSS for additional styling and branding.

- **Frontend Interactivity:**
  - JavaScript for dynamic features such as pop-up messages and image carousels.
  - Automatic image carousel transitions every 5 seconds.

- **Image Management:**
  - Images are stored on Cloudinary, with links saved in the PostgreSQL database.
  - Easy image management through an admin dashboard.

- **Database:**
  - PostgreSQL is used as the database to store user information, product details, and other relevant data.

- **Admin Dashboard:**
  - An intuitive admin interface for managing products, including adding images and descriptions without needing to modify the code.

## Technologies Used

- **Backend:**
  - Flask (Python web framework)
  - PostgreSQL (Database)
  - SMTP (Email verification)
  - Stripe (Payment processing)

- **Frontend:**
  - Bootstrap 5 (CSS framework)
  - Custom CSS
  - JavaScript (for interactive features)

- **Image Storage:**
  - Cloudinary (Cloud-based image storage)

## Setup and Installation

To run this project locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Rehina1010/mini-mart-Flask-.git
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   poerty install
   ```

3. **Install Dependencies:**
   ```bash
   poetry install
   ```

4. **Environment Variables:**
   - Rename the `.env.example` file to `.env`.
   - Fill in the necessary environment variables such as database URLs, Stripe API keys, SMTP credentials, and Cloudinary settings.

5. **Database Setup:**
   - Ensure PostgreSQL is installed and running.
   - Create a new database and update the `.env` file with the database URI.
   - Run the database migrations:
     ```bash
     flask db upgrade
     ```

6. **Run the Application:**
   ```bash
   flask run
   ```

7. **Access the Application:**
   - Open your web browser and go to `http://127.0.0.1:5000/`.

## Admin Dashboard

The admin dashboard is accessible at `/admin` and requires authentication. Use the following steps to manage products:

1. **Login:**
   - Navigate to `/admin`.

2. **Add Products:**
   - Once logged in, you can add new products by uploading images and providing descriptions.
   - The images will be stored on Cloudinary, and the links will be saved in the database.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

---

Thank you for checking out Mini Mart! If you have any questions or need further assistance, please don't hesitate to reach out.