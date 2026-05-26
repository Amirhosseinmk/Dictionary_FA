from django.db.models import Q
from django.shortcuts import render
from .models import Word

def home(request):
    exact_results = []
    related_results = []
    total_results = 0
    error = None
    query = ''

    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        if query:
            exact_results = Word.objects.filter(
                Q(text__iexact=query) | Q(definitions__text__iexact=query)
            ).distinct().prefetch_related('definitions')

            related_results = Word.objects.filter(
                Q(text__icontains=query) | Q(definitions__text__icontains=query)
            ).exclude(pk__in=exact_results).distinct().prefetch_related('definitions').order_by('text')

            total_results = exact_results.count() + related_results.count()
            if not total_results:
                error = f"کلمه «{query}» یافت نشد."

    return render(request, 'dictionary/home.html', {
        'exact_results': exact_results,
        'related_results': related_results,
        'total_results': total_results,
        'error': error,
        'query': query
    })
def about_us(request):
    return render(request, 'dictionary/aboutUs.html')

