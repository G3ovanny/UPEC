from rest_framework import permissions

class IsInGroupPermission(permissions.BasePermission):

    def __init__(self, group_name):
        self.group_name = group_name

    def has_permission(self, request, view):
        user = request.user
        return user.groups.filter(name=self.group_name).exists()