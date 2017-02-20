# TODO_APP
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404
from todo.models import ToDoTag, ToDoItem
from todo.serializers import ToDoItemSerializer, ToDoTagSerializer, ToDoItemSerializer2
from rest_framework import authentication, permissions
from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser



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
    def get(self, request, format=None):
        queryset = ToDoItem.objects.all()
        serializer = ToDoItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        #serializer = ToDoItemSerializer(data=request.data)
        print("SELF REQUEST USER2: ")

        content = JSONRenderer().render(request.data)

        stream = BytesIO(content)
        data = JSONParser().parse(stream)

        serializer2 = ToDoItemSerializer2(data=data)
        #serializer3 = ToDoTagSerializer()




        if serializer2.is_valid():
            serializer2.save()
            print('Tags:')
            print(serializer2.data)
            i = 0
            for item in request.data['tags']:
                tag_content = JSONRenderer().render(item)
                stream_tag = BytesIO(tag_content)
                data_tag = JSONParser().parse(stream_tag)
                print(serializer2.initial_data['tags'][i])
                print(tag_content)
                print(item['id'])
                print('TOTAL TODO ITEMS: ' + str(ToDoItem.objects.count()))
                parent = ToDoItem.objects.get(id=ToDoItem.objects.count())
                new_tag = ToDoTag(name=item['name'], color=item['color'], parent=parent,
                                  label=item['label'])
                new_tag.save()

                i += 1
            return Response(serializer2.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)


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