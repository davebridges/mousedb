from mousedb.groups.models import Group, License

def group_info(request):
	group = Group.objects.get(pk=1)
	return {'group': group}