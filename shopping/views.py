from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import ShoppingItem
from .forms import ShoppingItemForm

@login_required
def shopping_list(request):
    items = ShoppingItem.objects.filter(added_by=request.user)  # Nur Einträge des aktuellen Benutzers
    return render(request, 'shopping/list.html', {'items': items})

@login_required
def add_item(request):
    if request.method == "POST":
        form = ShoppingItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.added_by = request.user
            item.save()
            return redirect("shopping-list")
    else:
        form = ShoppingItemForm()
    return render(request, "shopping/add_item.html", {"form": form})

@login_required
def toggle_item(request, item_id):
    item = get_object_or_404(ShoppingItem, id=item_id, added_by=request.user)
    item.completed = not item.completed
    item.save()
    return redirect("shopping-list")

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(ShoppingItem, id =item_id, added_by=request.user)
    item.delete()
    return redirect("shopping-list")