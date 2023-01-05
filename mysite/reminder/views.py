from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import * 
import json
from django.http import JsonResponse
from reminder.log import loglib
import mimetypes
import os
from os.path import exists

app_title = "REMINDER"

@login_required(redirect_field_name="next",login_url='login_form')
def view_test(request):
   return render(request,"reminder/test.html")

@login_required(redirect_field_name="next",login_url='login_form')
def view_reminder(request):
   machines = []
   user = request.user
   #get the list of machine user interest
   user_mac_list =  user_mac.objects.filter(user = user).values()
   mac_id_list = list(i["machine_id"] for i in user_mac_list)

   machine_query = MachineStatus.objects.filter(macId__in = mac_id_list)
   
   #list of type
   type_list = list(set(i["macType_id"] for i in machine_query.values("macType_id")))
   
   #get machine follow type
   for macType in type_list:
      macs = list(machine_query.filter(macType_id = macType).values())
      # print(macs)
      mac_with_type = {"mac":macs,"type":macType} 
      machines.append(mac_with_type)
   context = {'machines': machines,'title':app_title}
   return render(request, 'reminder/reminder.html', context)

@login_required(redirect_field_name="next",login_url='login_form')
def view_userAddMachine(request):
   user = request.user
   query = user_mac.objects.filter(user = user).values()
   mac_user_have_list = list(i["machine_id"] for i in query)
   filter = []
   if(request.method == "GET"):
      query = MachineStatus.objects.filter().values()
   elif(request.method == "POST"):
      if(request.POST.get('have_filter') == "on"):
         postDict = request.POST.dict()
         # print(postDict)
         filter = [i for i in postDict if postDict[i]=="filter"]
         print((filter))
         query = MachineStatus.objects.filter(macType__macType__in = filter).values()
      else:
         query = MachineStatus.objects.filter().values()
   context = {'title':'User add mac'}
   mac_all_list = list(i["macId"] for i in query)
   print(mac_all_list)
   mac_user_dont_have_list = list(set(mac_all_list) - set(mac_user_have_list))
   mac_user_have_list = list(MachineStatus.objects.filter(macId__in = mac_user_have_list).values('macId','macType','line','model'))
   mac_user_dont_have_list =  list(MachineStatus.objects.filter(macId__in = mac_user_dont_have_list).values('macId','macType','line','model'))
   context.update({'mac_dont_have':mac_user_dont_have_list,'mac_have':mac_user_have_list})

   context.update({'current_filter':filter})
   all_mac_type_list = MachineType.objects.filter().values()
   context.update({'all_mac_type_list':all_mac_type_list})

   return render(request,'reminder/UserAddMachine.html',context)

@csrf_exempt
@login_required(redirect_field_name="next",login_url='login_form')
def view_logSystem(request):
   if(request.method=="GET"):
      user = request.user
      query = user_mac.objects.filter(user = user).values()
      mac_user_have_list = list(i["machine_id"] for i in query)
      context={'title':"Log system"}
      context.update({"mac_have":mac_user_have_list}) 
      print(context)
      return render(request,'reminder/logSystem.html',context)
   else:
      return HttpResponseBadRequest()

# API
@csrf_exempt
@login_required(redirect_field_name="next",login_url='login_form')
def getMachineStatus_multi(request):
   if(request.method == "POST"):
      data = request.body.decode('utf-8')
      data = json.loads(data)
      if(data["request_type"]=="getmulti"):
         list_id = data["list_id"]
         machines = MachineStatus.objects.filter(macId__in = list_id).values("macId","status","buildConfig","lotId","curDetail","sw")
         machines = list(machines)
         return JsonResponse(machines, safe=False)
   return JsonResponse({"error": ""}, status=400)

