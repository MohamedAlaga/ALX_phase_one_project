ROLAX


Introduction
ROLAX is a cutting-edge Pharmacy Management System designed to streamline pharmacy operations by automating sales, inventory, and purchasing processes. Tailored for pharmacy staff, ROLAX enhances efficiency by reducing manual paperwork. Our solution avoids e-commerce functionality, focusing solely on optimizing internal pharmacy operations.


Authors
Mohammed Alaga (CEO, Backend Developer) <
John Mokaya (COO, Frontend Developer)     www.linkedin.com/in/john-mokaya-3b926a261

 
Installation
To set up ROLAX locally, follow these steps:

Clone the Repository

bash
Copy code
git clone https://github.com/MohamedAlaga/ALX_phase_one_project.git
Navigate to the Project Directory

bash
Copy code
cd ALX_phase_one_project
Install Dependencies

Ensure you have Node.js and Python installed. Then, run:

bash
Copy code
npm install
For Python dependencies, use:

bash
Copy code
pip install -r requirements.txt
Set Up Environment Variables

Create a .env file in the root directory and add the necessary environment variables as described in .env.example.

Run Migrations

bash
Copy code
python manage.py migrate
Start the Application

bash
Copy code
npm start
For the backend, run:

bash
Copy code
python manage.py runserver
Usage
Once the application is running, you can access the ROLAX interface by navigating to http://localhost:3000 in your web browser.

Dashboard: Manage sales, view inventory, and handle purchasing.
Reports: Generate and view operational reports.
Settings: Configure system parameters and manage users.
Contributing
We welcome contributions to ROLAX! To contribute, please follow these steps:

Fork the Repository

Create a New Branch

bash
Copy code
git checkout -b feature/YourFeatureName
Make Your Changes

Commit Your Changes

bash
Copy code
git commit -m "Add feature or fix issue"
Push to Your Branch

bash
Copy code
git push origin feature/YourFeatureName
Create a Pull Request

Open a pull request on GitHub and describe the changes you’ve made.

For more detailed contribution guidelines, see CONTRIBUTING.md 

Related Projects
Here are some related projects that might interest you:

Pharmacy Management Software (PMS): Manages inventory, sales, and vendor interactions. Tailored for larger chains with e-commerce features.
Meditech: Integrated with electronic health records (EHR), focusing on tracking sales and managing stock.
Winpharm: Desktop-based solution with limited cloud capabilities for inventory control and sales management.
Licensing
ROLAX is licensed under the MIT License. See LICENSE for more details.
