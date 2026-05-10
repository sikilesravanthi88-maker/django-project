from django.shortcuts import render, redirect, get_object_or_404
from .models import Students
from django.contrib import messages

# 🔐 Auth imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# 🔐 LOGIN VIEW
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# 🚪 LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')


# 🏠 HOME (protected)
@login_required
def home(request):
    query = request.GET.get('q')

    if query:
        data = Students.objects.filter(name__icontains=query).order_by('-id')
    else:
        data = Students.objects.all().order_by('-id')

    if request.method == "POST":
        name = request.POST.get("username")
        age = request.POST.get("age")
        email = request.POST.get("email")

        if name and name.strip():
            Students.objects.create(
                name=name.strip(),
                age=age if age else 18,
                email=email if email else "test@gmail.com"
            )
            messages.success(request, "Added successfully!")
            return redirect('home')

    return render(request, 'home.html', {'data': data})


# ❌ DELETE
@login_required
def delete(request, id):
    student = get_object_or_404(Students, id=id)
    student.delete()
    messages.success(request, "Deleted successfully!")
    return redirect('home')


# ✏️ UPDATE
@login_required
def update(request, id):
    student = get_object_or_404(Students, id=id)

    if request.method == "POST":
        name = request.POST.get("username")
        age = request.POST.get("age")
        email = request.POST.get("email")

        if name and name.strip():
            student.name = name.strip()
            student.age = age if age else student.age
            student.email = email if email else student.email
            student.save()
            messages.success(request, "Updated successfully!")
            return redirect('home')

    return render(request, 'update.html', {'student': student})