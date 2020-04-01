Todo list made using django

app: https://pingwinostodolist.herokuapp.com/
user: test_user
password: test_password

SIGN UP: ------------------------------------------------------------------

- Sign-up page is made with CreateUserForm which is extended by django UserCreationForm
the extension adds e-mail field (which at the moment is not needed, I created it just 
in case I wanted to create the e-mail verification, but at the moment I feel it is redundant )

- Once logged in user is being redirected to the page where all the actions are made, 
left side of the page is designed to handle task, right side is designed to let user 
create and choose from their lists 

LIST-DISPLAY: ------------------------------------------------------------------

- When creating the list, list is assigned to logged user, 
When choosing the list check that user is authorized to
see this list performed, one this is successful user is being redirected to the page
where tasks of the lists are displayed along with task/list editing options

TASK_DIPLAY: ------------------------------------------------------------------

- Once list is selected, task assigned to this list are shown, along with 
edit/mark_as_done/delete options, whilst list is selected options to edit/delete lists are shown 
these options are self explanatory, all of them are performing security 
check to make sure user is authorized to perform them.
 
- User is also able to sort his list, the chosed sorting option is saved in the list model, 
 this way the sorting option stays the same even after logging out
 
- User is able to change name and delete list 
When editing name of existing list, check of edited list is 
performed to make sure that logged user has access to the edit list, if not user is being
redirected back to the list display page whit appropriate message displayed

MODELS: ------------------------------------------------------------------

 List fields:
 
    name: String
    sort_by: OptionField
    user: ForgeinKey(User)
    date_created = Date
    
 Task fields:
 
    name: String
    to_be_done_date: Date
    list: ForgeinKey(List)
    crated_date: timezone.now()
    priority = OptionField
    is_done = Boolean
