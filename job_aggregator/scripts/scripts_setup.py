import os
import sys
import django

# Add the project to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add the project settings to the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_aggregator.settings')
# Setup Django
django.setup()


#importing functions
from scripts.bestjobs import jobs_on_bestjobs

def run_scripts():
    jobs_on_bestjobs()


if __name__ == '__main__':
    run_scripts()