from datetime import date

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import Subject, Group, Expense
from .serializers import SubjectSerializer, GroupSerializer, ExpenseSerializer
from .decorators import is_authenticated, is_superuser


class SubjectViewSet(viewsets.ViewSet):
    """ ViewSet to handle CRUD operations for subjects """

    serializer_class = SubjectSerializer

    def get_object(self, pk):
        """ Helper function to retrieve a specific object or raise 404 """
        try:
            return Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            raise Http404('Not found')

    @is_authenticated
    def list(self, request):
        queryset = Subject.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @is_authenticated
    @is_superuser
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @is_authenticated
    def retrieve(self, request, pk=None, format=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @is_authenticated
    @is_superuser
    def update(self, request, pk=None, format=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @is_authenticated
    @is_superuser
    def partial_update(self, request, pk=None, format=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(data=request.data, instance=instance, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @is_authenticated
    @is_superuser
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ViewSet):
    """ ViewSet to handle CRUD operations for groups """

    serializer_class = GroupSerializer

    def get_object(self, pk, strict=False):
        """ Helper function to retrieve a specific object or raise 404 """

        try:
            if strict:
                return self.request.user.group_set.get(id=pk)
            else:
                return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404('Not found')

    @is_authenticated
    def list(self, request):
        if request.user.is_superuser:
            queryset = Group.objects.all()
        else:
            queryset = Group.objects.filter(teacher=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @is_authenticated
    def retrieve(self, request, pk=None):
        if request.user.is_superuser:
            instance = self.get_object(pk)
        else:
            instance = self.get_object(pk, strict=True)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @is_authenticated
    @is_superuser
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @is_authenticated
    @is_superuser
    def update(self, request, pk=None):
        instance = self.get_object(pk)

        if instance.price >= float(request.data.get('price', 0)):
            return Response({'error': 'Price cannot be less than or equal to initial amount'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @is_authenticated
    @is_superuser
    def partial_update(self, request, pk=None):
        instance = self.get_object(pk)

        if instance.price >= request.data.get('price', 0):
            return Response({'error': 'Price cannot be less than or equal to initial amount'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data, instance=instance, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @is_authenticated
    @is_superuser
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenseViewSet(viewsets.ViewSet):
    """ ViewSet to handle CRUD operations for expenses """

    serializer_class = ExpenseSerializer

    def get_object(self, pk, strict=False):
        """ Helper function to retrieve a specific object or raise 404 """

        try:
            if strict:
                return self.request.user.expense_set.get(id=pk)
            else:
                return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            raise Http404('Not found')

    @is_authenticated
    def list(self, request):
        if request.user.is_superuser:
            queryset = Expense.objects.all()
        else:
            queryset = Expense.objects.filter(owner=request.user, created__year__exact=date.today().year,
                                              created__month__exact=date.today().month)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @is_authenticated
    def retrieve(self, request, pk=None):
        if request.user.is_superuser:
            instance = self.get_object(pk)
        else:
            instance = self.get_object(pk, strict=True)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @is_authenticated
    def create(self, request):
        # Initializing data coming from frontend
        data = request.data.copy()

        # Updating depending on user status
        # Superuser can create expense for any user
        if request.user.is_superuser:
            owner = request.data.get('owner')
            if not owner:
                return Response({'error': 'Owner field is required'}, status=status.HTTP_400_BAD_REQUEST)
            data['owner'] = owner
        else:
            # User can create expense only for himself
            data['owner'] = request.user.id

        print(data)
        serializer = ExpenseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @is_authenticated
    @is_superuser
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
