import os
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from .models import Call, Client, LogCall
from users.models import User
from .filter import CallsFilter
from call_center.tasks import groups_phone_numbers
from .forms import EditCallForm, EditClientForm, ChoicePhoneForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
# Create your views here.


@login_required(login_url='/accounts/login/')
def call_list(request):
    call_list = Call.objects.all().order_by('-date_call')
    filter = CallsFilter(request.GET, queryset=call_list)
    paginator = Paginator(filter.qs, 20)
    page = request.GET.get('page')

    try:
        calls = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        calls = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        calls = paginator.page(paginator.num_pages)

    return render_to_response(
        'crm/calls_list.html', {
            'queryset': calls,
            'filter': filter,
            'request': request,
            'settings': settings,
        }
    )


class LogCallList(TemplateView):
    template_name = 'crm/log_call.html'

    def get_context_data(self, pk, **kwargs):
        context = super(LogCallList, self).get_context_data(**kwargs)
        context['log_call'] = LogCall.objects.filter(call=pk)
        context['settings'] = settings
        return context


class CallEdit(TemplateView):
    template_name = 'crm/call_edit_form.html'
    success_url = reverse_lazy('calls_list')

    def get_context_data(self, pk, **kwargs):
        context = super(CallEdit, self).get_context_data(**kwargs)
        context['settings'] = settings
        context['call'] = get_object_or_404(Call, pk=pk)
        context['call_form'] = EditCallForm(
            self.request.POST or None, instance=context['call'])
        context['client_form'] = EditClientForm(
            self.request.POST or None, instance=context['call'].client)
        return context

    def post(self, request, pk, *args, **kwargs):
        context = self.get_context_data(pk)
        if context['call_form'].is_valid() and context['client_form'].is_valid():
            call = context['call_form'].save(commit=False)
            client = context['client_form'].save()
            call.client = client
            call.login_name = request.user
            call.status_task = True
            if Call.objects.get(id=pk):
                self.log_call(
                    call,
                    call.executor_task,
                    call.type_task,
                    call.description_task,
                    pk,
                    request
                )
            call.save()
            if call.executor_task and call.executor_task.send_email:
                send_email(
                    call.executor_task.email,
                    call.type_task,
                    call.description_task,
                    call.client.fio,
                    call.client.phone_number,
                    call.file_name,
                    call.disposition,
                    call.path_to_file,
                )
            return redirect('calls_list')
        return JsonResponse({'errors': [context['call_form'].errors, context['client_form'].errors]})

    def log_call(self, call, form_executor_task, form_type_task, form_description_task, pk, request):
        call_from_bd = Call.objects.get(id=pk)

        if call_from_bd.executor_task != form_executor_task:
            executor_task = call_from_bd.executor_task
        else:
            executor_task = None

        if call_from_bd.type_task != form_type_task:
            type_task = call_from_bd.type_task
        else:
            type_task = ""

        if call_from_bd.description_task != form_description_task:
            description_task = call_from_bd.description_task
        else:
            description_task = ""

        LogCall.objects.create(
            call=call,
            old_executor_task=executor_task,
            old_type_task=type_task,
            old_description_task=description_task,
            log_time=timezone.now(),
            user_changed_record=request.user,
        )


class PhoneNumberChoice(TemplateView):
    template_name = 'crm/choice_phone_form.html'
    success_url = reverse_lazy('calls_list')

    def get_context_data(self, **kwargs):
        context = super(PhoneNumberChoice, self).get_context_data(**kwargs)
        context['settings'] = settings
        context['choice_phone_form'] = ChoicePhoneForm(
            self.request.POST or None, instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['choice_phone_form'].is_valid():
            user = context['choice_phone_form'].save(commit=False)
            user.save()

            return redirect('calls_list')
        return JsonResponse({'errors': [context['choice_phone_form'].errors]})


def send_email(email, problem_type, problem_discription, client_name, phone_number, audio_file, disposition, path_to_file):
    email = EmailMessage(
        "Заявка из CRM: {} {}".format(problem_type, timezone.now()),
        "Здравствуйте! \n Вам поступила заявка из CRM. От клиента: {} ,номер телефона: {}. \n Тип проблемы:{}. \n Описание проблемы: \n {}".format(
            client_name, phone_number, problem_type, problem_discription),
        settings.EMAIL_HOST_USER,
        [email],
    )
    if audio_file:
        if disposition == 'NO ANSWER':
            path = os.path.join(
                settings.MAIL_PATH_TO_ANSWERING_MACHINE, audio_file)
        else:
            path = os.path.join(settings.MAIL_PATH_TO_CALLS,
                                path_to_file, audio_file)
        email.attach_file(path)
    email.send()


def activity_users(request):
    request.user.last_login = timezone.now()
    request.user.save()
    return HttpResponse('')


def call_update(request):

    try:
        call = Call.objects.filter(is_get_history=False).filter(
            dst_phone_number=request.user.phone_number_local).first()
        return JsonResponse({
            'dst_phone_number': call.dst_phone_number,
            'client_phone_number': call.client.phone_number,
            'unique_id': call.unique_id,
            'client_surname': call.client.surname,
            'client_name': call.client.name,
            'call_id': call.id,
        })
    except:
        return HttpResponse('')
