
from django.http import HttpResponse
from django.shortcuts import render
from . models import Chat,Message
from account.models import User

# Create your views here.
def index(request):
    users = User.objects.all()
    context = {'users' :users}
    return render(request,"chat/index.html",context)


def chat(request):
    chat = Chat.objects.filter(initiator = request.user)
    q = request.GET.get("q")
    if q != None:
      user = User.objects.get(id=q)
      if user is None:
         return HttpResponse("user you searching for, does not exist")
      else:
        Chat.objects.create(initiator = request.user, reactor =user)
    context = {'chat': chat}
    return render(request,'chat/your_chat.html',context)

def Message(request,q):
    user = User.objects.get(id=q)
    chat = {}
    if user is None:
         return HttpResponse("user you searching for, does not exist")
    else:
         reactor = Chat.objects.get(reactor = user) 
         initiator = Chat.objects.get(initiator=user)
   
         if   reactor != None:
             chat = reactor
         elif initiator != None:
            chat = initiator
           
    messages = Message.objects.get(chat=chat)
    if request.method == "POST":
          receiver = User.objects.get( id=request.POST.get('id'))
          Message.objects.create(sender=request.user, receiver=receiver,body=request.POST.get('body') )
          return HttpResponse('the message is sent')
    context = {'messages':messages}
    return render(request,'chat/your_chat.html',context)  
        