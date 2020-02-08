from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.template import loader
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from p_library.models import Book, Publisher, Author, BooksOnHand
from p_library.forms import AuthorForm, BookForm, BooksOnHandForm
from django.forms import formset_factory


def index(request):
    template = loader.get_template("index.html")
    books = Book.objects.all()
    biblio_data = {
        "title": "мою библиотеку", 
        "books": books,
        }
    return HttpResponse(template.render(biblio_data, request))

def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

###

def publisher(request):
    template = loader.get_template('publisher.html')
    publishers = Publisher.objects.all().order_by('name')

    pubinfo = []
    for publisher in publishers:
        publisher_books = Book.objects.filter(publisher=publisher)
        book_info = []
        for book in publisher_books:
            book_info.append(book.title + ' ('+book.author.full_name+')')

        publisher_info = {}
        publisher_info[publisher.name] = book_info
        pubinfo.append(publisher_info)

    biblio_data = {
        "pubinfo": pubinfo,
    }
    return HttpResponse(template.render(biblio_data, request))

### 

class AuthorEdit(CreateView):  
    model = Author  
    form_class = AuthorForm  
    success_url = reverse_lazy('p_library:author_list')  
    template_name = 'author_edit.html'  
  
  
class AuthorList(ListView):  
    model = Author  
    template_name = 'author_list.html'


def author_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)

    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        if author_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))
    else:
            author_formset = AuthorFormSet(prefix='authors')
    return render(request, 'manage_authors.html', {'author_formset': author_formset})

def books_authors_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if author_formset.is_valid() and book_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            for book_form in book_formset:  
                book_form.save()  
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))  
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render(
	    request,  
		'manage_books_authors.html',  
		{  
	        'author_formset': author_formset,  
			'book_formset': book_formset,  
		}  
	)
    
###

class BooksOnHandEdit(CreateView):
    model = BooksOnHand
    form_class = BooksOnHandForm
    success_url = reverse_lazy('p_library:friends_list')
    template_name = 'friend_edit.html'


class BooksOnHandList(ListView):
    model = BooksOnHand
    template_name = 'friend_list.html'  
