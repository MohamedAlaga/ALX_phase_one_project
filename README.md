

# ROLAX

## Introduction

ROLAX is a cutting-edge Pharmacy Management System designed to streamline pharmacy operations by automating sales, inventory, and purchasing processes. Tailored for pharmacy staff, ROLAX enhances efficiency by reducing manual paperwork. Our solution avoids e-commerce functionality, focusing solely on optimizing internal pharmacy operations.

 Authors
- [Mohammed Alaga (CEO, Backend Developer)]() <!-- Replace with actual LinkedIn profile -->
- [John Mokaya (COO, Frontend Developer)](https://www.linkedin.com/in/john-mokaya-3b926a261) 

## Installation

To set up ROLAX locally, follow these steps:

1.** Clone the Repository**

    ```bash
    git clone https://github.com/MohamedAlaga/ALX_phase_one_project.git
    ```

2. **Navigate to the Project Directory**

    ```bash
    cd ALX_phase_one_project
    ```

3. **Install Dependencies**

    Ensure you have Node.js and Python installed. Then, run:

    ```bash
    npm install
    ```

    For Python dependencies, use:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**

    Create a `.env` file in the root directory and add the necessary environment variables as described in `.env.example`.

5. **Run Migrations**

    ```bash
    python manage.py migrate
    ```

6. **Start the Application**

    ```bash
    npm start
    ```

    For the backend, run:

    ```bash
    python manage.py runserver
    ```

## Usage

Once the application is running, you can access the ROLAX interface by navigating to `http://localhost:3000` in your web browser. 

- **Dashboard:** Manage sales, view inventory, and handle purchasing.
- **Reports:** Generate and view operational reports.
- **Settings:** Configure system parameters and manage users.

## Contributing

We welcome contributions to ROLAX! To contribute, please follow these steps:

1. **Fork the Repository**
2. **Create a New Branch**

    ```bash
    git checkout -b feature/YourFeatureName
    ```

3. **Make Your Changes**
4. **Commit Your Changes**

    ```bash
    git commit -m "Add feature or fix issue"
    ```

5. **Push to Your Branch**

    ```bash
    git push origin feature/YourFeatureName
    ```

6. **Create a Pull Request**

    Open a pull request on GitHub and describe the changes you’ve made.

For more detailed contribution guidelines, see [CONTRIBUTING.md]

## Related Projects

Here are some related projects that might interest you:

- **Pharmacy Management Software (PMS):** Manages inventory, sales, and vendor interactions. Tailored for larger chains with e-commerce features.
- **Meditech:** Integrated with electronic health records (EHR), focusing on tracking sales and managing stock.
- **Winpharm:** Desktop-based solution with limited cloud capabilities for inventory control and sales management.

## Licensing

ROLAX is licensed under the MIT License. See [LICENSE](LICENSE) for more details.

