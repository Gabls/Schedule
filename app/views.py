#region Librarys
from .models import Event, Event_User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_django
from django.contrib.auth import login as login_django
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.db.models import Q
#endregion



#region User (Login)
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        loged_user = authenticate(username=request.POST.get("email"), password=request.POST.get("password"))

        if loged_user:
            login_django(request, loged_user)
            return redirect('dashboard')
        else:
            return render(request, "login.html", {"error_login": 1})
#endregion

#region User (Logout)
@login_required(login_url="login")
def logout(request):
    logout_django(request)
    return redirect('login')
#endregion

#region User (Create)
def createUser(request, list_of_days, list_of_events):
    if User.objects.filter(username=request.POST.get("email")):
        return render(request, "dashboard.html", {"erro": "Usuário com esse e-mail não está disponível, tente novamente!", "user": request.user, "scheduleDates": list_of_days, "scheduleEvents": list_of_events})
    else:
        is_staff = True if request.POST.get("is_staff") == "True" else False
        User.objects.create_user(username=request.POST.get("email"), password=request.POST.get("password"), first_name=request.POST.get("first_name"), is_staff=is_staff)
        return render(request, "dashboard.html", {"success": "Usuário adicionado com sucesso!", "user": request.user, "scheduleDates": list_of_days, "scheduleEvents": list_of_events})
#endregion

#region User (Read)
@login_required(login_url="login")
def readUsers(request):
    if request.user.is_staff:
        return render(request, "users.html", {"users": User.objects.filter(~Q(username="admin")).order_by("username")})
    else:
        return redirect('dashboard')

#endregion

#region User (Update)
@login_required(login_url="login")
def updateUser(request):
    if request.user.is_staff:
        if request.method == "GET":
            return render(request, "updateUser.html", {"user": User.objects.get(username=request.META['QUERY_STRING'])})
        elif request.method == "POST":
            print(request.POST.get("is_staff")) 
            user = User.objects.get(username=request.META['QUERY_STRING'])
            user.password = request.POST.get("password") if request.POST.get("password") else user.password
            user.first_name = request.POST.get("first_name") if request.POST.get("first_name") else user.first_name
            user.is_staff = True if request.POST.get("is_staff") == "True" else False
            user.save()
            return redirect("users")
    else:
        return redirect("dashboard")
#endregion

#region User (Delete)
@login_required(login_url="login")
def deleteUser(request):
    if request.user.is_staff:
        (User.objects.get(username=request.META['QUERY_STRING'])).delete()
        return redirect('users')
    else:
        return redirect('dashboard')
#endregion



#region Event (Enter)
def enterEvent(request):
    event = Event.objects.get(id=request.POST.get("link"))
    if Event_User.objects.select_related("event", "participant").filter(participant_id=request.user.id, event__full_date=event.full_date):
        list_of_days = daysOfWeek(date.today())
        list_of_events = eventsOfWeek(date.today(), Event_User.objects.select_related("event", "participant").filter(participant_id=request.user.id))
        return render(request, "dashboard.html", {"erro": "Você já tem um compromisso marcado nesse horário, tente novamente!", "user": request.user, "scheduleDates": list_of_days, "scheduleEvents": list_of_events})
    else:
        Event_User.objects.create(event_id=event.id, participant_id=request.user.id)
        list_of_days = daysOfWeek(date.today())
        list_of_events = eventsOfWeek(date.today(), Event_User.objects.select_related("event", "participant").filter(participant_id=request.user.id))
        return render(request, "dashboard.html", {"success": "Evento adicionado com sucesso!", "user": request.user, "scheduleDates": list_of_days, "scheduleEvents": list_of_events})

#endregion

#region Event (Exit)
@login_required(login_url="login")
def exitEvent(request):
    print(request.META['QUERY_STRING'])
    (Event_User.objects.get(event_id=request.META['QUERY_STRING'], participant_id=request.user.id)).delete()
    return redirect('dashboard')
#endregion

