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
    local("coverage run --rcfile=.coveragerc ./ss-ase/test_login.py")
    local("coverage run --rcfile=.coveragerc ./ss-ase/test_listing.py")
    local("coverage report > coverage.txt")
    local("coverage report")
