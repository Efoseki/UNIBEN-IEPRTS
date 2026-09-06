def ieprts_access(request):
    user=request.user
    can_manage=False
    if getattr(user,'is_authenticated',False):
        can_manage=bool(user.is_staff or user.is_superuser)
        if not can_manage:
            try:
                can_manage=user.profile.role in {'officer','management','admin'}
            except Exception:
                can_manage=False
    return {'can_manage_reports':can_manage}
