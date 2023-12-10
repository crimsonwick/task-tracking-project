from datetime import datetime
from api.views import BaseAPIView
from rest_framework.authentication import TokenAuthentication
from api.permissions import IsOauthAuthenticatedSoftwareEngineer, IsOauthAuthenticatedTeamManager, IsOauthAuthenticatedSuperAdmin
from .serializers import TaskSerializer, StatusSerializer, AssignTaskSerializer
from rest_framework import status
from .models import Status
# ~imports for listing
from api.users.models import User
from api.task.models import Task
from api.users.serializers import UserSerializer
from django.db.models import Q

#Create your views here
'''
class CreateTaskView(BaseAPIView):
    """
    SWE and Team Manager can create a task
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSoftwareEngineer,)

    def post(self, request):
        try:
            if request.user.is_approved:
                taskID = request.user.id

                #~works but Log doesn't update so using StatusSerializer

                taskStatus = request.data.get("status", None)
                tempStatus = Status(current_status=taskStatus)
                tempStatus.created_by = taskID
                tempStatus.save() #~necessary after Django 1.8 for foreign key many-many many-one relations

                serializerTwo = TaskSerializer(data=request.data, context = {'request':request,
                                                                          'status': tempStatus})
                if serializerTwo.is_valid():
                    serializerTwo.save()

                # serializerTwo = TaskSerializer(data=request.data, context = {'request':request,
                #                                                           'status': taskStatus})
                # # if serializerTwo.is_valid():
                #     serializer_data = serializerTwo.data
                #     serializer_data['status'] = taskStatus
                #     serializerOne = StatusSerializer(data=serializer_data, context={'request': request})
                #     if serializerOne.is_valid():
                #         serializerOne.save()

                return self.customResponse(
                    success=True,
                    code=f'200',
                    status_code=status.HTTP_200_OK,
                    payload= serializerTwo.data,
                    description='Task added successfully'
                )
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="Get your account approved from the CEO"
            )
        except Exception as e:
            return self.customResponse(
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )
'''
"""
SWE and Team Manager can create a task
"""

