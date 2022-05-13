from django.contrib import admin

# Register your models here.
from .models import Project, Agent, Manufacturers, Order, EqModels, Types, OrderLine, Equipement




class OrderLineAdmin(admin.TabularInline):
    model = OrderLine

class OrderAdmin(admin.ModelAdmin):
    list_display = ('agent_id', 'id','date_created', 'order_details')
    search_fields = ('id', 'orderlines__sn', 'agent_id__first_name', 'agent_id__last_name', 'agent_id__ccms_id', 'agent_id__email', 'agent_id__phone')
    inlines = [OrderLineAdmin,]



admin.site.register(Project)
admin.site.register(Agent)
admin.site.register(Manufacturers)
admin.site.register(EqModels)
admin.site.register(Types)
admin.site.register(Order,OrderAdmin)
admin.site.register(Equipement)
admin.site.register(OrderLine)

