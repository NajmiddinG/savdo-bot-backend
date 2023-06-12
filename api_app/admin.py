from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.contrib import admin
from .models import BotUser, Product, Savat, Buyurtma, Income
from django.db.models import Sum
from django.utils import timezone
import os
from django import forms
from django.conf import settings
from .import_data import import_data
from django.shortcuts import render, redirect
from django.contrib.admin.helpers import ActionForm


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'date')
    search_fields = ('name', 'username')


class ImportDataForm(forms.Form):
    excel_file = forms.FileField(label='Select XLSX file')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'shtrix', 'name', 'kelish_narx', 'sotish_narx', 'brend')
    search_fields = ('name', 'brend', 'shtrix')
    change_list_template = 'admin/product_change_list.html'

    def import_from_excel_view(self, request):
        if request.method == 'POST':
            form = ImportDataForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = form.cleaned_data['excel_file']
                import_data(excel_file)
                self.message_user(request, 'Data imported successfully.')
                return redirect('admin:api_app_product_changelist')
        else:
            form = ImportDataForm()
        context = {
            'title': 'Import Products from Excel',
            'form': form,
            'opts': self.model._meta,
        }
        return render(request, 'admin/import_from_excel.html', context)

    

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-from-excel/', self.import_from_excel_view, name='import_from_excel'),
        ]
        return custom_urls + urls

@admin.register(Savat)
class SavatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'count', 'location', 'tel', 'date')
    search_fields = ('user__name', 'product__name', 'location', 'tel')


@admin.register(Buyurtma)
class BuyurtmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'yakunlandi', 'count', 'location', 'tel', 'date')
    search_fields = ('user__name', 'product__name', 'location', 'tel')



# class TimeRangeForm(ActionForm):
#     start_time = forms.DateTimeField(required=False, label='Start Time', widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S'))
#     end_time = forms.DateTimeField(required=False, label='Start Time', widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S'))


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyurtma', 'full_price', 'date')
    search_fields = ('buyurtma__user__name', 'full_price')
    # actions = ['get_report']
    # action_form = TimeRangeForm

    # def get_report(self, request, queryset):
    #     form = TimeRangeForm(request.POST)
    #     if form.is_valid():
    #         start_time = form.cleaned_data['start_time']
    #         end_time = form.cleaned_data['end_time']

    #         # Calculate income and profit within the time range
    #         range_stats = queryset.filter(date__range=[start_time, end_time])
    #         total_income = range_stats.aggregate(total_income=Sum('full_price'))['total_income'] or 0
    #         total_profit = range_stats.aggregate(total_profit=Sum('full_price') - Sum('buyurtma__product__kelish_narx'))['total_profit'] or 0

    #         # Display the statistics
    #         message = f"Income within the range: {total_income}\nProfit within the range: {total_profit}"
    #         self.message_user(request, message)

    # get_report.short_description = "Get Report"

    # def changelist_view(self, request, extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['time_range_form'] = TimeRangeForm()

    #     return super().changelist_view(request, extra_context=extra_context)


