# Deploying to PythonAnywhere

PythonAnywhere is an excellent choice for hosting this Flask clinic application because it allows for persistent local SQLite databases and local file uploads on their free tier natively.

I have updated your code (`app.py`) to use **absolute paths** for your database and upload directories. This ensures that the application won't crash when running from a different working directory on the server. I also generated the `requirements.txt` file for you in your project folder.

Here is the step-by-step guide to get your application running online.

## Step 1: Create an Account
1. Go to [PythonAnywhere](https://www.pythonanywhere.com/) and create a **Beginner (Free)** account.
2. Verify your email address.

## Step 2: Upload Your Code
You need to transfer your files from your local machine to PythonAnywhere.

1. In PythonAnywhere, go to the **Files** tab.
2. Under "Directories", you should see your `/home/yourusername/` directory.
3. Create a new directory named `mysite` (or whatever you prefer) and click into it.
4. Use the "Upload a file" button to upload your project files. It's often much faster to **compress your entire `divyadeep-clinic` folder into a `.zip` file** on your machine, upload the `.zip`, and then use the PythonAnywhere Bash console to unzip it.
    - If you upload a zip file, go to your **Consoles** tab, start a new **Bash** console, and run:
      ```bash
      cd mysite
      unzip your_zip_file.zip
      ```
    - Make sure `app.py`, `database.db`, `requirements.txt`, and the folders `static/` and `templates/` are directly inside the `mysite/` folder. (Note: You do not need the virtual environment folder).

## Step 3: Create the Web App
1. Go to the **Web** tab.
2. Click the **"Add a new web app"** button.
3. Click "Next" to confirm your domain name (it will look like `yourusername.pythonanywhere.com`).
4. Select **Flask** framework.
5. Select **Python 3.10** (or whichever latest version you want to use).
6. Under "Enter path to a Flask app.py", ensure it points to where your file is located. E.g., `/home/yourusername/mysite/app.py`.
7. Click "Next". Your web framework is now configured.

## Step 4: Install Dependencies
Your app requires `Flask` and `Werkzeug`.

1. Go to the **Consoles** tab and open a **Bash** console.
2. Navigate to your app directory:
   ```bash
   cd ~/mysite
   ```
3. Install the packages from your newly created `requirements.txt`:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
   *(Ensure you use `pip3.10` if you selected Python 3.10 in Step 3).*

## Step 5: Configure the WSGI File
PythonAnywhere uses a WSGI file to connect their web server to your Flask code.

1. Go back to the **Web** tab.
2. Look for the **"Code"** section.
3. Click on the link next to **"WSGI configuration file:"** (it will look something like `/var/www/yourusername_pythonanywhere_com_wsgi.py`).
4. It will open a text editor. PythonAnywhere should have already set this up reasonably well if you selected Flask earlier, but verify the bottom imports look exactly like this:

```python
import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/mysite'
if path not in sys.path:
    sys.path.append(path)

# Import your Flask app
from app import app as application
```
*(Make sure to replace `yourusername` with your actual username and `mysite` with the folder where your code lives).*

5. Click **"Save"** in the top right corner.

## Step 6: Reload the Application
1. Go back to the **Web** tab.
2. Click the big green **"Reload yourusername.pythonanywhere.com"** button at the top.

## Step 7: View Your Site!
1. Click the link at the top of the Web tab (e.g., `http://yourusername.pythonanywhere.com`).
2. Your dynamic Dermatology clinic CMS is now live!
3. Go to `/admin` and log in with your credentials to double-check that database interactions (like adding treatments and gallery photos) are working correctly.
