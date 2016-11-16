from fabric.api import local

def server():
    local("python ./ss-ase/run.py")

def serve():
    server()

def s():
    server()

def build():
    local("pip install -r requirements.txt")
    server()

def test():
    local("python ./ss-ase/test_login.py")
    local("python ./ss-ase/test_listing.py")
