A Simple Hello World Project

Softwares and Platform Requirements

1. Python
2. Docker
3. VS Code
3. Git and Github
4. GCP App Engine




Python Commands Required

Creating a Python Virtual Environment

```
python -m venv venv
```

Executing the Application

```
python filename.py
```

Upgrade pip

```
python -m install pip --upgrade pip
```

Installing the required python Package
```
pip install <package-name>
```

Git Commands


Cloning a Repository from the Github

```
git clone "<repository-url>"
```


Setting up the Git Credentials globally (Mandatory to push the changes)

```
git config --global user.name "<user-name>"
```
```
git config --global user.email "<user-email>"
```
```
git config --global user.password "<user-pass>"
```


Check the status of file

```
git status
```


Add Files to the Staging Area

```
git add .
```

```
git add "<file-names>"
```

Inserting Items from Staging Area to Local Repo

```
git commit -m "<message>"
```

Pushing the code to Github origin  main Repo

```
git push origin main
```

Docker Commands

```
docker build -t <image-name:version>
```

```
docker run -e PORT:5000 -p 5000:5000 <image-id or image-name:version>
```