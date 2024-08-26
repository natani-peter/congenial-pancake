from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .authentication import TokenAuthentication
from rest_framework import generics, mixins, permissions, status
from core.models import Task
from core.serializers import TaskSerializer, UserSerializer
from rest_framework.decorators import api_view


class TaskGenericApiView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        objects = Task.objects.filter(owner=self.request.user)
        return objects

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


get_task = TaskGenericApiView.as_view()


@api_view(['POST'])
def register(request, *args, **kwargs):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"Message": "User Successfully Created",
                             "token": token.key},
                            status=status.HTTP_201_CREATED)
        return Response({"Message": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update(request, *args, **kwargs):
    queryset = Task.objects.filter(id=kwargs['pk']).first()
    serializer = TaskSerializer(queryset, data=request.data)
    if queryset:
        token = request.headers.get('Authorization').split(" ")[1]
        token_data = Token.objects.get(key=token)
        if queryset.owner.id == token_data.user.id:
            if serializer.is_valid():
                serializer.save(owner=token_data.user)
                return Response(TaskSerializer(queryset, many=False).data, status=status.HTTP_200_OK)
            return Response({"detail": f"Bad Request\n{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
