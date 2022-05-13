from django.urls import path

from . import views
from .views import Order_add,OrderList ,OrderUpdate, OrderDetail

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.orders, name='orders'),
    path('agent/<int:agent_id>', views.agent, name='agent'),
    path('agreementPDF/<int:order_id>', views.agreementPDF, name='agreementPDF'),
    path('agent_add', views.agent_add, name='agent_add'),
    path('order_add', Order_add.as_view(), name="order_add"),
    path('search/', views.search, name='search'),
    path('agent/<int:agent_id>', views.agent, name='agent'),
    path('agent_order_test/<int:agent_id>', views.agent_order_test, name='agent_order_test'),
    path('all_agents', views.all_agents, name='all_agents'),
    path('orders-list/', OrderList.as_view(), name="orders-list"),
    path('order/<int:pk>', OrderDetail.as_view(), name="order"),
    path('order-update/<int:pk>', OrderUpdate.as_view(), name='order-update'),
    path('docx/<int:order_id>', views.generate_docx, name='docx'),



]

