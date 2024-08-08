from django.contrib import admin

from django.contrib.auth.models import Group
from .models import House, Member
from django.db.models import Q

admin.site.unregister(Group)

class MemberInline(admin.StackedInline):
    model = Member
    extra = 1

class HouseAdmin(admin.ModelAdmin):
    inlines = [MemberInline]
    list_filter = ['house_no', 'house_name', 'place']
    search_fields = ['house_no', 'house_name', 'place']
    list_display = ['house_no', 'house_name', 'place', 'contact_number']
    
    class Media:
        css = {
            'all': ('css/custom_admin.css',) 
        }
    
class MemberAdmin(admin.ModelAdmin):
    list_filter = ['first_name', 'last_name', 'marital_status', 'house']
    list_display = ['first_name', 'last_name', 'age', 'marital_status', 'occupation', 'house'] 
    
    def get_search_results(self, request, queryset, search_term):
        # Search by related house name
        if search_term:
            # Try to filter by house ID if the search term is numeric
            try:
                house_id = int(search_term)
                queryset = queryset.filter(
                    Q(first_name__icontains=search_term) |
                    Q(last_name__icontains=search_term) |
                    Q(age__icontains=search_term) |
                    Q(house__house_name__icontains=search_term) |
                    Q(house__house_no__icontains=search_term) |
                    Q(house__id=house_id)  # Filter by house ID
                )
            except ValueError:
                # If the search term is not numeric, skip ID filtering
                queryset = queryset.filter(
                    Q(first_name__icontains=search_term) |
                    Q(last_name__icontains=search_term) |
                    Q(age__icontains=search_term) |
                    Q(house__house_name__icontains=search_term) |
                    Q(house__house_no__icontains=search_term)
                )
        return queryset, False
    
    search_fields = ['first_name', 'last_name', 'age']
    list_filter = ['first_name', 'last_name', 'marital_status', 'house']

admin.site.register(House, HouseAdmin)
admin.site.register(Member, MemberAdmin)