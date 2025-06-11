
from django.shortcuts import render, redirect
from myapp.forms import BookForm
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required

from django.contrib import messages

def about(request):
    return HttpResponse('this is the about page')

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('/')  # redirect to home or another page
    else:
        messages.error(request, "Error adding book. Please try again.")
        form = BookForm()
    
    return render(request, 'myapp/add_book.html', {'form': form})

from django.contrib.auth import login
from myapp.forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


from django.shortcuts import get_object_or_404
from myapp.models import Book

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = BookForm(instance=book)
    return render(request, 'myapp/edit_book.html', {'form': form})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('/')
    return render(request, 'myapp/delete_book.html', {'book': book})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'myapp/book_detail.html', {'book': book})


#@login_required
#def home(request):
#    return render(request, 'myapp/home.html')

from django.db.models import Q  # import this

def home(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'myapp/home.html', {'books': books, 'query': query})

from django.core.paginator import Paginator
#from django.db.models import Q

def home(request):
    query = request.GET.get('q')
    book_list = Book.objects.all()

    if query:
        book_list = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

    paginator = Paginator(book_list, 5)  # 5 books per page
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    return render(request, 'myapp/home.html', {'books': books, 'query': query})
