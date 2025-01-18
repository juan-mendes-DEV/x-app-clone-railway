from django.shortcuts import render, redirect
from register_e_login.serializers.register_serializer import RegisterSerializer


def register_view(request):
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect("login")
        else:
            errors = serializer.errors
    else:
        serializer = RegisterSerializer()
        errors = {}

    return render(request, "signup.html", {"serializer": serializer, "errors": errors})
