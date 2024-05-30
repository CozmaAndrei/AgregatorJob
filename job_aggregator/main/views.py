from django.shortcuts import render
from jobs.models import Jobs

def display_jobs(request):
    jobs = Jobs.objects.all()
    context = {
        'jobs_list': jobs,
    }
    return render(request, 'main.html', context)
