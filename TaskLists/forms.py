from django.forms import ModelForm, DateField, Form, CharField, ChoiceField
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from .models import List, Task, order_by, priorities




class SortBy(Form):
    sort_options = ChoiceField(choices=order_by)


class NewNameForm(Form):
    new_name = CharField(max_length=124, min_length=1)


class TaskRenameForm(Form):
    new_name = CharField(max_length=124, min_length=1)
    new_to_be_done_date = DateField(widget=SelectDateWidget)
    new_priority = ChoiceField(choices=priorities)

class CreateList(ModelForm):
    class Meta:
        model = List
        fields = ['name']


class AddTask(ModelForm):
    to_be_done_date = DateField(initial=timezone.now(), widget=SelectDateWidget)
    priority = ChoiceField(choices=priorities)

    class Meta:
        model = Task
        fields = ['name', "to_be_done_date", "priority"]


