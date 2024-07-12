from django.shortcuts import render, redirect
from jobs.models import Jobs

def jobs_list(request):
    all_jobs = Jobs.objects.all()
    context = {
        'all_jobs': all_jobs,
    }
    return render(request, 'jobs.html', context)