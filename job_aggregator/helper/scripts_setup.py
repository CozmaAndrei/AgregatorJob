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
from helper.bestjobs import jobs_on_bestjobs
from helper.ejobs import jobs_on_ejobs
from helper.juniors import jobs_on_juniors

def run_scripts():
    jobs_on_ejobs()
    jobs_on_bestjobs()
    jobs_on_juniors()


if __name__ == '__main__':
    run_scripts()