from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import ToDo
from .forms import FormTodo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

@login_required 
def home(request):
    tarea_a_editar = None
    if request.method == 'POST':
        if 'save' in request.POST:
            form = FormTodo(request.POST)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.user = request.user
                tarea.save()

        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            ToDo.objects.get(pk=pk, user=request.user).delete()

        elif 'toggle' in request.POST:
            pk = request.POST.get('toggle')
            tarea = ToDo.objects.get(pk=pk)
            tarea.complete = not tarea.complete
            tarea.save()

        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            tarea_a_editar = get_object_or_404(ToDo, pk=pk)

        elif 'update' in request.POST:
            pk = request.POST.get('id')
            tarea = get_object_or_404(ToDo, pk=pk)
            form = FormTodo(request.POST, instance=tarea)
            if form.is_valid():
                form.save()

        return HttpResponseRedirect(request.path_info)

    tareas = ToDo.objects.filter(user=request.user)
    form = FormTodo(instance=tarea_a_editar) if tarea_a_editar else FormTodo()
    return render(
        request,
        'home.html',
        {'tareas': tareas, 'form': form, 'tarea_a_editar': tarea_a_editar},
    )


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
           
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
