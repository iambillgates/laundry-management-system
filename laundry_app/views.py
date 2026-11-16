from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import LaundryOrder
from .forms import LaundryOrderForm, TrackOrderForm


def _mask_address(address):
    """Show only the first ~10 characters of an address (public tracking)."""
    if not address:
        return ""
    text = str(address)
    return text[:10] + "..." if len(text) > 10 else text


def _mask_whatsapp(number):
    """Show only the first 4 and last 2 characters of a WhatsApp number."""
    if not number:
        return ""
    digits = str(number)
    if len(digits) <= 6:
        return digits[:2] + "****"
    return digits[:4] + "****" + digits[-2:]


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
                # Public tracking: never expose the full address / WhatsApp
                # number to anyone holding an E-Faktur number. Mask them
                # in memory only — nothing is saved back to the database,
                # staff still see the full details on the dashboard/admin.
                order.address = _mask_address(order.address)
                order.whatsapp = _mask_whatsapp(order.whatsapp)
                return render(request, 'laundry_app/track_result.html', {'order': order})
            except LaundryOrder.DoesNotExist:
                messages.error(request, 'Order with this E-Faktur Number does not exist.')
                return redirect('home')
    return redirect('home')

@login_required
def dashboard(request):
    # Staff only: the dashboard lists every customer's name, address
    # and WhatsApp number, so anonymous visitors must not reach it.
    if not request.user.is_staff:
        messages.error(request, 'Halaman dashboard hanya untuk staff.')
        return redirect('home')
    orders = LaundryOrder.objects.all().order_by('-created_at')
    return render(request, 'laundry_app/dashboard.html', {'orders': orders})
