from django.urls import path
from . import views

urlpatterns = [
    path('view_all_wallets/', views.ListAllWallets.as_view()),
    path('create_wallet/', views.CreateViewWallet.as_view()),
    path('single_wallet/<int:pk>/', views.WalletDetail.as_view()),
    path('wallet/<int:pk>/deposit/', views.WalletDetailView.as_view()),
    path('wallets/<int:pk>/deposit/',
         views.RetreivesAllDepositInfoForSpecificWallet.as_view()),
    path('wallets/<int:wallet_id>/deposits/<int:deposit_id>/',
         views.RetreiveInfoOnDeposit.as_view()),
    path('wallets/<int:pk>/withdrawls/', views.WalletWithdrawView.as_view()),
    path('wallets/<int:pk>/withdrawal/',
         views.RetreivesAllWithdrawalInfoForSpecificWallet.as_view()),
    path('wallets/<int:wallet_id>/withdrawal/<int:withdrawal_id>/',
         views.RetreiveInfoOnWithdrawal.as_view()),
    path('wallets/<int:pk>/transfers/', views.TransferView.as_view()),
    path('wallets/<int:pk>/transfer/',
         views.RetreivesAllTransferInfoForSpecificWallet.as_view()),
    path('wallets/<int:wallet_id>/transfer/<int:transfer_id>/',
         views.RetreiveInfoOnTransfer.as_view()),
    path('wallets/<int:pk>/transactions/', views.TransactionListView.as_view()),
    path('wallets/<int:pk>/transaction/download/',
         views.TransactionPDFView.as_view()),
]
