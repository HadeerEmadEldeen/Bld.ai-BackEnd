from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from rest_framework import status
import json , uuid , os
from .forms import nameValidation , descriptionValidation
path_json = os.path.join(os.getcwd(), 'course/db.json')

def getCourses():
    data = open(path_json, "r")
    obj  = json.load(data)["courses"]
    data.close()
    return obj

def courseShape(body):
    return {
        "id": str(uuid.uuid1()),
        "title": body["title"],
        "subTitle": body["subTitle"],
        "description": body["description"],
        "image": body["image"],
        "price": body["price"],
    }


# Get , Create , Update , delete -> for only one course 
class oneCourse(View):
    #Get
    def get(self, request, *args, **kwargs):
        obj = getCourses()
        id = kwargs["id"]
        if id in obj:
            return JsonResponse(data=obj[id])
        return JsonResponse(data={"result": "404 not found"}, status=status.HTTP_404_NOT_FOUND)

    #Updates
    def put(self, request, *args, **kwargs):
        obj = getCourses()
        id = kwargs["id"]
        if id  in obj:
            data = open(path_json, "w")
            body_decode = request.body.decode('utf-8')
            body = json.loads(body_decode)
            courseForUpdate = obj[id]
            for key in body:
                if key in courseForUpdate:
                    courseForUpdate[key] = body[key]
            obj[id] = courseForUpdate
            json.dump({"courses": obj}, data)
            data.close()
            return JsonResponse(data={"result": "updated"} )
        return JsonResponse(data={"result": "404 not found"}, status=status.HTTP_404_NOT_FOUND)

    #delete
    def delete(self, request, *args, **kwargs):
        obj = getCourses()
        id = kwargs["id"]
        if id in obj:
            obj.pop(id)
            data = open(path_json, "w")
            json.dump({"courses": obj}, data)
            data.close()
            return JsonResponse(data={"result": "deleted"}, status=status.HTTP_200_OK)
        return JsonResponse(data={"result": "404 not found"}, status=status.HTTP_404_NOT_FOUND)

    #Create
    def post(self, request, *args, **kwargs):
        obj = getCourses()
        body_decode = request.body.decode('utf-8')
        body = json.loads(body_decode)
        name = body['name']
        description = body['description']
        nametCheck = nameValidation({"name": name})
        discraptionCheck = descriptionValidation({"description": description})

        if nametCheck.is_valid():
            if discraptionCheck.is_valid():
                data = open(path_json, "w")
                newcourseShape = courseShape(body)
                obj[newcourseShape["id"]] = newcourseShape
                json.dump({"courses": obj}, data)
                data.close()
                return JsonResponse(data={"result": "created"}, status=status.HTTP_201_CREATED)
       

# Get ->for all courses
class Courses (View):
    #Get
    def get(self, request, *args, **kwargs):
        obj = getCourses()
        return JsonResponse(data = obj)
     
    


