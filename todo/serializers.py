# TODO_APP

from rest_framework import serializers
from todo.models import ToDoItem, ToDoTag

import json



class ToDoTagSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=30)
    label = serializers.CharField(required=False, allow_blank=True, max_length=30)
    color = serializers.CharField(required=False, allow_blank=True, max_length=30)
    parent = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = ToDoItem
        fields = ('id','name','label','color','parent')


class ToDoItemSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=600)
    start_date = serializers.DateTimeField()
    due_date = serializers.DateTimeField()
    completed = serializers.BooleanField()
    starred = serializers.BooleanField()
    important = serializers.BooleanField()
    deleted = serializers.BooleanField()
    tags = ToDoTagSerializer(many=True, read_only=False) #serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def update(self, instance, validated_data):
        print('HELLO?????')
        print(json.loads(json.dumps(validated_data.get('tags', instance.tags))))

        instance.title = validated_data.get('title', instance.title)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.completed = validated_data.get('completed', instance.completed)

        instance.starred = validated_data.get('starred', instance.starred)
        instance.important = validated_data.get('important', instance.important)
        instance.deleted = validated_data.get('deleted', instance.deleted)
        #instance.tags = validated_data.get('tags', instance.tags)
        print("TAGS:")
        for tag in validated_data.get('tags', instance.tags):
            try:
                tag_obj = ToDoTag.objects.get(name=tag['name'])
            except:
                thisItem = ToDoItem.objects.get(id=instance.id)
                new_tag = ToDoTag(name=tag['name'], label=tag['label'], color=tag['color'], parent=thisItem)
                new_tag.save()

        #instance.tags = json.loads(json.dumps(validated_data.get('tags', instance.tags)))
        instance.save()
        return instance

    class Meta:
        model = ToDoItem
        fields = ('id','title','notes','start_date','due_date','completed','starred','important','deleted','tags')