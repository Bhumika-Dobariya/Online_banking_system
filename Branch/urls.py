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
    path('branches/create/', create_branch, name='create_branch'),
    path('branches/<int:id>/', get_branch_by_id, name='get_branch_by_id'),
    path('branches/', get_all_branches, name='get_all_branches'),
    path('branches/update/', update_branch, name='update_branch'),
    path('branches/delete/', delete_branch, name='delete_branch'),
    path('branches/filter_by_name/', filter_branches_by_name, name='filter_branches_by_name'),
    path('branches/by_manager/', get_branches_by_manager, name='get_branches_by_manager'),
    path('branches/by_phone_number/', get_branches_by_phone_number, name='get_branches_by_phone_number'),
    
]
