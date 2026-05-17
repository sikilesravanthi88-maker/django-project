from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from .models import Students

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# 🔐 LOGIN
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# 🔐 LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')


# 🏠 HOME (VIEW + ADD + SEARCH)
@login_required(login_url='/')
def home(request):
    query = request.GET.get('q')

    if query:
        data = Students.objects.filter(name__icontains=query).order_by('-id')
    else:
        data = Students.objects.all().order_by('-id')

    # ➕ ADD STUDENT
    if request.method == "POST":
        roll = request.POST.get("roll")
        name = request.POST.get("name")
        age = request.POST.get("age")
        email = request.POST.get("email")

        # validation
        if not roll or not name:
            messages.error(request, "Roll & Name are required!")
            return redirect('home')

        # duplicate check
        if Students.objects.filter(roll_number=roll).exists():
            messages.error(request, "Roll number already exists!")
            return redirect('home')

        Students.objects.create(
            roll_number=roll,
            name=name.strip(),
            age=int(age) if age else 18,
            email=email if email else "test@gmail.com"
        )

        messages.success(request, "Student added successfully!")
        return redirect('home')

    return render(request, 'home.html', {'data': data})


# ❌ DELETE STUDENT
@login_required(login_url='/')
def delete(request, id):
    student = get_object_or_404(Students, id=id)
    student.delete()
    messages.success(request, "Deleted successfully!")
    return redirect('home')


# ✏️ UPDATE STUDENT
@login_required(login_url='/')
def update(request, id):
    student = get_object_or_404(Students, id=id)

    if request.method == "POST":
        roll = request.POST.get("roll")
        name = request.POST.get("name")
        age = request.POST.get("age")
        email = request.POST.get("email")

        # validation
        if not roll or not name:
            messages.error(request, "Roll & Name required!")
            return redirect('update', id=id)

        # duplicate check (exclude current record)
        if Students.objects.filter(roll_number=roll).exclude(id=id).exists():
            messages.error(request, "Roll number already exists!")
            return redirect('update', id=id)

        student.roll_number = roll
        student.name = name.strip()
        student.age = int(age) if age else student.age
        student.email = email if email else student.email
        student.save()

        messages.success(request, "Updated successfully!")
        return redirect('home')

    return render(request, 'update.html', {'student': student})


# 📍 NEARBY PAGE
@login_required(login_url='/')
def nearby(request):
    return render(request, 'nearby.html')


# 📡 GET NEARBY DATA (API)
@login_required(login_url='/')
def get_nearby_places(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    place_type = request.GET.get('type')  # hospital / petrol

    # 👉 Dummy data (later real API add chestam)
    data = [
        {"name": "Apollo Hospital", "type": "hospital", "distance": "1.2 km"},
        {"name": "Indian Oil Petrol Pump", "type": "petrol", "distance": "0.8 km"},
        {"name": "City Care Hospital", "type": "hospital", "distance": "2 km"},
        {"name": "HP Petrol Bunk", "type": "petrol", "distance": "1.5 km"},
    ]

    # filter based on type
    if place_type:
        data = [d for d in data if d["type"] == place_type]

    return JsonResponse(data, safe=False)