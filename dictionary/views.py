from django.shortcuts import render
from .models import Word

def home(request):
    result = None
    error = None

    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        if query:
            try:
                word = Word.objects.get(text__iexact=query)  # case-insensitive exact match
                result = {
                    'word': word.text,
                    'definitions': word.definitions.all()  # gets all related definitions
                }
            except Word.DoesNotExist:
                error = f"کلمه «{query}» یافت نشد."

    return render(request, 'dictionary/home.html', {
        'result': result,
        'error': error,
        'query': request.POST.get('query', '') if request.method == 'POST' else ''
    })