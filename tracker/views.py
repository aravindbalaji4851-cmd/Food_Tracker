from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from tracker.serializer import UserSerializer,FoodlogSerializer
from tracker.models import Foodlog
from tracker.permissions import IsOwner

from datetime import datetime

class SignUpView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_inst = UserSerializer(data=form_data)

        if serializer_inst.is_valid():

            cleaned_data = serializer_inst.validated_data

            qs = User.objects.create_user(** cleaned_data)

            instance = UserSerializer(qs)

            return Response(data=instance.data)

        else: return Response(data=serializer_inst.errors)


class GetMeView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        qs = User.objects.get(username=request.user)

        serializer = UserSerializer(qs)

        return Response(data=serializer.data)

class FoodlogCreateListView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        qs = Foodlog.objects.filter(owner=request.user)

        serializer = FoodlogSerializer(qs,many=True)

        return Response(serializer.data)

    def post(self,request):

        form_data = request.data

        seralizer = FoodlogSerializer(data=form_data)

        if seralizer.is_valid():

            seralizer.save(owner=request.user)

            return Response(data=seralizer.data)

        else: return Response(data=seralizer.errors)

class FoodlogRetrieveUpdateDeleteView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwner]

    def get(self,request,pk=None):

        qs = get_object_or_404(Foodlog,id=pk)

        self.check_object_permissions(request,qs)

        serializer = FoodlogSerializer(qs)

        return Response(data=serializer.data)

    def put(self,request,pk=None):

        instance = get_object_or_404(Foodlog,id=pk)

        self.check_object_permissions(request,instance)
        
        form_data = request.data

        serializer = FoodlogSerializer(data=form_data,instance=instance)

        if serializer.is_valid():

            serializer.save()

            return Response(data=serializer.data)

        else: return Response(serializer.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(Foodlog,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response({"message":"deleted..."})


class FoodlogSummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        response_data = {
            "todays_total_calorie":0
        }

        current_date = datetime.now().date()

        current_month = datetime.now().month

        current_year = datetime.now().year

        todays_calorie = Foodlog.objects.filter(owner=request.user,created_at__date=current_date)

        if todays_calorie:

            todays_total_calorie = todays_calorie.values("calorie").aggregate(total=Sum("calorie")).get("total")

            todays_category_summary = todays_calorie.values("meal_type").annotate(calorie=Sum("calorie"))

            response_data["todays_total_calorie"] =todays_total_calorie 
            response_data["todays_category_summary"] =todays_category_summary

        monthly_calorie = Foodlog.objects.filter(owner=request.user,created_at__month=current_month,created_at__year=current_year)

        if monthly_calorie:

            monthly_total_calorie = monthly_calorie.values("calorie").aggregate(total=Sum("calorie")).get("total")

            monthly_category_summary = monthly_calorie.values("meal_type").annotate(calorie=Sum("calorie"))

            response_data["monthly_total_calorie"] = monthly_total_calorie

            response_data["monthly_category_summary"] = monthly_category_summary


        return Response(data=response_data)