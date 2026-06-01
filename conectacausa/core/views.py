import json
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Sum
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Allocation, Campaign, Donation, DonorUser, SpendLog


def _payload(request):
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return {}


def _money(value):
    return float(value or 0)


def _seed_if_empty():
    if Campaign.objects.exists():
        return

    campaign = Campaign.objects.create(
        title='Cuidados Médicos',
        org='Luiz Santos',
        desc='Preciso de ajuda para conseguir ajuda médica.',
        goal=Decimal('5000.00'),
        deadline='2026-09-01',
    )
    Allocation.objects.create(campaign=campaign, name='Farmácia', pct=70)
    SpendLog.objects.create(
        campaign=campaign,
        date='2026-05-10',
        cat='Farmácia',
        desc='',
        amount=Decimal('200.00'),
    )
    user = DonorUser.objects.create(
        name='Ana Silva',
        email='donor@example.com',
        password_hash=make_password('password'),
    )
    Donation.objects.create(campaign=campaign, user=user, amount=Decimal('50.00'), date='2026-05-15')


def index(_request):
    return FileResponse(open(settings.BASE_DIR.parent / 'main.html', 'rb'))


def style(_request):
    return FileResponse(open(settings.BASE_DIR.parent / 'style.css', 'rb'), content_type='text/css')


def campaigns(_request):
    _seed_if_empty()
    data = []
    for campaign in Campaign.objects.prefetch_related('allocations', 'spend_logs', 'donations'):
        raised = campaign.donations.aggregate(total=Sum('amount'))['total'] or 0
        data.append({
            'id': campaign.id,
            'title': campaign.title,
            'org': campaign.org,
            'desc': campaign.desc,
            'goal': _money(campaign.goal),
            'raised': _money(raised),
            'deadline': campaign.deadline.isoformat(),
            'allocation': [
                {'name': item.name, 'pct': item.pct}
                for item in campaign.allocations.all()
            ],
            'spendLog': [
                {
                    'date': item.date.isoformat(),
                    'cat': item.cat,
                    'desc': item.desc,
                    'amount': _money(item.amount),
                }
                for item in campaign.spend_logs.all()
            ],
        })
    return JsonResponse({'campaigns': data})


@csrf_exempt
@require_http_methods(['POST'])
def login(request):
    data = _payload(request)
    user = DonorUser.objects.filter(email=data.get('email', '').strip()).first()
    if not user or not check_password(data.get('password', ''), user.password_hash):
        return JsonResponse({'error': 'Email ou senha inválidos.'}, status=401)
    return JsonResponse({'user': _user_json(user)})


@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    data = _payload(request)
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    if not name or not email or not password:
        return JsonResponse({'error': 'Favor preencher.'}, status=400)
    if DonorUser.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email já cadastrado.'}, status=409)
    user = DonorUser.objects.create(name=name, email=email, password_hash=make_password(password))
    return JsonResponse({'user': _user_json(user)}, status=201)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def donations(request):
    _seed_if_empty()
    if request.method == 'GET':
        email = request.GET.get('email', '').strip()
        user = get_object_or_404(DonorUser, email=email)
        return JsonResponse({'donations': [_donation_json(item) for item in user.donations.select_related('campaign')]})

    data = _payload(request)
    try:
        amount = Decimal(str(data.get('amount', '')))
    except InvalidOperation:
        return JsonResponse({'error': 'Digite um valor válido.'}, status=400)
    if amount < 1:
        return JsonResponse({'error': 'Digite um valor válido.'}, status=400)

    user = get_object_or_404(DonorUser, email=data.get('email', '').strip())
    campaign = get_object_or_404(Campaign, pk=data.get('campaignId'))
    donation = Donation.objects.create(
        campaign=campaign,
        user=user,
        amount=amount,
        anonymous=bool(data.get('anonymous')),
    )
    return JsonResponse({'donation': _donation_json(donation)}, status=201)


def _user_json(user):
    return {'name': user.name, 'email': user.email, 'role': user.role}


def _donation_json(donation):
    return {
        'campaignId': donation.campaign_id,
        'amount': _money(donation.amount),
        'date': donation.date.isoformat(),
        'anonymous': donation.anonymous,
    }
