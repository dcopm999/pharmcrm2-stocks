from django.contrib.auth import mixins
from django.urls import reverse_lazy
from django.views import generic

from stocks import forms, models


class HomeView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = "stocks/base.html"


class StockListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = "stocks.view_stock"
    model = models.Stock


class StockDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = "stocks.view_stock"
    model = models.Stock


class StockCreateView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = "stocks.add_stock"
    model = models.Stock
    form_class = forms.StockForm
    success_url = reverse_lazy("goods:stock-list")


class StockUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView):
    permission_required = "stocks.change_stock"
    model = models.Stock
    form_class = forms.StockForm

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("stocks:stock-detail", kwargs={"slug": self.object.slug})


class StockDeleteView(mixins.PermissionRequiredMixin, generic.DeleteView):
    permission_required = "stocks.delete_stock"
    model = models.Stock
    success_url = reverse_lazy("stocks:stock-list")


class BatchListView(mixins.PermissionRequiredMixin, generic.ListView):
    permission_required = "stocks.view_batch"
    model = models.Batch


class BatchDetailView(mixins.PermissionRequiredMixin, generic.DetailView):
    permission_required = "stocks.view_batch"
    model = models.Batch


class BatchCreateView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = "stock.add_batch"
    model = models.Batch
    form_class = forms.BatchForm
    success_url = reverse_lazy("stocks:batch-list")


class BatchUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView):
    permission_required = "stocks.change_batch"
    model = models.Batch
    form_class = forms.BatchForm

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("stocks:batch-detail", kwargs={"slug": self.object.slug})


class BatchDeleteView(mixins.PermissionRequiredMixin, generic.DeleteView):
    permission_required = "stocks.delete_batch"
    model = models.Batch
    success_url = reverse_lazy("stocks:batch-list")
