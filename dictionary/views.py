from django.shortcuts import render
from .models import Word

def home(request):
    results = []
    error = None
    query = ''

    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        if query:
            results = Word.objects.filter(text__icontains=query).prefetch_related('definitions').order_by('text')
            if not results:
                error = f"کلمه «{query}» یافت نشد."

    return render(request, 'dictionary/home.html', {
        'results': results,
        'error': error,
        'query': query
    })