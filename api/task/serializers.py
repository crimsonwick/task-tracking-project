from rest_framework import serializers
from api.task.models import Task, Status
# from api.task.serializers import TaskSerializer


class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    description = serializers.CharField(required=False, allow_blank=True)
    assigned_to = serializers.SerializerMethodField()
    time_estimation = serializers.TimeField(required=False, allow_null=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'assigned_to',
            'time_estimation',
            'status'
        ]

    def create(self, validated_data):
        '''
        # designating task belongs to which user by setting the 'assigned_to' field from context data
        '''

        user = self.context.get("user", None)
        ezStatus = self.context.get("status", None)
        if ezStatus and user:
            validated_data['assigned_to'] = user
            validated_data['status'] = ezStatus
        task = Task.objects.create(**validated_data)
        task.created_by = user.id
        task.assigned_to = user
        task.save()
        return task

    def update(self, instance, validated_data):
        instance.status.name = validated_data.get('name', None)
        instance.modified_by = validated_data.get('modified_by', None)
        instance.modified_on = validated_data.get('modified_on', None)
        instance.assigned_to = validated_data.get('assigned_to', None)
        instance.save()
        return instance

    def get_status(self, obj):
        try:
            return obj.status.name
        except:
            return ''

    def get_assigned_to(self, obj):
        try:
            return obj.assigned_to.id
        except:
            return 0

class AssignTaskSerializer(serializers.ModelSerializer):
    pass

class StatusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    modified_on = serializers.DateTimeField()
    modified_by = serializers.IntegerField()

    class Meta:
        model = Status
        fields = [
            'id',
            'name',
            'modified_on',
            'modified_by'
        ]
        # extra_kwargs = {'current_status': {'required': False}}

    # def create(self, validated_data):
    #     """
    #     whenever task creates we create status for it (& update Log attribute created_by)
    #     """
    #     user_id = self.context['request'].user.id
    #     status_data = validated_data.pop('current_status', None)
    #     if status_data is None:
    #         status_data = Status.STATUS_PENDING_CODE
    #     for i in range(len(Status.CHOICES)):
    #         if status_data in Status.CHOICES[i]:
    #             status = Status.objects.create(**validated_data)
    #             status.created_by = user_id
    #             status.save()
    #             break
    #     return status
    #
    # def update(self, instance, validated_data):
    #     """
    #     whenever task status updates we update Log attribute updated_by
    #     """
    #     userID = self.context['request'].user.id
    #     instance.updated_by = userID
    #     instance.current_status = validated_data.get("status", instance.current_status)
    #     instance.save()
    #
    #     return instance
