from django.shortcuts import render
from jobs.models import Jobs

'''Return first page with navbar and description'''
def main(request):
    return render(request, 'main.html', {})