#region Event (Create)
def createEvent(request):
    if (Event_User.objects.select_related("event", "participant").filter(participant_id=request.user.id)).filter(event__full_date=request.POST.get("fullDate")):
        list_of_days = daysOfWeek(date.today())
        list_of_events = eventsOfWeek(date.today(), Event_User.objects.select_related("event", "participant").filter(participant_id=request.user.id))
        return render(request, "dashboard.html", {"erro": "Você já tem um compromisso marcado nesse horário, tente novamente!", "user": request.user, "scheduleDates": list_of_days, "scheduleEvents": list_of_events})
    else:
        new_event = Event.objects.create(title=request.POST.get("title"), description=request.POST.get("description"), full_date=request.POST.get("fullDate"), creator=request.user)
        Event_User.objects.create(event_id=new_event.id, participant_id=request.user.id)
        list_of_days = daysOfWeek(date.today())
        list_of_events = eventsOfWeek(date.today(), Event_User.objects.select_related("event", "participant").filter(participant_id=request.user.id))
        return render(request, "dashboard.html", {"success": "Evento adicionado com sucesso!", "user": request.user, "scheduleDates": list_of_days, "scheduleEvents": list_of_events})
#endregion

#region Event (Read)
def daysOfWeek(today):
    list_of_days = []

    for i in range(7):
        current_date = today + timedelta(days=i)
        match current_date.weekday():
            case 0:
                week_day = "Segunda-feira"
            case 1:
                week_day = "Terça-feira"
            case 2:
                week_day = "Quarta-feira"
            case 3:
                week_day = "Quinta-feira"
            case 4:
                week_day = "Sexta-feira"
            case 5:
                week_day = "Sabádo"
            case 6:
                week_day = "Domingo"
        list_of_days.append({"day_of_week": week_day, "day": current_date.strftime("%d")})
    return list_of_days

def eventsOfWeek(today, events_of_week):
    list_of_events = []
    
    for i in range(7):
        list_of_events.append(events_of_week.filter(event__full_date__range=[(today + timedelta(days=i)).strftime("%Y-%m-%d 00:00:00"), (today + timedelta(days=i)).strftime("%Y-%m-%d 23:59:59")]).order_by("event__full_date"))
    return list_of_events

@login_required(login_url="login")
def dashboard(request):
    if request.method == "GET":
        list_of_days = daysOfWeek(date.today())
        list_of_events = eventsOfWeek(date.today(), Event_User.objects.select_related("event", "participant").filter(participant_id=request.user.id))
        return render(request, "dashboard.html", {"user": request.user, "scheduleDates": list_of_days, "scheduleEvents": list_of_events})
    
    elif request.method == "POST":
        if request.POST.get("email"):
            list_of_days = daysOfWeek(date.today())
            list_of_events = eventsOfWeek(date.today(), Event_User.objects.select_related("event", "participant").filter(participant_id=request.user.id))
            return createUser(request, list_of_days, list_of_events)
        elif request.POST.get("link"):
            return enterEvent(request)
        else:
            return createEvent(request)
#endregion

#region Event (Update)
@login_required(login_url="login")
def updateEvent(request):
    if request.user.id == Event.objects.get(id=request.META['QUERY_STRING']).creator_id:
        if request.method == "GET":
            return render(request, "updateEvent.html", {"event": Event.objects.get(id=request.META['QUERY_STRING'])})
        elif request.method == "POST":
            event = Event.objects.get(id=request.META['QUERY_STRING'])
            event.title = request.POST.get("title") if request.POST.get("title") else event.title
            event.description = request.POST.get("description") if request.POST.get("description") else event.description
            event.full_date = request.POST.get("full_date") if request.POST.get("full_date") else event.full_date
            event.save()
            return redirect("dashboard")
    else:
        return redirect("dashboard")
#endregion

#region Event (Delete)
@login_required(login_url="login")
def deleteEvent(request):
    if request.user.id == Event.objects.get(id=request.META['QUERY_STRING']).creator_id:
        (Event_User.objects.get(event_id = request.META['QUERY_STRING'], participant_id=request.user.id)).delete()
        (Event.objects.get(id=request.META['QUERY_STRING'])).delete()
        return redirect('dashboard')
    else:
        return redirect('dashboard')
#endregion