@csrf_exempt
@login_required(redirect_field_name="next",login_url='login_form')
def updateMachineStatus(request):
   if (request.method == 'POST'):
      data = request.body.decode('utf-8')
      data = json.loads(data)
      macId = data[0]["macId"]
      status = int(data[0]["status"])
      buildConfig = data[0]["buildConfig"]
      lotId = data[0]["lotId"]
      curDetail = data[0]["curDetail"]
      sw = data[0]["sw"]

      machine = MachineStatus.objects.get(macId=macId)
      machine.status = status
      machine.buildConfig = buildConfig
      machine.lotId = lotId
      machine.curDetail = curDetail
      machine.sw = sw
      machine.save()

      loglib.write_log(machine,request.user)
      
      return JsonResponse(data, safe=False)
   return JsonResponse({"error": ""}, status=400)

@csrf_exempt
@login_required(redirect_field_name="next",login_url='login_form')
def userAddMachineInterest(request):
   if (request.method == 'POST'):
      user = request.user
      user_intance = (User.objects.filter(username=user)[0])
      # print(user)

      data = request.body.decode('utf-8')
      data = json.loads(data)
      if("listMac" in data ):
         listMac = data["listMac"]
         if(len(listMac)<=0):
            return JsonResponse({"error": "expect list have more than zero"}, status=400)
         for mac in listMac:
            query = MachineStatus.objects.filter(macId=mac)
            if(len(query)):
               mac_intance = query[0]
               newUserMac = user_mac(id=None,machine=mac_intance,user=user_intance)
               newUserMac.save()
         return HttpResponse("ok")
      else:
         return JsonResponse({"error": "wrong data format"}, status=400)

   return JsonResponse({"error": "expect POST request"}, status=400)


@csrf_exempt
@login_required(redirect_field_name="next",login_url='login_form')
def userDeleteMachineInterest(request):
   if (request.method == 'POST'):
      user = request.user
      user_intance = (User.objects.filter(username=user)[0])
      # print(user)

      data = request.body.decode('utf-8')
      data = json.loads(data)
      if("listMac" in data ):
         listMac = data["listMac"]
         if(len(listMac)<=0):
            return JsonResponse({"error": "expect list have more than zero"}, status=400)
         for mac in listMac:
            query = user_mac.objects.filter(machine=mac,user=user_intance)
            if(len(query)):
               query[0].delete()
         return HttpResponse("ok")
      else:
         return JsonResponse({"error": "wrong data format"}, status=400)

   return JsonResponse({"error": "expect POST request"}, status=400)

@csrf_exempt
@login_required(redirect_field_name="next",login_url='login_form')
def downloadMachineLog(request):
   if(request.method == "GET"):
      fileName = request.GET.get('fileName')
      BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
      filePath = BASE_DIR+"\\reminder\\log\\"+fileName
      file_is_exists = exists(filePath)
      print(filePath)
      if(file_is_exists):
         with open(filePath,'r',encoding='utf-8') as file:
            mime_type,_ = mimetypes.guess_type(filePath)
            response = HttpResponse(file,content_type = mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % fileName
         return response
      else:
         return HttpResponse("This log is not exists")
   else:
      return HttpResponse("Error")

@csrf_exempt
@login_required(redirect_field_name="next",login_url='login_form')
def create_machine(request):
   if request.method == 'POST':
      try:
         # Get the form data
         mac_id = request.POST.get('macId')
         mac_type = request.POST.get('macType')
         line = request.POST.get('line')
         model = request.POST.get('model')

         mac_type_intance = MachineType.objects.filter(macType=mac_type)[0]

         # Create the machine object with the provided properties
         machine = MachineStatus.objects.create(
            macId=mac_id,
            macType=mac_type_intance,
            line=line,
            model=model
         )
         context = {'title':'Create machine','message_ok':'Machine have been created'}
      except Exception as e:
         error = "error:"+str(e)
         context = {'title':'Create machine','message_fail':error}
      # Redirect to a success page
      return render(request, 'reminder/createNewMachine.html', context)

   # If the request is not a POST request, render the form template
   return render(request, 'reminder/createNewMachine.html')