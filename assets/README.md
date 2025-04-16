# 🩺 Clini — AI-Assisted Medical Report Generator

Clini is a Django web application designed to streamline the extraction of medical data from uploaded clinical documents (PDF) and generate clear, concise reports using AI.


## 🩺Features (version 1.1, April 15th 2025)

- User authentication (login, logout, register, confirm email, change password and profile details)
- Drag-and-drop file upload 
- Encryption of all uploaded data
- View and manage uploaded files per patient
- Cleans and anonymises data 
- Medical data extracted and organised using AI call #1
- Generates patient report using AI call #2
- Allows user to manually edit then download the final report 
- Optional password protection of report
 

## 🩺Tech Stack

- **Backend:** Django 3.2
- **Frontend:** HTML, CSS, JavaScript
- **AI Integration:** OpenAI API
- **PDF Handling:** PyMuPDF, python-docx
- **Deployment:** PythonAnywhere




## 🩺 Distinctiveness and Complexity


>**🩺Distinctiveness**

This app was designed for local use at a clinic in Doha, Qatar. The report generator accepts as input pdfs from laboratories or clinical software systems; text files; and image files. On one level, it can be used by anyone, but there are customisations such as stamps and letterheads specific to the organisation in which it is intended to be used intially.

> **🩺Complexity**

This Django project contains seperate apps for user authentication, data upload, and report generation. There is also a core app containing templates and logic common to all the other apps.

- Within the user app, SMTP email integration allows verification of users identity.

- Within the upload app, uploaded files are encrypted before being stored in the database. The decrypt key is specific to each user, ensuring that there can be no breach of privacy.

- Within the reportgen app, plain text is extracted from the PDF files, and then anonymised. Using an AI API call, medical data is parsed from this anonymised text. This data is cleaned and organised, and passed to the AI API again, with prompts to generate a report.

- Within the core app, the user interface is structured as a single-page web application, with html components dynamically controlled using javascript modules and CSS.


## 🩺Project Structure

```
clini/
├── clini/               # Main Django project
│   └── settings.py      # Configuration
├── upload/              # Handles drag and drop file uploads
├── user/                # User authentication
├── core/                # core files and templates
├── reportgen/           # report generation using AI
├── media/               # Uploaded user files
└── static/              # Collected static files 
```

## 🩺A list of every file created (required for CS50 project submission)

