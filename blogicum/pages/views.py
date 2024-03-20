from django.shortcuts import render


# about
def about(request):
    """О программе"""
    return render(request, 'pages/about.html')


def rules(request):
    """Правила"""
    return render(request, 'pages/rules.html')
