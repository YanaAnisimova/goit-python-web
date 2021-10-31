from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.db.models import Sum, Func, Case, When, Value, IntegerField, F, ExpressionWrapper, Q, BooleanField
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timezone import now


from .models import Transaction, TransactionCategory

from django.http import HttpResponse
from finance.api import create_category, create_transaction  # NOQA


@login_required(login_url='auth:login')
def index(request):
    latest_record_list = Transaction.objects.filter(user=request.user).order_by('-created')[0:5]
    context = {'latest_record_list': latest_record_list}
    return render(request, 'finance/index.html', context)


@login_required(login_url='auth:login')
def reports_view(request):
    if not request.GET.get('reports'):
        categories = TransactionCategory.objects.filter(user=request.user).order_by('name')
        return render(request, 'finance/reports.html', {'categories': categories})
    user = request.user
    start = request.GET['from']
    end = request.GET['to']
    start, end = validate_period(start, end, user)
    categories = validate_categories(request.GET.getlist('category'), user)
    record_list = Transaction.objects.filter(created__range=[start, end],
                                             user=user,
                                             categories__in=categories
                                             )

    if request.GET['reports'] == 'r_detailed':
        context = handle_data_report_detailed(record_list)
        return render(request, 'finance/detailed.html', context)

    elif request.GET['reports'] == 'r_category':
        context = handle_data_report_by_category(record_list)
        return render(request, 'finance/category.html', context)

    elif request.GET['reports'] == 'r_month':
        context = handle_data_report_month(record_list)
        return render(request, 'finance/month.html', context)


def handle_data_report_month(record_list):
    sum_income_by_month = record_list.filter(
        amount__gte='0'
    ).values_list(
        'created__year',
        'created__month'
    ).annotate(
        total_i=Sum('amount')
    ).order_by(
        'created__year',
        'created__month'
    )

    sum_expenditure_by_month = record_list.filter(
        amount__lt='0'
    ).values_list(
        'created__year',
        'created__month'
    ).annotate(
        total_ex=Sum('amount')
    ).order_by(
        'created__year',
        'created__month'
    )
    sum_by_month = {}

    sum_income = 0
    for i in sum_income_by_month:
        sum_income += i[2]
        if sum_by_month.get(i[0]):
            sum_by_month[i[0]][i[1]] = {'income': i[2]}
        else:
            sum_by_month[i[0]] = {i[1]: {'income': i[2]}}

    sum_expenditure = 0
    for j in sum_expenditure_by_month:
        sum_expenditure += j[2]
        if sum_by_month.get(j[0]):
            if sum_by_month.get(j[0]).get(j[1]):
                sum_by_month[j[0]][j[1]]['expenditure'] = j[2]

            else:
                sum_by_month[j[0]][j[1]] = {'expenditure': j[2]}
        else:
            sum_by_month[j[0]] = {j[1]: [None, j[2]]}

    context = {
        'sum_by_month': sum_by_month,
        'sum_income': sum_income,
        'sum_expenditure': sum_expenditure,
        'total': sum_income + sum_expenditure
    }
    return context


def handle_data_report_by_category(record_list):
    group_by_categories = record_list.annotate(
        amount_positive=ExpressionWrapper(
            Q(amount__gte=0),
            output_field=BooleanField()
              )
        ).values(
        'categories',
        'amount_positive'
        ).annotate(
        sum=Sum('amount'),
        ).order_by(
            'categories'
        )

    result = dict()
    sum_income = 0
    sum_expenditure = 0

    for el in group_by_categories:
        id_category = el['categories']
        # если значение amount_positive True
        if el['amount_positive']:
            # если есть в result ключ 17
            if result.get(id_category):
                result[id_category]['sum_i'] = el['sum']
            else:
                result[id_category] = dict(category=TransactionCategory.objects.get(pk=id_category))
                result[id_category]['sum_i'] = el['sum']
                result[id_category]['sum_ex'] = 0
            sum_income += result[id_category]['sum_i']
        else:
            if result.get(id_category):
                result[id_category]['sum_ex'] = el['sum']
            else:
                result[id_category] = dict(category=TransactionCategory.objects.get(pk=id_category))
                result[id_category]['sum_ex'] = el['sum']
                result[id_category]['sum_i'] = 0
            sum_expenditure += result[id_category]['sum_ex']

    total = sum_income + sum_expenditure

    context = {
        'sum_by_category': result,
        'sum_income': sum_income,
        'sum_expenditure': sum_expenditure,
        'total': total
    }
    return context


def handle_data_report_detailed(record_list):
    sum_income = record_list.filter(amount__gte='0').aggregate(sum=Sum('amount'))
    sum_expenditure = record_list.filter(amount__lt='0').aggregate(sum=Sum('amount'))
    sum_income, sum_expenditure = validate_sum(sum_income, sum_expenditure)
    total = sum_income + sum_expenditure
    context = {
        'record_list': record_list,
        'sum_income': sum_income,
        'sum_expenditure': sum_expenditure,
        'total': total
    }
    return context


def validate_period(start, end, user):
    if start and end:
        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')
    if not start:
        start = Transaction.objects.filter(user=user).earliest('created').created
    if not end:
        end = now()
    return start, end


def validate_sum(sum_income, sum_expenditure):
    if sum_income and sum_expenditure:
        sum_income = sum_income['sum']
        sum_expenditure = sum_expenditure['sum']
    if not sum_income:
        sum_income = 0
    if not sum_expenditure:
        sum_expenditure = 0
    return sum_income, sum_expenditure


def validate_categories(categories, user):
    if categories[0] == 'all':
        categories = TransactionCategory.objects.filter(user=user)
    else:
        categories = TransactionCategory.objects.filter(user=user, name__in=categories)
    return categories


@login_required(login_url='auth:login')
def new_record_view(request):
    categories = TransactionCategory.objects.filter(user=request.user).order_by('name')
    if request.method == 'GET':
        return render(request, 'finance/record.html', {'categories': categories})

    elif request.method == 'POST' and 'Reports' in request.POST:
        amount_money = request.POST.get('money')
        if request.POST['income_expenditure'] == 'expenditure':
            amount_money = int(amount_money) * (-1)
        category = TransactionCategory.objects.filter(id=request.POST['category'])[0]
        comment = request.POST['comment']
        user = request.user

        # create transaction
        with transaction.atomic():
            trans = create_transaction(amount=amount_money, categories=category, user=user, comment=comment)
        return redirect(reverse('finance:index'))

    elif request.method == 'POST' and 'Create category' in request.POST:
        user_id = request.user.id
        name_category = request.POST.get('new_category', None)
        category_exists = TransactionCategory.objects.filter(user_id=user_id, name=name_category).exists()
        if category_exists:
            messages.add_message(request, messages.ERROR, '* Category already exists')
            return render(request, 'finance/record.html', {'categories': categories})

        # create category
        with transaction.atomic():
            category = create_category(name=name_category, user_id=user_id)
        return redirect(reverse('finance:new_record'))


