from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Branch
from .serializers import BranchSerializer

# _____________ Create Branch ___________________

@api_view(["POST"])
def create_branch(request):
    serializer = BranchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# _____________ Get Branch by ID ___________________

@api_view(["GET"])
def get_branch_by_id(request):
    branch_id = request.query_params.get('id')
    if not branch_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    branch = get_object_or_404(Branch, pk=branch_id)
    serializer = BranchSerializer(branch)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Get All Branches ___________________

@api_view(["GET"])
def get_all_branches(request):
    branches = Branch.objects.all()
    serializer = BranchSerializer(branches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Update Branch ___________________

@api_view(["PUT"])
def update_branch(request):
    branch_id = request.query_params.get('id')
    if not branch_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    branch = get_object_or_404(Branch, pk=branch_id)
    serializer = BranchSerializer(branch, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# _____________ Delete Branch ___________________

@api_view(["DELETE"])
def delete_branch(request):
    branch_id = request.query_params.get('id')
    if not branch_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    branch = get_object_or_404(Branch, pk=branch_id)
    branch.delete()
    return Response({"detail": "Branch deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



# _____________ Filter Branches by Name ___________________

@api_view(["GET"])
def filter_branches_by_name(request):
    name = request.query_params.get('name')
    if name:
        branches = Branch.objects.filter(name__icontains=name)
    else:
        branches = Branch.objects.all()
    
    serializer = BranchSerializer(branches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Get Branches by Manager ___________________

@api_view(["GET"])
def get_branches_by_manager(request):
    manager_name = request.query_params.get('manager_name')
    if not manager_name:
        return Response({"detail": "Manager name query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    branches = Branch.objects.filter(manager_name__icontains=manager_name)
    serializer = BranchSerializer(branches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#_______________ get branches by phone number________________
@api_view(["GET"])
def get_branches_by_phone_number(request):
    phone_number = request.query_params.get('phone_number')
    if phone_number:
        branches = Branch.objects.filter(phone_number=phone_number)
    else:
        branches = Branch.objects.all()
    
    serializer = BranchSerializer(branches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
