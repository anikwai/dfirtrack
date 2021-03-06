from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import CaseForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Case

class CaseList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Case
    template_name = 'dfirtrack_main/case/cases_list.html'
    context_object_name = 'case_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " CASE_LIST_ENTERED")
        return Case.objects.order_by('case_name')

class CaseDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Case
    template_name = 'dfirtrack_main/case/cases_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case = self.object
        case.logger(str(self.request.user), " CASE_DETAIL_ENTERED")
        return context

class CaseCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Case
    form_class = CaseForm
    template_name = 'dfirtrack_main/case/cases_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " CASES_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.case_created_by_user_id = request.user
            case.save()
            case.logger(str(request.user), " CASES_ADD_EXECUTED")
            messages.success(request, 'Case added')
            return redirect('/cases/' + str(case.case_id))
        else:
            return render(request, self.template_name, {'form': form})

class CaseUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Case
    form_class = CaseForm
    template_name = 'dfirtrack_main/case/cases_edit.html'

    def get(self, request, *args, **kwargs):
        case = self.get_object()
        form = self.form_class(instance=case)
        case.logger(str(request.user), " CASES_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        case = self.get_object()
        form = self.form_class(request.POST, instance=case)
        if form.is_valid():
            case = form.save(commit=False)
            case.case_created_by_user_id = request.user
            case.save()
            case.logger(str(request.user), " CASES_EDIT_EXECUTED")
            messages.success(request, 'Case edited')
            return redirect('/cases/' + str(case.case_id))
        else:
            return render(request, self.template_name, {'form': form})
