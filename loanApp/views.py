from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LoanRequestForm, LoanTransactionForm
from .models import loanRequest, loanTransaction, CustomerLoan
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Sum
# Create your views here.


# @login_required(login_url='/account/login-customer')
def home(request):

    return render(request, 'home.html', context={})


@login_required(login_url='/account/login-customer')
def LoanRequest(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('managerApp:dashboard'))
    form = LoanRequestForm()

    if request.method == 'POST':
        form = LoanRequestForm(request.POST)

        if form.is_valid():
            loan_obj = form.save(commit=False)
            loan_obj.customer = request.user.customer
            loan_obj.save()
            return redirect('/')

    return render(request, 'loanApp/loanrequest.html', context={'form': form})

    # reason = request.POST.get('reason')
    # amount = request.POST.get('amount')
    # category = request.POST.get('category')
    # year = request.POST.get('year')
    # customer = request.user.customer

    # loan_request = LoanRequest(request)
    # loan_request.customer = customer
    # loan_request.save()
    # if form.is_valid():
    #     loan_request = form.save(commit=False)
    #     loan_request.customer = request.user.customer
    #     print(loan_request)
    #     return redirect('/')


@login_required(login_url='/account/login-customer')
def LoanPayment(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('managerApp:dashboard'))
    form = LoanTransactionForm()
    if request.method == 'POST':
        form = LoanTransactionForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = request.user.customer
            payment.save()
            # pay_save = loanTransaction()
            return redirect('/')

    return render(request, 'loanApp/payment.html', context={'form': form})


@login_required(login_url='/account/login-customer')
def UserTransaction(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('managerApp:dashboard'))
    transactions = loanTransaction.objects.filter(
        customer=request.user.customer)
    return render(request, 'loanApp/user_transaction.html', context={'transactions': transactions})


@login_required(login_url='/account/login-customer')
def UserLoanHistory(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('managerApp:dashboard'))
    loans = loanRequest.objects.filter(
        customer=request.user.customer)
    return render(request, 'loanApp/user_loan_history.html', context={'loans': loans})


@login_required(login_url='/account/login-customer')
def UserDashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('managerApp:dashboard'))
    requestLoan = loanRequest.objects.all().filter(
        customer=request.user.customer).count(),
    approved = loanRequest.objects.all().filter(
        customer=request.user.customer).filter(status='approved').count(),
    rejected = loanRequest.objects.all().filter(
        customer=request.user.customer).filter(status='rejected').count(),
    totalLoan = CustomerLoan.objects.filter(customer=request.user.customer).aggregate(Sum('total_loan'))[
        'total_loan__sum'],
    totalPayable = CustomerLoan.objects.filter(customer=request.user.customer).aggregate(
        Sum('payable_loan'))['payable_loan__sum'],
    totalPaid = loanTransaction.objects.filter(customer=request.user.customer).aggregate(Sum('payment'))[
        'payment__sum'],
    

    dict = {
        'request': requestLoan[0],
        'approved': approved[0],
        'rejected': rejected[0],
        'totalLoan': totalLoan[0],
        'totalPayable': totalPayable[0],
        'totalPaid': totalPaid[0],
        

    }

    return render(request, 'loanApp/user_dashboard.html', context=dict)


def error_404_view(request, exception):
    print("not found")
    return render(request, 'notFound.html')
