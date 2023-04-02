from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import Wallets, Transaction
from rest_framework.views import APIView
from decimal import Decimal
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import WalletSerializer, TransactionSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa


class ListAllWallets(ListAPIView):
    queryset = Wallets.objects.all()
    serializer_class = WalletSerializer

    def get_queryset(self):
        return Wallets.objects.filter(user_id=self.request.user.id)


class CreateViewWallet(ListCreateAPIView):
    queryset = Wallets.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallets.objects.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # set the user_id to the current user's id before saving
        serializer.validated_data['user_id'] = request.user.id

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            'message': 'Wallet created successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class WalletDetail(RetrieveUpdateDestroyAPIView):
    queryset = Wallets.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        wallet = get_object_or_404(Wallets, pk=pk)
        wallet.delete()
        return Response({'status': 'success', 'message': 'wallet deleted successfully'}, status=status.HTTP_200_OK)


class WalletDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Wallets.objects.get(pk=pk)
        except Wallets.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        wallet = self.get_object(pk)
        transactions = wallet.transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        wallet = self.get_object(pk)
        amount = Decimal(request.data.get('amount', 0))
        if amount <= 0:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)
        wallet.amount += amount
        wallet.save()
        transaction = Transaction.objects.create(
            wallet=wallet, amount=amount, transaction_type='deposit')
        serializer = TransactionSerializer(transaction)
        return Response({'status': 'success', 'message': 'wallet deposited successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


class RetreivesAllDepositInfoForSpecificWallet(APIView):
    def get(self, request, pk, format=None):
        wallet = Wallets.objects.get(pk=pk)
        transactions = wallet.transactions.filter(transaction_type='deposit')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class RetreiveInfoOnDeposit(APIView):
    def get_object(self, wallet_id, deposit_id):
        try:
            return Transaction.objects.get(wallet__id=wallet_id, id=deposit_id, transaction_type='deposit')
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, wallet_id, deposit_id, format=None):
        deposit = self.get_object(wallet_id, deposit_id)
        serializer = TransactionSerializer(deposit)
        return Response(serializer.data)


class WalletWithdrawView(APIView):
    def get_object(self, pk):
        try:
            return Wallets.objects.get(pk=pk)
        except Wallets.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        wallet = self.get_object(pk)
        transactions = wallet.transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        wallet = self.get_object(pk)
        amount = Decimal(request.data.get('amount', 0))
        if amount <= 0:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)
        wallet.amount -= amount
        wallet.save()
        transaction = Transaction.objects.create(
            wallet=wallet, amount=amount, transaction_type='withdrawal')
        serializer = TransactionSerializer(transaction)
        return Response({'status': 'success', 'message': 'amount withdrawn successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


class RetreivesAllWithdrawalInfoForSpecificWallet(APIView):
    def get(self, request, pk, format=None):
        wallet = Wallets.objects.get(pk=pk)
        transactions = wallet.transactions.filter(
            transaction_type='withdrawal')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class RetreiveInfoOnWithdrawal(APIView):
    def get_object(self, wallet_id, withdrawal_id):
        try:
            return Transaction.objects.get(wallet__id=wallet_id, id=withdrawal_id, transaction_type='withdrawal')
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, wallet_id, withdrawal_id, format=None):
        withdrawal = self.get_object(wallet_id, withdrawal_id)
        serializer = TransactionSerializer(withdrawal)
        return Response(serializer.data)


class TransferView(APIView):
    def post(self, request, pk, format=None):
        source_wallet = Wallets.objects.get(pk=pk)
        destination_wallet_id = request.data.get('destination_wallet_id')
        amount = Decimal(request.data.get('amount', 0))

        # Perform validation, e.g. ensure the source wallet has enough balance,
        amount = Decimal(request.data.get('amount'))
        if amount <= 0:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

        if source_wallet.amount < amount:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct the transfer amount from the source wallet
        source_wallet.amount -= amount
        source_wallet.save()

        # Create a new transfer transaction for the source wallet
        transfer_transaction = Transaction.objects.create(
            wallet=source_wallet,
            amount=-amount,
            transaction_type='transfer',
        )

        # Add the transfer amount to the destination wallet
        destination_wallet = Wallets.objects.get(pk=destination_wallet_id)
        destination_wallet.amount += amount
        destination_wallet.save()

        # Create a new deposit transaction for the destination wallet
        deposit_transaction = Transaction.objects.create(
            wallet=destination_wallet,
            amount=amount,
            transaction_type='deposit',
        )

        # Return a success response
        response_data = {
            'id': transfer_transaction.pk,
            'source_wallet_id': source_wallet.pk,
            'destination_wallet_id': destination_wallet.pk,
            'amount': amount,
            'message': 'Transfer successful!',
        }
        return Response(response_data, status=status.HTTP_200_OK)


class RetreivesAllTransferInfoForSpecificWallet(APIView):
    def get(self, request, pk, format=None):
        wallet = Wallets.objects.get(pk=pk)
        transactions = wallet.transactions.filter(
            transaction_type='transfer')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class RetreiveInfoOnTransfer(APIView):
    def get_object(self, wallet_id, transfer_id):
        try:
            return Transaction.objects.get(wallet__id=wallet_id, id=transfer_id, transaction_type='transfer')
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, wallet_id, transfer_id, format=None):
        transfer = self.get_object(wallet_id, transfer_id)
        serializer = TransactionSerializer(transfer)
        return Response(serializer.data)


class TransactionListView(APIView):
    def get(self, request, pk):
        wallet = get_object_or_404(Wallets, pk=pk)
        transactions = wallet.transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        wallet = get_object_or_404(Wallets, id=id)
        transaction_type = request.data.get('transaction_type')
        amount = Decimal(request.data.get('amount', 0))

        # Perform validation, e.g. ensure the transaction type is valid,
        # the amount is positive, etc.
        # ...

        transaction = Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=transaction_type,
        )

        # Update the wallet balance based on the transaction type
        if transaction_type == 'deposit':
            wallet.amount += amount
        elif transaction_type == 'withdrawal':
            wallet.amount -= amount
        else:
            # Assume it's a transfer
            destination_wallet_id = request.data.get('destination_wallet_id')
            destination_wallet = get_object_or_404(
                Wallets, id=destination_wallet_id)
            if wallet.amount < amount:
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
            wallet.amount -= amount
            destination_wallet.amount += amount
            destination_wallet.save()

        wallet.save()

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionPDFView(APIView):
    def get(self, request, pk):
        wallet = Wallets.objects.get(pk=pk)
        transactions = Transaction.objects.filter(wallet=wallet)
        template = get_template('transactions.html')
        context = {'wallet': wallet, 'transactions': transactions}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{wallet.user}_transactions.pdf"'

        # Create a PDF file from the HTML content
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)
        return response
