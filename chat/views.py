
from django.http import HttpResponse
from django.shortcuts import render
from . models import Chat,Message
from account.models import User

# Create your views here.
def index(request):

    return render(request,"chat/index.html")


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