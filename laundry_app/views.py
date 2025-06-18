from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import LaundryOrder
from .forms import LaundryOrderForm, TrackOrderForm

def home(request):
    if request.method == 'POST':
        form = LaundryOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, f'Order placed successfully! Your E-Faktur Number is {order.e_invoice_number}')
            return redirect('home')
    else:
        form = LaundryOrderForm()

    track_form = TrackOrderForm()
    context = {
        'form': form,
        'track_form': track_form,
    }
    return render(request, 'laundry_app/home.html', context)

def track_order(request):
    if request.method == 'POST':
        form = TrackOrderForm(request.POST)
        if form.is_valid():
            e_invoice_number = form.cleaned_data['e_invoice_number']
            try:
                order = LaundryOrder.objects.get(e_invoice_number=e_invoice_number)
                return render(request, 'laundry_app/track_result.html', {'order': order})
            except LaundryOrder.DoesNotExist:
                messages.error(request, 'Order with this E-Faktur Number does not exist.')
                return redirect('home')
    return redirect('home')

def dashboard(request):
    orders = LaundryOrder.objects.all().order_by('-created_at')
    return render(request, 'laundry_app/dashboard.html', {'orders': orders})
