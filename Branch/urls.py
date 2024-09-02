# urls.py
from django.urls import path
from .views import (
    create_branch,
    get_branch_by_id,
    get_all_branches,
    update_branch,
    delete_branch,
    filter_branches_by_name,
    get_branches_by_manager,
    get_branches_by_phone_number,

)

urlpatterns = [
    path('create_branch/', create_branch, name='create_branch'),
    path('get_branch_by_id/', get_branch_by_id, name='get_branch_by_id'),
    path('get_all_branches/', get_all_branches, name='get_all_branches'),
    path('update_branch/', update_branch, name='update_branch'),
    path('delete_branch/', delete_branch, name='delete_branch'),
    path('filter_branches_by_name/', filter_branches_by_name, name='filter_branches_by_name'),
    path('get_branches_by_manager/', get_branches_by_manager, name='get_branches_by_manager'),
    path('get_branches_by_phone_number/', get_branches_by_phone_number, name='get_branches_by_phone_number'),
    
]
