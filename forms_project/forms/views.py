from django.shortcuts import render
from .models import User,Room,Options,Questions,Voters
import json
from . import formscraper
from django.http import JsonResponse
user_name=""
room_name_x = ""
room_password_x = ""
def home(request):
    context = {
        "is_true":True
    }
    return render(request,"forms/home.html")
def join_room(request):
    name = request.POST["name"]
    global user_name
    user_name = name
    password = request.POST["password"]
    if User.objects.filter(name=name).exists():
        real_password = ""
        for user in User.objects.filter(name=name):
            real_password = user.password
        if real_password != password:
            context = {
                "is_true":False,
                "short_pass":False
            }
            return render(request,"forms/home.html",context)
        else:
            
            return render(request,"forms/join_room.html")
    else:
        if len(password) < 4:
            context = {
                "is_true":True,
                "short_pass":True
            }
            return render(request,"forms/home.html",context)
        User.objects.create(name=name,password=password)
        return render(request,"forms/join_room.html")


def room_url(request):
    room_name = request.POST["room_name"]
    password = request.POST["room_password"]
    print("the password is " + password)
    
    if Room.objects.filter(room_name=room_name).exists():
        url = ""
        for room in Room.objects.filter(room_name=room_name):
            url = Room.url
            real_password = ""
            for pas in Room.objects.filter(room_name=room_name):
                real_password = pas.room_password
            
        if real_password != password:
            context = {
                "is_true":False,
                "short_pass":True,
                "short_name":True
            }
            return render(request,"forms/join_room.html",context)
        else:
            questions_list = []
            options_list = []
            votes_list = []
            option_id_list = []
            for question in Questions.objects.filter(room=room_name):
                questions_list.append(question.question)
                sub_option = []
                sub_votes = []
                sub_id = []
                for option in Options.objects.filter(question=question.question,room_name=room_name):
                    sub_option.append(option.option)
                    sub_votes.append(option.votes)
                    sub_id.append(option.id)
                options_list.append(sub_option)
                votes_list.append(sub_votes)
                option_id_list.append(sub_id)
            print("the id list is is:")
            print(option_id_list)

            zipped_list = zip(votes_list,options_list,questions_list)
            context = {
                "zipped_list": zipped_list,
                "room_name":room_name
            }
            return render(request,"forms/display_room.html",context)
    else:
        context = {
            "room_name":room_name,
            "room_password":password,

        }
        return render(request,"forms/room_url.html",context)


def display_room(request):
    global user_name
    room_name = request.POST["room_name"]
    room_password = request.POST["room_password"]
    room_url = request.POST["url"]
    
    

    Room.objects.create(room_name=room_name, room_password=room_password,url=room_url)
    ques_ans_dict = formscraper.ques_dict(room_url)
    
    options_list = []
    votes_list = []
    questions_list = []
    option_id_list = []
    for question in ques_ans_dict:
        sub_option = []
        sub_vote = []
        sub_id = []
        questions_list.append(question)
        for option in ques_ans_dict[question]:
            Options.objects.create(option=option, question=question,votes=0,room_name=room_name)
            sub_option.append(option)
            sub_vote.append(0)
            for option in Options.objects.filter(option=option, question=question, room_name=room_name):
                sub_id.append(option.id)
            
        options_list.append(sub_option)
        votes_list.append(sub_vote)
        option_id_list.append(sub_id)
        Questions.objects.create(question=question, room=room_name)
    context = {
        "show_message":True,
    }
    return render(request, 'forms/join_room.html',context)
    # print(option_id_list)
    # zipped_list = zip(votes_list,options_list,questions_list)



    # context = {
    #     "ques_ans_dict":ques_ans_dict,
    #     "zipped_list":zipped_list,
    #     "username":user_name,
    #     "room_name":room_name
    # }
    # return render(request, 'forms/display_room.html',context)




def vote_option(request):
    option = json.loads(request.body)
    id = option['id']
    print(id)
    option = Options.objects.filter(id=id)[0]
    print(option.votes)
    option.votes += 1
    print(option.votes)
    option.save()
    return JsonResponse({})