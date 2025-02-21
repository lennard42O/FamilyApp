from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import ShoppingItem
from .forms import ShoppingItemForm

@login_required
def shopping_list(request):
    family_members = request.user.family_members.all()
    family_members = family_members | get_user_model().objects.filter(id=request.user.id)

    items = ShoppingItem.objects.filter(added_by__in=family_members)
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
    family_members = request.user.family_members.all()
    family_members = family_members | get_user_model().objects.filter(id=request.user.id)

    item = get_object_or_404(ShoppingItem, id=item_id, added_by__in=family_members)
        
    item.completed = not item.completed
    item.save()
    return redirect("shopping-list")

@login_required
def delete_item(request, item_id):
    family_members = request.user.family_members.all()
    family_members = family_members | get_user_model().objects.filter(id=request.user.id)
    item = get_object_or_404(ShoppingItem, id =item_id, added_by__in=family_members)
    item.delete()
    return redirect("shopping-list")