```
clini/

This is the main application directory containing the high level Django project files.​ Within it, I have created the following files:

- README.md: Describes features, stack, and folder structure of the project.
- .gitignore Lists: files and folders to be ignored by Git
- requirements.txt:Lists all Python dependencies required to run the project

/core/

This is an application directory containing logic and templates which are core to all other applications.

- admin.py : Used to register any models from the core app with the Django admin interface.
- apps.py : Defines configuration for the app. 
- models.py : Used to define database models (empty, as no models are needed in core).
- tests.py :Contains unit tests for the app.
- urls.py : Defines URL routes for the core app’s views.
- utils.py : Contains helper functions or shared logic used throughout the apps, including file encryption and decryption.
- views.py Defines views that handle HTTP requests and return responses (e.g., rendering templates like home or about pages).

/core/static/core/images/banners

- the 7 .png files in this directory are used for creating banners on the web pages

/core/static/core/images/letterheads

- the 2 .png files in this directory are used for creating letterheads in pdf reports

/core/static/core/images/TIMC/stamps

- the 2 .jpg files in this directory are used for adding stamp imgaes to pdf reports

/core/static/core/images/

- medical-pattern.jpg : a tile which is repeated to render a background graphic

/core/templates/core/

- about.html             # info about the app 
- layout.html            # base template to be extended by all other UI templates
- privacy_policy.html    # info about how data is protected
- report_builder.html    # the main singlepage web application template, which is updated dyamically by javascript

/media/documents/

- this is where user-uploaded, encrypted pdfs are stored.

/reportgen/

This is the app directory for AI report generation.

- admin.py : Used to register any models from the app with the Django admin interface.
- apps.py : Defines configuration for the app. 
- models.py : empty
- tests.py :empty
- urls.py : Defines URL routes for the reportgen app’s views.
- utils.py : Contains helper functions used throughout the apps.
- views.py Defines views that handle HTTP requests and return responses (e.g., generating reports).

/reportgen/services

Python files handling the logic of report generation.

- extract_data_pipeline.py : Function to manage the steps to extract, anonymise, redact and structure medical data from the uploaded pdf files
- anonymiser.py : Function to anonymise and redact text from the uploaded pdf files, using spacy library. Takes as input a string of text. Returns a tuple [tuple [redacted text, redacted terms], error_messages]
- extract_data_AI : Function to extract and organise medical data from redacted text, using OpenAI API call. Returns a JSON object.
- generate_report_AI: Function to generate a report from the organised medical data, using OpenAI API call. Returns a string of text.
- extract_text_from_pdfupload_object.py: Takes a PDFUpload instance, decrypts the encrypted file, and extracts its text using PyPDF2. Returns a tuple : [plain text string, errors]
- process_data: formats the data into a list of strings which can be displayed in the attriutes window of the main html template , manipulated via attributes.js
- write_pdf_report.py: function to build a PDF report from the generated text


/reportgen/static/reportgen/js/

- attributes.js : maniuplates the main template to display formatted medical data in list form
- report.js : maniuplates the main template to display the generated report and allow editing, saving, preview and download.

/staticfiles/

- the location of pooled static files for serving in deployment

/upload/

This is the app directory for UPLOAD, which allows users to upload patient data files using a drag and drop interface. It reads these files; attemp to assign them to a patient automatically; allows manual organisation of the files and creation of new patient objects using a graphical UI.

- admin.py : Used to register any models from the  app with the Django admin interface.
- apps.py : Defines configuration for the app. 
- forms.py : contains the forms used for drag and drop upload and the original user and userprofile creation. These actually should be deleted now #TO DO
- models.py : Used to define the PdfUpload, Identifier and Patient database models.
- tests.py :Contains unit tests for the app.
- urls.py : Defines URL routes for the upload app’s views.
- utils.py : Contains helper functions used in the upload app.
- views.py Defines views that handle HTTP requests and return responses

/upload/services/

- upload_pipeline.py : function to co-ordinates the flow through the upload extraction, file assignment and storage pipeline.
- find_name_in_pdf.py : function to try to find the patient's name in the text of an uploaded file.
- extract_text_from_pdf : function to read the pdf using PyPDF2 library
- jpg_to_pdf_bytes.py : takes as input a jpg image and stores it a single pdf file for incorporation into report later, and for encyrpting and storing in the filesystem.
- txt_to_pdf_bytes.py : takes as input a txt image and stores it a single pdf file for incorporation into report later, and for encyrpting and storing in the filesystem.


/upload/services/doha/

This directory contains python files with functions to extract data from pdf files which are specific to Doha Qatar. It keeps this logic seperate from the logic for more general data extraction.

- find_name_in_doha_pdf : function to find a patient's name from a text input, using regular expressions
- find_qid_in_doha_pdf : function to find a patient's nationa ID number from a text input, using regular expressions. This is used as a password for the final report
- identify_doha_pdf.py : returns the lab or source which generated type to the pdf, if it is possible to do so.


/upload/static/upload/js/

- patients.js : the JS to dyanmically update the patient list in the main html template
- upload.js : the JS to handle drag and drop of file to upload and the file list in the main html template

/upload/templates/upload/

(empty)

/user/

Contains the user registration and authentication templates and logic. Extends Django's standard user model.

- __init__.py : Marks the directory as a Python package.
- admin.py : Used to register any models from the app with the Django admin interface.
- apps.py : Defines configuration for the app. 
- forms.py : contains the forms used for user and userprofile creation and editing.
- models.py : Used to define Sser and UserProfile database models. 
- tests.py :Contains unit tests for the app.
- signals.py : contains django signal to create a new user profile object when a new user object is created.
- tokens.py : for encryption : makes a hash from timestamp and user info.
- urls.py : Defines URL routes for the user app’s views.
- utils.py : Contains helper functions used in the upload app.
- views.py Defines views that handle HTTP requests and return responses


/user/templates/user/

- activation_success.html : the page a user is directed to by their email activation link
- edit_profile.html : edit user profile template
- email_confirmation.html : the html message sent by email to a registering user
- email_verificaton_required.html: landing page for @email_cerification_required decorator. requires a user to have responded to an email
- forgot_password.html : (not yet implemented)
- login.html : login template
- register.html : sign up template



```

## 🩺 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/clini.git
cd clini
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```env
SECRET_KEY=your-django-secret-key
EMAIL_HOST_PASSWORD=your-email-password
OPENAI_API_KEY=your-openai-key
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 🩺 Deployment Notes (PythonAnywhere)

- Set `DEBUG = False` in `settings.py`
- Run `python manage.py collectstatic`
- Map `/static/` and `/media/` directories in PythonAnywhere's Web tab:
  - `/static/` → `/home/yourusername/clini/staticfiles/`
  - `/media/` → `/home/yourusername/clini/media/`

---

## 🩺 Future Features

- Clinical coding and risk scoring (e.g. QRISK, CHA₂DS₂-VASc)
- Improve robustness of generated reports using Retrieval-augmented-generation using clinical guidelines such as those published by NICE
- Patient interface for viewing repoerts
- Roll out for general use, outside of Doha Qatar

---

## 🩺 Acknowledgements

- [Django](https://www.djangoproject.com/)
- [OpenAI](https://platform.openai.com/)
- [PythonAnywhere](https://www.pythonanywhere.com/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [CS50](https://cs50.harvard.edu/)

---

## 🩺 License

Copyright (c) 2025 clini.co.uk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2. The software is provided without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software
