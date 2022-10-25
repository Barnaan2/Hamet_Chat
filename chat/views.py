from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from . models import Chat,Message
from account.models import User


# Create your views here.
def index(request):
    users = User.objects.all()
    context = {'users' :users}
    return render(request,"chat/index.html",context)

@login_required(login_url='login')
def chat(request):
    chat= Chat.objects.filter(initiator = request.user) | Chat.objects.filter(reactor = request.user)
    q = request.GET.get("q")
    if q != None:
      user = User.objects.get(id=q)
      if user is None:
         return HttpResponse("user you searching for, does not exist")
      elif user == request.user:
          return HttpResponse(" error 10000007x you cannot chat with your self dude :)")
      else:
        if Chat.objects.filter(initiator = request.user, reactor = user).exists() or  Chat.objects.filter(reactor = request.user,initiator = user).exists() :
             return redirect('message' ,user.id)
        else:
          Chat.objects.create(initiator = request.user, reactor =user)
          return redirect('message' ,user.id)
    context = {'chats': chat}
    return render(request,'chat/your_chat.html',context)

@login_required(login_url='login')
def message(request,q):
    user = User.objects.get(id=q)
    chat = {}
    if user is None:
         return HttpResponse("user you searching for, does not exist")
    else:
        chat= Chat.objects.filter(initiator = request.user) & Chat.objects.filter(reactor = user) |  Chat.objects.filter(initiator = user) | Chat.objects.filter(reactor = request.user);
        chat = chat.first()
    messages = Message.objects.filter(chat=chat)
    if request.method == "POST":
          Message.objects.create(chat=chat,sender=request.user, receiver=user,body=request.POST.get('body') )
         
  
    context = {'messages':messages,'user':user }
    return render(request,'chat/messages.html',context)  


@login_required(login_url='login')
def ajax(request,q):
    user = User.objects.get(id=q)
    chat = {}
    if user is None:
         return HttpResponse("user you searching for, does not exist")
    else:
        chat= Chat.objects.filter(initiator = request.user) & Chat.objects.filter(reactor = user) |  Chat.objects.filter(initiator = user) | Chat.objects.filter(reactor = request.user);
        chat = chat.first() 
        users = User.objects.filter(id=user.id) | User.objects.filter(id=request.user.id)
        print(users)
    messages = Message.objects.filter(chat=chat)
    return JsonResponse({"message":list(messages.values()),"users":list(users.values()),"owner_id":request.user.id}) 