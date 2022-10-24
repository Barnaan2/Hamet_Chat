from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from . models import Chat,Message
from account.models import User


# Create your views here.
def index(request):
    users = User.objects.all()
    context = {'users' :users}
    return render(request,"chat/index.html",context)


def chat(request):
    chat= Chat.objects.filter(initiator = request.user) | Chat.objects.filter(reactor = request.user)
    q = request.GET.get("q")
    if q != None:
      user = User.objects.get(id=q)
      if user is None:
         return HttpResponse("user you searching for, does not exist")
      else:
        if Chat.objects.filter(initiator = request.user, reactor = user).exists() or  Chat.objects.filter(reactor = request.user,initiator = user).exists() :
             return redirect('message' ,request.user.id)
        else:
          Chat.objects.create(initiator = request.user, reactor =user)
    context = {'chats': chat}
    return render(request,'chat/your_chat.html',context)

def message(request,q):
    user = User.objects.get(id=q)
    chat = {}
    if user is None:
         return HttpResponse("user you searching for, does not exist")
    else:
        if  Chat.objects.filter(reactor = user).exists() :
             chat = Chat.objects.filter(reactor = user).first()
        elif Chat.objects.filter(initiator=user).exists():
             chat = Chat.objects.filter(initiator = user).first()
         
    messages = Message.objects.filter(chat=chat)
    if request.method == "POST":
        #   receiver = User.objects.get( id=request.POST.get('id'))
          Message.objects.create(chat=chat,sender=request.user, receiver=user,body=request.POST.get('body') )
          username = request.user.username
          name ='{"name":"me"}'
          return HttpResponse(name) 
  
    context = {'messages':messages,'user':user }
    return render(request,'chat/messages.html',context)  

def ajax(request,q):
    user = User.objects.get(id=q)
    chat = {}
    if user is None:
         return HttpResponse("user you searching for, does not exist")
    else:
        if  Chat.objects.filter(reactor = user).exists() :
             chat = Chat.objects.filter(reactor = user).first()
        elif Chat.objects.filter(initiator=user).exists():
             chat = Chat.objects.filter(initiator = user).first()
         
    messages = Message.objects.filter(chat=chat)
    owner = request.user
    print(owner)
    print(user)
    return JsonResponse({"message":list(messages.values())}) 