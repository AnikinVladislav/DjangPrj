from django.shortcuts import render

def spendigs_view(request):
    return render(request, "spendings/spendings_view.html")