class CreateTaskView(BaseAPIView):
    '''
    swe creates task which is assigned to himself
    '''
    # **always get data in exact format of models structure for POST/PUT reqs imp for serializing
    # assigned_to in Task model make it Foreign Key
    # implement statuses like Roles
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSoftwareEngineer,)

    def post(self, request):
        try:
            if request.user.is_approved:
                # get user obj for this task
                userID = request.user.id
                user = User.objects.get(id=userID)
                # serializedUser = UserSerializer(instance=user)

                # user = serializedUser.data
                # create and get status obj for this task
                currentStatus = request.data.get("status", None)
                if currentStatus in Status.CHOICES:
                    statusObj = Status.objects.create_status(currentStatus)
                    statusObj.created_by = userID
                    statusObj.save()

                    serializer = TaskSerializer(data=request.data, context={"user":user, "status":statusObj})
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return self.customResponse(
                            code=f'422',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            description=serializer.errors
                        )
                    return self.customResponse(
                        success=True,
                        code=f'200',
                        status_code=status.HTTP_200_OK,
                        payload=serializer.data,
                        description='Task added successfully'
                    )

                statusObj = Status.objects.create_status('Pending')
                statusObj.created_by = userID
                statusObj.save()
                serializer = TaskSerializer(data=request.data, context={"user": user, "status": statusObj})
                if serializer.is_valid():
                    serializer.save()
                else:
                    return self.customResponse(
                        code=f'422',
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        description=serializer.errors
                    )

                # serializerTwo = TaskSerializer(data=request.data, context = {'request':request,
                #                                                           'status': taskStatus})
                # if serializerTwo.is_valid():
                #     serializer_data = serializerTwo.data
                #     serializer_data['status'] = taskStatus
                #     serializerOne = StatusSerializer(data=serializer_data, context={'request': request})
                #     if serializerOne.is_valid():
                #         serializerOne.save()

                return self.customResponse(
                    success=True,
                    code=f'200',
                    status_code=status.HTTP_200_OK,
                    payload=serializer.data,
                    description='Task added successfully'
                )
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="Get your account approved from the CEO"
            )
        except User.DoesNotExist:
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='User with this id Does Not Exist'
            )
        except Exception as e:
            return self.customResponse(
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

class CreateAndAssignTaskView(BaseAPIView):
    """
    TM accepts task credentials and id of SWE to assign the task to/ if no assign_to assigns task to self(team manager)
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes =  (IsOauthAuthenticatedTeamManager,)

    def post(self, request):
        try:
            if request.user.is_approved:
                managerID = request.user.id
                taskStatus = request.data.get("status",None)
                assignToID = request.data.get("assign_to", None)
                if assignToID:
                    user = User.objects.get(id=assignToID)
                else:
                    user = User.objects.get(id=managerID)

                # create task status instance
                if taskStatus is None:
                    tempStatus = Status.objects.create_status('Pending')
                    tempStatus.created_by = managerID
                    tempStatus.save()

                    serializer = TaskSerializer(data=request.data, context={'user': user, 'status': tempStatus})
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return self.customResponse(
                            code=f'422',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            description=serializer.errors
                        )
                    return self.customResponse(
                        success=True,
                        code=f'200',
                        status_code=status.HTTP_200_OK,
                        payload=serializer.data,
                        description='Task added successfully'
                    )

                if taskStatus in Status.CHOICES:
                    tempStatus = Status.objects.create_status(taskStatus)
                    tempStatus.created_by = managerID
                    tempStatus.save() # ~necessary after Django 1.8 for foreign key, many-many many-one relations

                    serializer = TaskSerializer(data=request.data, context = {'user':user, 'status': tempStatus})
                    if serializer.is_valid():
                        serializer.save()
                    #     serialized = serializerTwo.initial_data
                    # if assignToID is None:
                    #     serialized['assigned_to'] = managerID
                    # serialized['created_by'] = managerID
                    else:
                        return self.customResponse(
                            code=f'422',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            description=serializer.errors
                        )
                    return self.customResponse(
                        success=True,
                        code=f'200',
                        status_code=status.HTTP_200_OK,
                        payload= serializer.data,
                        description='Task added successfully'
                    )
                return self.customResponse(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=f'{taskStatus} is not a valid status'
                )
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="Get your account approved from the CEO"
            )
        except Exception as e:
            return self.customResponse(
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
        )

class ListingTaskView(BaseAPIView):
    """
    CEO can see the list of all tasks assigned to a employee
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdmin,)

    def get(self, request, pk=None):
        try:
            if pk:
                paramStatus = request.query_params.get("status", None)
                if paramStatus is None:
                    userID = pk
                    taskObj = Task.objects.filter(assigned_to=userID).order_by('-id')
                    serialized = TaskSerializer(taskObj, many=True)
                    tasksData = serialized.data
                    tasksCount = taskObj.count()
                    return self.customResponse(
                        success=True,
                        code=f'200',
                        status_code=status.HTTP_200_OK,
                        payload=tasksData,
                        description=f'Listing of Tasks of User {userID}',
                        count=tasksCount
                    )
                if paramStatus in Status.CHOICES:
                    userID = pk
                    taskObj = Task.objects.filter(assigned_to=userID).order_by('-id')
                    taskObj = Task.objects.filter(status__name=paramStatus)
                    serialized = TaskSerializer(taskObj, many=True)
                    tasksData = serialized.data
                    tasksCount = taskObj.count()
                    return self.customResponse(
                        success=True,
                        code=f'200',
                        status_code=status.HTTP_200_OK,
                        payload=tasksData,
                        description=f'Listing of Tasks of User {userID} with {paramStatus} status',
                        count=tasksCount
                    )
                return self.customResponse(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description='invalid status in query'
                )

            queryset = Task.objects.all().order_by('-id')
            serialized = TaskSerializer(queryset, many=True)
            tasksData = serialized.data
            tasksCount = queryset.count()
            return self.customResponse(
                success=True,
                code=f'200',
                status_code=status.HTTP_200_OK,
                description= 'Listing of Tasks of All Users',
                payload=tasksData,
                count=tasksCount
            )
        except User.DoesNotExist:
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='User with this id Does Not Exist'
            )
        except Exception as e:
            return self.customResponse(
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

class ChangeStatusSweView(BaseAPIView):
    """
    SWE and Team Manager can change task status
    pass taskid and status
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSoftwareEngineer,)

    def post(self, request):
        try:
            if request.user.is_approved:
                # get task obj
                userID = request.user.id
                taskID = request.data.get("task_id", None)
                taskObj = Task.objects.get(id=taskID)

                # get and update status obj for this task
                currentStatus = request.data.get("status", None)
                if currentStatus in Status.CHOICES:
                    statusObj = taskObj.status
                    statusObj.name = currentStatus
                    statusObj.modified_by = userID
                    statusObj.modified_on = datetime.utcnow()
                    statusObj.save()
                # statusSerializer = StatusSerializer(statusObj)
                # serializer = TaskSerializer(instance=statusSerializer.data, data=taskObj)
                # if serializer.is_valid():
                #     serializer.save()
                # else:
                #     return self.customResponse(
                #         code=f'422',
                #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                #         description=serializer.errors
                #     )
                else:
                    return self.customResponse(
                        code=f'422',
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        description=f'{currentStatus} is not a valid status'
                    )

                # serializerTwo = TaskSerializer(data=request.data, context = {'request':request,
                #                                                           'status': taskStatus})
                # if serializerTwo.is_valid():
                #     serializer_data = serializerTwo.data
                #     serializer_data['status'] = taskStatus
                #     serializerOne = StatusSerializer(data=serializer_data, context={'request': request})
                #     if serializerOne.is_valid():
                #         serializerOne.save()

                serializer = TaskSerializer(instance=taskObj)
                return self.customResponse(
                    success=True,
                    code=f'200',
                    status_code=status.HTTP_200_OK,
                    payload=serializer.data,
                    description='Task status updated successfully'
                )
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="Get your account approved from the CEO"
            )
        except Task.DoesNotExist:
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Task with this id Does Not Exist'
            )
        except Exception as e:
            return self.customResponse(
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

class ChangeStatusTmView(BaseAPIView):
    """
    tm can change task status for any swe
    """
    permission_classes = (IsOauthAuthenticatedTeamManager,)
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        try:
            if request.user.is_approved:
                # get task obj
                userID = request.user.id
                taskID = request.data.get("task_id", None)
                taskObj = Task.objects.get(id=taskID)

                # get and update status obj for this task
                currentStatus = request.data.get("status", None)
                if currentStatus in Status.CHOICES:
                    statusObj = taskObj.status
                    statusObj.name = currentStatus
                    statusObj.modified_by = userID
                    statusObj.modified_on = datetime.utcnow()
                    statusObj.save()

                    serializer = TaskSerializer(instance=taskObj)
                    return self.customResponse(
                        success=True,
                        code=f'200',
                        status_code=status.HTTP_200_OK,
                        payload=serializer.data,
                        description='Task status updated successfully'
                    )
                else:
                    return self.customResponse(
                        code=f'422',
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        description=f'{currentStatus} is not a valid status'
                    )
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="Get your account approved from the CEO"
            )
        except Task.DoesNotExist:
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Task with this id Does Not Exist'
            )
        except Exception as e:
            return self.customResponse(
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

class ChangeTimeEstimationTmView(BaseAPIView):
    '''
    tm can change task estimation of any task
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedTeamManager,)

    def post(self, request):
        try:
            if request.user.is_approved:
                userID = request.user.id
                taskID = request.data.get("task_id", None)
                timeEst = request.data.get("time_estimation", None)
                taskObj = Task.objects.get(id=taskID)
                taskObj.time_estimation = timeEst
                taskObj.modified_by = userID
                taskObj.modified_on = datetime.utcnow()
                taskObj.save()

                serialized = TaskSerializer(instance=taskObj)
                return self.customResponse(
                    success=True,
                    code=f'200',
                    status_code=status.HTTP_200_OK,
                    payload=serialized.data,
                    description='Task Time Estimation updated successfully'
                )
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Get your account approved from the CEO'
            )
        except Exception as e:
            return self.customResponse(
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description= str(e)
            )
        except Task.DoesNotExist:
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Task with this id Does Not Exist'
            )