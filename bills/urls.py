from django.urls import path

from . import views

app_name = "bills"

urlpatterns = [
    path(
        "receipts/create/<str:note_number>/",
        views.ReceiptCreateView.as_view(),
        name="receipt_create",
    ),
    path(
        "invoices/create/<str:note_number>/<int:supply_time>/",
        views.InvoiceCreateView.as_view(),
        name="invoice_create",
    ),
    path(
        "adv_invoices/create/<str:note_number>/<int:supply_time>/<str:advance_value>/",
        views.AdvanceInvoiceCreateView.as_view(),
        name="adv_invoice_create",
    ),
    path(
        "invoices/update/<str:note_number>/<int:supply_time>/<str:state>/",
        views.InvoiceUpdateView.as_view(),
        name="invoice_update",
    ),
    path(
        "adv_invoices/update/<str:note_number>/<int:supply_time>/<str:state>/<str:advance_value>/",
        views.AdvanceInvoiceUpdateView.as_view(),
        name="adv_invoice_update",
    ),
    path(
        "receipts/delete/<str:note_number>/",
        views.ReceiptDeleteView.as_view(),
        name="receipt_delete",
    ),
    path(
        "invoices/delete/<str:note_number>/",
        views.InvoiceDeleteView.as_view(),
        name="invoice_delete",
    ),
    path(
        "adv_invoices/delete/<str:note_number>/",
        views.AdvanceInvoiceDeleteView.as_view(),
        name="adv_invoice_delete",
    ),
    path(
        "receipts/<str:note__number>/",
        views.ReceiptDetailView.as_view(),
        name="receipt_detail",
    ),
    path("receipts/", views.ReceiptListView.as_view(), name="receipt_list"),
    path(
        "invoices/<str:note__number>/",
        views.InvoiceDetailView.as_view(),
        name="invoice_detail",
    ),
    path("invoices/", views.InvoiceListView.as_view(), name="invoice_list"),
    path(
        "adv_invoices/<str:note__number>/",
        views.AdvanceInvoiceDetailView.as_view(),
        name="adv_invoice_detail",
    ),
    path(
        "adv_invoices/", views.AdvanceInvoiceListView.as_view(), name="adv_invoice_list"
    ),
    path("export/", views.ExportData.as_view(), name="export_list"),
    path(
        "export/<str:note_number>/",
        views.ExportData.as_view(),
        name="export_detail",
    ),
    path("test_data/", views.AddTestData.as_view(), name="test_data"),
]
