from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Count, Sum
from .models import Order, Trailer, Driver
from .forms import OrderForm


class OrderListView(ListView):
    model = Order
    template_name = 'transports/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Сортировка по расстоянию или весу
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'distance':
            queryset = queryset.order_by('distance')
        elif sort_by == 'weight':
            queryset = queryset.order_by('weight')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort_by', '')
        return context


class OrderDetailView(DetailView):
    model = Order
    template_name = 'transports/order_detail.html'
    context_object_name = 'order'


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'transports/order_form.html', {'form': form})


def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'transports/order_form.html', {'form': form})


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'transports/order_confirm_delete.html', {'order': order})


def statistics(request):
    # Трейлер с наибольшим количеством заказов
    top_trailer = Trailer.objects.annotate(
        order_count=Count('order')
    ).order_by('-order_count').first()

    # Водитель с наибольшим количеством заказов
    top_driver = Driver.objects.annotate(
        order_count=Count('order')
    ).order_by('-order_count').first()

    # Рейсы без напарника
    solo_orders = Order.objects.filter(distance__lte=500)

    # Общая прибыль
    total_profit = Order.objects.aggregate(
        total=Sum('distance') * Sum('trailer__cost_per_km')
    )['total'] or 0

    context = {
        'top_trailer': top_trailer,
        'top_driver': top_driver,
        'solo_orders': solo_orders,
        'total_profit': total_profit,
    }

    return render(request, 'transports/statistics.html', context)