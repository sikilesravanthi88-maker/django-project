from django.shortcuts import render, redirect, get_object_or_404
from .models import Students
from django.contrib import messages


def home(request):

    query = request.GET.get('q')

    if query:
        data = Students.objects.filter(name__icontains=query).order_by('-id')
    else:
        data = Students.objects.all().order_by('-id')

    # ➕ ADD DATA
    if request.method == "POST":
        name = request.POST.get("username")

        if name and name.strip():
            Students.objects.create(name=name.strip())
            messages.success(request, "Added successfully!")
            return redirect('home')

    return render(request, 'home.html', {'data': data})


# ❌ DELETE
def delete(request, id):
    student = get_object_or_404(Students, id=id)
    student.delete()
    messages.success(request, "Deleted successfully!")
    return redirect('home')


# ✏️ UPDATE
def update(request, id):
    student = get_object_or_404(Students, id=id)

    if request.method == "POST":
        name = request.POST.get("username")

        if name and name.strip():
            student.name = name.strip()
            student.save()
            messages.success(request, "Updated successfully!")
            return redirect('home')

    return render(request, 'update.html', {'student': student})