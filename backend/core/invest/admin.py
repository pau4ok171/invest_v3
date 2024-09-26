import datetime

from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe
from statements.services.analysis import main


@admin.action(description='Analyse company by statements checks')
def check_company(modeladmin, request, queryset):
    return main(queryset)


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'slug',
        'get_html_image',
        'market',
        'sector',
        'industry',
        'is_visible'
    )

    prepopulated_fields = {'slug': ('ticker',)}
    list_display_links = ('title',)
    list_editable = ('is_visible',)
    readonly_fields = ('created', 'updated', 'created_by', 'updated_by')
    actions = [check_company]

    def get_html_image(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="50">')

    get_html_image.short_description = 'Logo'

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
            obj.updated = datetime.datetime.utcnow()
        else:
            obj.created_by = request.user
            obj.created = datetime.datetime.utcnow()

        super().save_model(request, obj, form, change)


@admin.register(models.Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'country')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'sector')
    list_display_links = ('title',)
    list_editable = ['sector']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('company', 'year', 'quarter', 'report_type', 'report_form')
    list_display_links = ('company',)
    fieldsets = (
        ('', {
            'fields':
                [
                    'company',
                    'verified',
                    'is_analysed',
                    'is_automatically_collected',
                    'is_verified',
                    'is_complete',
                ]
        }),
        ('Summary', {
            'fields':
                [
                    'year',
                    'quarter',
                    'report_type',
                    'report_form',
                    'scale',
                    'scale_unit',
                    'currency',
                ]
        }),
        ('Balance Sheet', {
            'fields':
                [
                    # Banks
                    # ASSETS
                    # SHORT-TERM ASSETS
                    # Cash
                    'cash_and_cash_equivalents',
                    'marketable_securities',
                    'cash_and_cash_equivalents_and_marketable_securities',
                    # Receivable
                    'accounts_receivable',
                    'notes_receivable',
                    'loans_receivable',
                    'other_current_receivables',
                    'total_receivables',
                    # Inventories
                    'inventories_and_raw_materials_and_components',
                    'inventories_and_work_in_process',
                    'inventories_and_inventories_adjustments',
                    'inventories_and_other',
                    'inventories_and_finished_good',
                    'total_inventories',
                    # Other current assets
                    'other_current_assets',
                    # TOTAL CURRENT ASSETS
                    'total_current_assets',
                    # LONG-TERM ASSETS
                    # Property, Plant and Equipment
                    'investments_and_advanced',
                    'land_and_improvements',
                    'buildings_and_improvements',
                    'machinery_and_furniture_and_equipment',
                    'construction_in_progress',
                    'other_gross_ppe',
                    'gross_property_and_plant_and_equipment',
                    'accumulated_depreciation',
                    'property_and_plant_and_equipment',
                    # Intangible Assets
                    'intangible_assets',
                    'goodwill',
                    # Other long-term assets
                    'other_long_term_assets',
                    # TOTAL LONG-TERM ASSETS
                    'total_long_term_assets',
                    # TOTAL ASSETS
                    'total_assets',

                    # LIABILITIES
                    # CURRENT LIABILITIES
                    # Accounts payable and accrued expense
                    'accounts_payable',
                    'total_tax_payable',
                    'other_current_payables',
                    'current_accrued_expense',
                    'accounts_payable_and_accrued_expense',
                    # Short-term debt and capital lease obligation
                    'short_term_debt',
                    'short_term_capital_lease_obligation',
                    'short_term_debt_and_capital_lease_obligation',
                    # Current deferred tax and revenue
                    'current_deferred_revenue',
                    'deferred_tax_and_revenue',
                    # Other current liabilities
                    'other_current_liabilities',
                    # TOTAL CURRENT LIABILITIES
                    'total_current_liabilities',
                    # LONG LIABILITIES
                    'long_term_debt',
                    'long_term_capital_lease_obligation',
                    'long_term_debt_and_capital_lease_obligation',
                    'pension_and_retirement_benefit',
                    'non_current_deferred_liabilities',
                    'other_long_term_liabilities',
                    # TOTAL LONG-TERM LIABILITIES
                    'total_long_term_liabilities',
                    # TOTAL LIABILITIES
                    'total_liabilities',
                    # EQUITY
                    'common_stock',
                    'preferred_stock',
                    'retained_earnings',
                    'accumulated_other_comprehensive_income_or_loss',
                    'additional_paid_in_capital',
                    'treasury_stock',
                    'other_stockholders_equity',
                    'total_stockholders_equity',
                    'minority_interest',
                    'total_equity',
                    # # INDUSTRIAL
                    # 'balance_sheet_cash_and_cash_equivalents',
                    # 'money_market_investments',
                    # # Net loans
                    # 'gross_loan',
                    # 'allowance_for_loans_and_lease_losses',
                    # 'unearned_income',
                    # 'net_loan',
                    # 'securities_and_investments',
                    # # Total Receivables
                    # # ...
                    # # ...
                    # # ...
                    # # Property, Plant and Equipment
                    # # Intangible Assets
                    # # ...
                    # 'other_assets_for_banks',
                    # # TOTAL ASSETS
                    # 'total_deposits',
                    # # accounts_payable_and_accrued_expense
                    # # short_term_debt_and_capital_lease_obligation
                    # # current deferred tax and revenue
                    # # current_deferred_revenue
                    # # deferred_tax_and_revenue
                    # # long_term_debt_and_capital_lease_obligation
                    # # non_current_deferred_liabilities
                    # # TOTAL LIABILITIES
                    # # common_stock
                    # # preferred_stock
                    # # accumulated_other_comprehensive_income_or_loss
                    # # additional_paid_in_capital
                    # # treasury_stock
                    # # other_stockholders_equity
                    # # total_stockholders_equity
                    # # minority_interest
                    # # total_equity
                    #
                    # # FONDS
                    # 'fixed_maturity_investment',
                    # 'equity_investments',
                    # 'short_term_investments',
                    # 'net_loan',
                    # 'balance_sheet_cash_and_cash_equivalents',
                    # # Total Receivables
                    # # ...
                    # # ...
                    # # ...
                    # 'deferred_policy_acquisition_costs',
                    # # Property, Plant and Equipment
                    # # Intangible Assets
                    # # ...
                    # 'other_assets_for_insurance_companies',
                    # # TOTAL ASSETS
                    # 'unpaid_loss_and_loss_reserve',
                    # 'unearned_premiums',
                    # 'future_policy_benefits',
                    # 'policyholder_funds',
                    # 'accounts_payable_and_accrued_expense_for_financial_companies',
                    # # short_term_debt_and_capital_lease_obligation
                    # # current_deferred_revenue
                    # 'current_deferred_taxes_liabilities',
                    # # deferred_tax_and_revenue
                    # # long_term_debt_and_capital_lease_obligation
                    # 'other_liabilities_for_insurance_companies',
                    # # TOTAL LIABILITIES
                    # # common_stock
                    # # preferred_stock
                    # # accumulated_other_comprehensive_income_or_loss
                    # # additional_paid_in_capital
                    # # treasury_stock
                    # # other_stockholders_equity
                    # # total_stockholders_equity
                    # # minority_interest
                    # # total_equity
                ]
        }),
        ('Income Statement', {
            'fields':
                [
                    # Banks
                    'interest_income',
                    'interest_expense',
                    'net_interest_income_for_banks',
                    'non_interest_income',
                    'revenue',
                    'credit_losses_provision',
                    'selling_and_general_and_administrative_expense',
                    'other_noninterest_expense',
                    'total_noninterest_expense',
                    'special_charges',
                    'other_income',
                    'pretax_income',
                    'tax_provision',
                    'tax_rate',
                    'other_net_income_or_loss',
                    'net_income_including_noncontrolling_interests',
                    'net_income_continuing_operations',
                    'net_income_discontinued_operations',
                    'other_income_minority_interest',
                    'net_income',
                    # net_margin
                    'preferred_dividends',
                    'eps_basic',
                    'eps_diluted',
                    'shares_outstanding_diluted_average',
                    'depreciation_and_depletion_and_amortization',

                    # INDUSTRIAL
                    # revenue
                    'cost_of_goods_sold',
                    'gross_profit',
                    # gross_margin
                    # selling_and_general_and_administrative_expense
                    'research_and_development',
                    'other_operating_expense',
                    'total_operating_expense',
                    'operating_income',
                    # operating_margin
                    # interest_income
                    # interest_expense
                    'net_interest_income',
                    # other_income
                    # pretax_income
                    # tax_provision
                    # tax_rate
                    # other_net_income_or_loss
                    # net_income_including_noncontrolling_interests
                    # net_income_continuing_operations
                    # net_income_discontinued_operations
                    # other_income_minority_interest
                    # net_income
                    # net_margin
                    # preferred_dividends
                    # eps_basic
                    # eps_diluted
                    # shares_outstanding_diluted_average
                    'ebit',
                    # depreciation_and_depletion_and_amortization
                    'ebitda',
                    # ebitda_margin

                    # FOND
                    'total_premiums_earned',
                    'net_investment_income',
                    # interest_income
                    'fees_and_other_income',
                    # revenue
                    # selling_and_general_and_administrative_expense
                    'net_policyholder_benefits_or_claims',
                    'policy_acquisition_expense',
                    # interest_expense
                    'other_expense',
                    'total_expenses',
                    # pretax_income
                    # tax_provision
                    # tax_rate
                    # other_net_income_or_loss
                    # net_income_continuing_operations
                    # net_income_including_noncontrolling_interests
                    # net_income_discontinued_operations
                    # other_income_minority_interest
                    # net_income
                    # net_margin
                    # preferred_dividends
                    # eps_basic
                    # eps_diluted
                    # shares_outstanding_diluted_average
                    # ebit
                    # depreciation_and_depletion_and_amortization
                    # ebitda
                    # ebitda_margin

                    'general_and_administrative_expense',
                    'non_operation_income',
                    'selling_and_marketing_expense',
                    'shares_outstanding_basic_average',
                    'tax_expense',
                ]
        }),
        ('Cashflow Statement', {
            'fields':
                [
                    'net_income_from_continuing_operations',
                    'depreciation_and_depletion_and_amortization_cash_flow',
                    'change_in_receivables',
                    'change_in_inventory',
                    'change_in_prepaid_assets',
                    'change_in_payables_and_accrued_expense',
                    'change_in_other_working_capital',
                    'change_in_working_capital',
                    'deferred_tax',
                    'stock_based_compensation',
                    'asset_impairment_charge',
                    'cash_from_discontinued_operating_activities',
                    'cash_flow_from_others',
                    'cash_flow_from_operations',
                    'purchase_of_property_and_plant_and_equipment',
                    'sale_of_property_and_plant_and_equipment',
                    'purchase_of_business',
                    'sale_of_business',
                    'purchase_of_investment',
                    'sale_of_investment',
                    'net_intangibles_purchase_and_sale',
                    'cash_flow_from_discontinued_operations',
                    'cash_from_other_investing_activities',
                    'cash_flow_from_investing',
                    'issuance_of_stock',
                    'repurchase_of_stock',
                    'net_issuance_of_preferred_stock',
                    'issuance_of_debt',
                    'payments_of_debt',
                    'net_issuance_of_debt',
                    'cash_flow_for_dividends',
                    'cash_flow_for_lease_financing',
                    'other_financing',
                    'cash_flow_from_financing',
                    'beginning_cash_position',
                    'effect_of_exchange_rate_changes',
                    'net_change_in_cash',
                    'ending_cash_position',
                    'capital_expenditure',
                    'free_cash_flow',
                ]
        }),
        ('CashFlow Other', {
            'fields': [
                'all_taxes_paid',
                'cash_from_discontinued_investing_activities',
                'cash_paid_for_insurance_activities',
                'cash_payments',
                'cash_payments_for_deposits_by_banks_and_customers',
                'cash_payments_for_loans',
                'cash_receipts_from_deposits_by_banks_and_customers',
                'cash_receipts_from_fees_and_commissions',
                'cash_receipts_from_loans',
                'cash_receipts_from_operating_activities',
                'cash_receipts_from_securities_related_activities',
                'cash_receipts_from_tax_refunds',
                'cash_receipts_from_insurance_activities',
                'dividends_paid',
                'dividends_received',
                'ffo',
                'interest_and_commission_paid',
                'interest_paid',
                'interest_received',
                'other_cash_payments_from_operating_activities',
                'other_cash_receipts_from_operating_activities',
                'payments_on_behalf_of_employees',
                'payments_to_suppliers_for_goods_and_services',
                'receipts_from_customers',
                'receipts_from_government_grants',
                'taxes_refund_paid',
            ]
        }),
        ('Additional Info', {
            'fields':
                [
                    'share_outstanding_eop',
                    'total_employees_figure',
                ]
        }),

    )


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'currency')


@admin.register(models.Sorter)
class SorterAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order_type')


@admin.register(models.CandlePerDay)
class CandlePerDayAdmin(admin.ModelAdmin):
    list_display = ('company', 'open', 'high', 'close', 'low', 'volume', 'time', 'is_complete')
    ordering = ('-time', 'company__title')
    list_filter = ('company__title', 'time')
    search_fields = ('company__title', 'time')


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_iso', 'symbol')


@admin.register(models.Analyst)
class AnalystAdmin(admin.ModelAdmin):
    list_display = ('name', 'score')


@admin.register(models.AnalystIdea)
class AnalystIdeaAdmin(admin.ModelAdmin):
    list_display = ('analyst', 'company', 'idea_created', 'price_target', 'date_target')


@admin.register(models.Dividend)
class DividendAdmin(admin.ModelAdmin):
    list_display = ('company', 'ex_dividend_date', 'dividend_yield')
