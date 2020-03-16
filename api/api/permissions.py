from rest_framework import permissions
import logging

logger = logging.getLogger('permissions')


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):

        logger.debug("checking the user permissions")


        check_perm = request.user.has_perm(view.permission_code)
        logger.debug("user: %s has permission to permission_code: %s: %s ", request.user, view.permission_code, check_perm)
        return check_perm