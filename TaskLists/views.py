from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import CreateList, AddTask, NewNameForm, TaskRenameForm, SortBy
from django.contrib.messages import add_message, INFO, ERROR
from .models import Task, List

@login_required
def display_lists(request, list_id=None):
    tasks = None
    current_list = None

    """
    if received list_id
    Get list to work on using list id and save it to current list
    """
    if list_id:
        try:
            current_list = List.objects.get(id=list_id)
        except ObjectDoesNotExist:
            add_message(request, INFO, "List does not exist")
            return redirect(reverse("display-lists"))


    """
    check if logged user is same as lists user
    In case someone unathorized tries to access list
    get tasks from the list
    """
    if current_list:
        if current_list.user != request.user:
            add_message(request,INFO , "User not authenticated to view this list!")
            return redirect(reverse("display-lists"))
        tasks = Task.objects.filter(list=current_list).all().order_by(current_list.ordered_by)


    """
    If Params does not exist do not pass the form to template, template will show link to page with right param
    probably I could have it done better now, without use of params
    """
    add_new_task_form = AddTask() if request.GET.get("add_new_task") else None
    create_list_form = CreateList() if request.GET.get("create_new_list") else None
    new_name_form = NewNameForm() if request.GET.get("rename") else None
    sort_by_form = SortBy(initial={"sort_options": current_list.ordered_by}) if current_list else SortBy()

    task_rename_form = None
    if request.GET.get("edit_task") and request.GET.get("task_id") and Task.objects.filter(id=request.GET.get("task_id")).first().list.user == request.user:
        t = Task.objects.get(id=request.GET.get("task_id"))
        task_rename_form = TaskRenameForm(initial= {"new_name": t.name,
                                                    "new_priority": t.priority,
                                                    "new_to_be_done_date": t.to_be_done_date})

    return render(request, "TaskLists/lists.html", { "create_list_form": create_list_form,
                                                     "add_new_task": add_new_task_form,
                                                     "task_rename_form": task_rename_form,
                                                     "new_name_form": new_name_form,
                                                     "sort_by_form": sort_by_form,
                                                     "current_list": current_list,
                                                     "lists": request.user.lists.all(),
                                                     "tasks": tasks})



@login_required
def sort_tasks(request, list_id):
    """
    if user is logged in change in the model List sorting option field,
    "display-task" will use it order lists
    """
    if List.objects.get(id=list_id).user == request.user:
        sort_options_choosed = request.GET.get("sort_options")
        current_list = List.objects.filter(id=list_id)
        current_list.update(ordered_by=sort_options_choosed)
    return redirect("display-tasks", list_id)


@login_required
def add_new_list(request):

    if not request.user:
        return redirect(reverse('login'))

    new_list = List(user=request.user)
    CreateListForm = CreateList(request.POST, instance=new_list)

    if CreateListForm.is_valid():
        CreateListForm.save()
    else:
        add_message(request,INFO , "Cannot create new list! Not valid name")
        return redirect("display-lists")

    return redirect(reverse('display-tasks', args={new_list.id}))


@login_required
def add_new_task(request, list_id):

    try:
        new_task = Task(list=List.objects.get(id=list_id))
    except ObjectDoesNotExist:
        add_message(request, INFO, "List does not exist/Not Authorized")
        return redirect(reverse('display-tasks', args={list_id}))

    if List.objects.get(id=list_id).user != request.user:
        add_message(request, INFO, "List does not exist/Not Authorized")
        return redirect(reverse('display-tasks', args={list_id}))

    add_task_form = AddTask(data=request.POST, instance=new_task)

    if add_task_form.is_valid():
        add_task_form.save()
    else:
        add_message(request, INFO, "Cannot add new task, Form not valid")

    return redirect(reverse('display-tasks', args={list_id}))


@login_required()
def edit_list(request, list_id):
    try:
        list = List.objects.filter(id=list_id)
    except ObjectDoesNotExist:
        add_message(request, INFO, "List does not exist/User not authorized!!")
        return redirect(reverse('display-lists'))

    if request.user != list.first().user:
        add_message(request, INFO, "List does not exist/User not authorized!!")
        return redirect(reverse('display-lists'))

    new_name_form = NewNameForm(request.POST)

    if new_name_form.is_valid():
        list.update(name=new_name_form['new_name'].value())
    else:
        add_message(request, INFO, "Cannot edit list, Form not valid")
        return redirect(reverse('display-lists'))
    return redirect(reverse('display-tasks', args={list_id}))

@login_required()
def delete_list(request, list_id):

    try:
        l = List.objects.get(id=list_id)
    except ObjectDoesNotExist:
        add_message(request, INFO, "List does not exist/User not authorized!!")
        return redirect(reverse('display-lists'))

    if l.user != request.user:
        add_message(request, INFO, "User not authorized!!")
        return redirect(reverse("display-lists"))

    l.delete()
    return redirect(reverse("display-lists"))

@login_required()
def update_task(request, list_id, task_id):
    t = Task.objects.filter(id=task_id)
    if t.first().list.user != request.user:
        add_message(request, INFO, "User not authorized!!")
        return redirect(reverse("display-lists"))


    if request.GET.get('delete'):
        t.delete()

    if request.POST:
        new = TaskRenameForm(request.POST)
        if new.is_valid():
            t.update(name=new.data['new_name'], priority=new.data['new_priority'], to_be_done_date=new.cleaned_data['new_to_be_done_date'])

    if request.GET.get('is_done'):
        t.update(is_done = request.GET.get('is_done'))

    return redirect(reverse("display-tasks", args={list_id}))