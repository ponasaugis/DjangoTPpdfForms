from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .models import Project, Agent, Manufacturers, EqModels, Equipement, Types, OrderLine, Order
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import *
from django.forms import inlineformset_factory, modelformset_factory
from django.views.generic import UpdateView, ListView, CreateView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from docxtpl import DocxTemplate
from django.contrib.auth.models import User


def index(request):
    num_orders = Order.objects.all().count()
    num_projects = Project.objects.all().count()
    num_agents = Agent.objects.all().count()

    context = {
        'num_orders': num_orders,
        'num_projects': num_projects,
        'num_agents': num_agents,
    }

    return render(request, 'index.html', context=context)


@login_required(login_url='/accounts/login/')
def orders(request):
    all_orders = Order.objects.all()

    context = {
        'all_orders': all_orders,
    }

    return render(request, 'orders.html', context=context)


@login_required(login_url='/accounts/login/')
def agent(request, agent_id):
    single_agent = get_object_or_404(Agent, pk=agent_id)
    return render(request, 'agent.html', {'agent': single_agent})



@login_required(login_url='/accounts/login/')
def agent_add(request):
    submitted = False
    if request.method == 'POST':
        form = AgentAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/facility/agent_add?submitted=True')
    else:
        form = AgentAddForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'agent_add.html', {'form': form, 'submitted': submitted})


# ---------------------------------------------------------------------

@login_required(login_url='/accounts/login/')
def search(request):
    query = request.GET.get('query')
    search_results = Order.objects.filter(Q(agent_id__first_name__icontains=query) | Q(agent_id__last_name__icontains=query) | Q(agent_id__ccms_id__icontains=query) | Q(agent_id__project_id__project_name__icontains=query))
    return render(request, 'search.html', {'orders': search_results, 'query': query})


# ----------------------------------------------------------------------

class Order_add(CreateView):
    form_class = OrderForm
    template_name = 'order_add.html'

    def get_context_data(self, **kwargs):
        context = super(Order_add, self).get_context_data(**kwargs)
        context['order_line_meta_formset'] = OrderMetaInLineFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        order_line_meta_formset = OrderMetaInLineFormset(self.request.POST)
        if form.is_valid() and order_line_meta_formset.is_valid():
            return self.form_valid(form, order_line_meta_formset)
        else:
            return self.form_invalid(form, order_line_meta_formset)

    def form_valid(self, form, order_line_meta_formset):
        self.object = form.save(commit=False)
        self.object.save()
        # saving ProductMeta Instances
        order_line_metas = order_line_meta_formset.save(commit=False)
        for meta in order_line_metas:
            meta.order_id = self.object
            meta.save()

        return redirect(reverse("order_add"))

    def form_invalid(self, form, order_line_meta_formset):
        return self.render_to_response(
            self.get_context_data(form=form, order_line_meta_formset=order_line_meta_formset))


# -------------------------------------------------------------------------
def add_order_test(request):
    agents = Agent.objects.all()
    context = {
        'agents': agents,
    }

    return render(request, 'add_order_test.html', context=context)


def agent_order_test(request, agent_id):
    single_agent = get_object_or_404(Agent, pk=agent_id)

    TestFormSet = inlineformdeset_factory(Orr, OrderLine, fields=('order_id', 'equipement_id', 'sn'),
                                          widgets={'equipement_id': forms.Select(attrs={'class': 'form-control'}), })

    form = TestFormSet()

    return render(request, 'agent_order_test.html', {'agent': single_agent, 'form': form, })


def all_agents(request):
    all_agents = Agent.objects.all

    context = {
        'all_agents': all_agents,
    }

    return render(request, 'all_agents.html', context=context)


# Clas based lists-----------------------------------------------------

class OrderList(ListView):
    model = Order
    fields = '__all__'
    context_object_name = 'orders'
    template_name = 'orders-list.html'


class OrderDetail(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders-detail.html'


class OrderUpdate(UpdateView):
    model = Order
    template_name = 'order-update.html'
    form_class = OrderInlineUpdateFormset
    def get_success_url(self):
        orderid = self.kwargs['pk']
        return reverse_lazy('order', kwargs={'pk': orderid})


def agreementPDF(request, order_id):
    single_agent = get_object_or_404(Order, pk=order_id)
    template_path = 'agreementPDF.html'
    context = {'single_agent': single_agent}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, encoding='UTF-8', dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def generate_docx(request, order_id):
    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename="generated_document.docx"'
    doc = DocxTemplate('C:/Users/Augis/Desktop/VIGI/BackEnd/DjangoTPpdfForms/TP/facility/static/Document.docx')

    issuer = User.get_full_name(request.user)
    order = Order.objects.filter(id=order_id)
    order_id = ''
    date = datetime.today().strftime('%Y-%m-%d')
    first_name = ''
    last_name = ''
    ccms_id = ''
    phone = ''
    email = ''
    country = ''
    city = ''
    street = ''
    project_id = ''
    total = ''
    totalVat = ''
    totalWithoutVat = ''
    manufacturer = []
    price = []
    for x in order:
        order_id = (str(x.id))
        first_name = (x.agent_id.first_name)
        last_name = (x.agent_id.last_name)
        ccms_id = (x.agent_id.ccms_id)
        phone = (x.agent_id.phone)
        email = (x.agent_id.email)
        country = (x.agent_id.country)
        city = (x.agent_id.city)
        street = (x.agent_id.street)
        project_id = (x.agent_id.project_id)
        total = (str(x.total))
        totalVat = (str(x.totalVat))
        totalWithoutVat = (str(x.totalWithoutVat))

        for order_line in x.orderlines.all():
            manufacturer.append(order_line.equipement_id.types_id.type + ', '+ order_line.equipement_id.manufacturer_id.manufacturer + ' ' + order_line.equipement_id.eqModels_id.eq_model + ', SN:' + order_line.sn)
            price.append(str(order_line.equipement_id.price))

        while len(manufacturer) <= 8:
            manufacturer.append('')
            pass

        while len(price) <= 8:
            price.append('')
            pass



    context = {
        'order_id': order_id,
        'date': date,
        'first_name' : first_name,
        'last_name' : last_name,
        'ccms_id' : ccms_id,
        'phone' : phone,
        'email' : email,
        'country' : country,
        'city' : city,
        'street' : street,
        'project_id' : project_id,
        'total' : total,
        'totalVat' : totalVat,
        'totalWithoutVat' : totalWithoutVat,
        'manufacturer': manufacturer,
        'manufacturer1': manufacturer[0],
        'manufacturer2': manufacturer[1],
        'manufacturer3': manufacturer[2],
        'manufacturer4': manufacturer[3],
        'manufacturer5': manufacturer[4],
        'manufacturer6': manufacturer[5],
        'manufacturer6': manufacturer[6],
        'manufacturer6': manufacturer[7],
        'manufacturer6': manufacturer[8],
        'price1' : price[0],
        'price2' : price[1],
        'price3': price[2],
        'price4': price[3],
        'price5': price[4],
        'price6': price[5],
        'price6': price[6],
        'price6': price[7],
        'price6': price[8],
        'issuer': issuer,
    }

    doc.render(context)
    doc.save(response)

    return response