from django.shortcuts import render, redirect

# Create your views here.
from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/lists/the-only-list-in-the-world/')
    else:
        items = Item.objects.all()
        return render(request, 'home.html', {'items':items})

def new_list(request):
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text)
    return redirect('/lists/the-only-list-in-the-world/')

def list_view(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items':items})


