# TODO_APP
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404
from todo.models import ToDoTag, ToDoItem
from todo.serializers import ToDoItemSerializer, ToDoTagSerializer
from rest_framework import authentication, permissions


"""
class UserDetail(generics.RetrieveAPIView):

    A view that returns a templated HTML representation of a given user.

    queryset = User.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object}, template_name='user_detail.html')
"""


# Create your views here.
class ToDoList(generics.ListAPIView):
    queryset = ToDoItem.objects.all()
    serializer_class = ToDoItemSerializer


class ToDoDetail(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, pk):
        try:
            return ToDoItem.objects.get(pk=pk)
        except ToDoItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = ToDoItemSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        todo = self.get_object(pk)
        print(todo)
        serializer = ToDoItemSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)