from fabric.api import local

def server():
    local("python run.py")

def serve():
    local("python run.py")

def s():
    local("python run.py")

def build():
    local("pip install -r requirements.txt")
    local("python run.py")
    
