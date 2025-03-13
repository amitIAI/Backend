Steps to Integrate:
Python:
pip install -r requirements.txt


Node,js
Move the backend code into a /backend folder.
Navigate to the backend folder and install dependencies:
	cd backend
	npm install express dotenv googleapis multer fs path axios cors exceljs
Run the backend server:
	node server.js
Update your React frontend (src/contentApi/driveApi.js)
	Create a file driveApi.js inside src/contentApi/ to handle API calls to the backend