import urllib

from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import logout
import uuid
import random

from django.utils import timezone
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.models import User
import threading
from superadmin.forms import UserForm, authenticate, UserResetForm, get_user_email, ResetForm, PaymentForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from .tokens import account_activation_token
from django.core.mail import EmailMessage
from superadmin.models import *
import os
from superadmin.vnpay import vnpay

from .plugin.novaclient import nova
from .plugin.keystoneclient import keystone
from .plugin.neutronclient import neutron
from .plugin.get_tokens import getToken
from kvmvdi.settings import OPS_ADMIN, OPS_IP, OPS_PASSWORD, OPS_PROJECT, OPS_TOKEN_EXPIRED, VNPAY_HASH_SECRET_KEY, VNPAY_TMN_CODE, VNPAY_API_URL, VNPAY_PAYMENT_URL, VNPAY_RETURN_URL, \
        PRICE_RAM, PRICE_VCPUS, PRICE_DISK_HDD ,PRICE_DISK_SSD, DISK_HDD, DISK_SSD
from django.utils import timezone

                
class EmailThread(threading.Thread):
    def __init__(self, email):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.email = email

    def run(self):
        self.email.send()
        

class check_ping(threading.Thread):
    def __init__(self, host):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.host = host

    def run(self):
        # response = os.system("ping -n 1 " + self.host)
        response = os.system("ping -c 1 " + self.host)
        if response == 0:
            return True
        else:
            return False


def home(request):
    user = request.user
    list_ops = Ops.objects.all()
    if user.is_authenticated  and user.is_adminkvm:
        if request.method == 'POST':
            if 'image' in request.POST:
                if Ops.objects.get(ip=request.POST['ops']):
                    ops = Ops.objects.get(ip=request.POST['ops'])
                    if not user.check_expired():
                        user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                        user.token_id = getToken(ip=ops.ip, username=user.username, password=user.username,
                                                 project_name=user.username, user_domain_id='default',
                                                 project_domain_id='default')
                        user.save()
                    connect = nova(ip=ops.ip, token_id=user.token_id, project_name=user.username,
                                   project_domain_id=ops.projectdomain)

                    svname = request.POST['svname']
                    image = request.POST['image']
                    network = request.POST['network']
                    ram = int(float(request.POST['ram']) * 1024)
                    vcpus = int(request.POST['vcpus'])
                    disk = int(request.POST['disk'])
                    count = int(request.POST['count'])

                    if [ram, vcpus, disk] in connect.list_flavor():
                        fl = connect.find_flavor(ram=ram, vcpus=vcpus, disk=disk)
                        im = connect.find_image(image)
                        net = connect.find_network(network)
                        connect.createVM(svname=svname, flavor=fl, image=im, network_id=net, max_count=count)
                    else:
                        connect.createFlavor(svname=svname, ram=ram, vcpus=vcpus, disk=disk)
                        check = False
                        while check == False:
                            if connect.find_flavor(ram=ram, vcpus=vcpus, disk=disk):
                                check = True
                        connect.createVM(svname=svname, flavor=connect.find_flavor(ram=ram, vcpus=vcpus, disk=disk), image=connect.find_image(image), network_id=connect.find_network(network), max_count=count)
                else:
                    return HttpResponseRedirect('/')
            elif 'delete' in request.POST:
                ops = Ops.objects.get(ip=request.POST['ops'])
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=ops.ip, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=ops.ip, token_id=user.token_id, project_name=user.username,
                               project_domain_id=ops.projectdomain)
                svid = request.POST['delete']
                connect.delete_vm(svid=svid)
            elif 'ipsv' in request.POST:
                Ops.objects.create(name=request.POST['nameops'],
                                    ip=request.POST['ipsv'],
                                    username=request.POST['username'],
                                    password=request.POST['password'],
                                    project=request.POST['project'],
                                    userdomain=request.POST['userid'],
                                    projectdomain=request.POST['projectid'])
            elif 'reload_image' in request.POST:
                ops_ip = request.POST['reload_image']
                if Ops.objects.get(ip=ops_ip):
                    thread = check_ping(host=ops_ip)
                    if thread.run():
                        ops = Ops.objects.get(ip=ops_ip)
                        if not user.check_expired():
                            user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                            user.token_id = getToken(ip=ops.ip, username=user.username, password=user.username,
                                                    project_name=user.username, user_domain_id='default',
                                                    project_domain_id='default')
                            user.save()
                        connect = nova(ip=ops.ip, token_id=user.token_id, project_name=user.username,
                                    project_domain_id=ops.projectdomain)
                        try:
                            Images.objects.all().delete()
                        except:
                            pass
                        for im in connect.list_Images():
                            print(im.name)
                            if im.visibility == 'public':
                                try:
                                    Images.objects.create(ops=ops, name=im.name, os=im.os_type)
                                except:
                                    Images.objects.create(ops=ops, name=im.name, os='other')
        return render(request, 'kvmvdi/index.html',{'username': mark_safe(json.dumps(user.username)),
                                                        'ops': list_ops,
                                                        'OPS_IP': OPS_IP
                                                        })
    else:
        return HttpResponseRedirect('/')

def flavors(request):
    user = request.user
    list_ops = Ops.objects.all()
    ops = Ops.objects.get(ip=OPS_IP)
    if user.is_authenticated  and user.is_adminkvm:
        if request.method == 'POST':
            if 'ram' in request.POST:
                if user.token_id is None or user.check_expired() == False:
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=OPS_ADMIN, password=OPS_PASSWORD, project_name=OPS_PROJECT,
                                user_domain_id='default', project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=OPS_PROJECT,
                            project_domain_id='default')
                flavor = connect.createFlavor(svname=request.POST['flavorname'], ram=int(request.POST['ram'])*1024, vcpus=int(request.POST['vcpus']), disk=0)
                Flavors.objects.create(ops=ops, i_d=flavor.id ,ram=int(request.POST['ram']), vcpus=int(request.POST['vcpus']), disk=int(request.POST['disk']), name=request.POST['flavorname'])
            elif 'flavorid' in request.POST:
                if user.token_id is None or user.check_expired() == False:
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=OPS_ADMIN, password=OPS_PASSWORD, project_name=OPS_PROJECT,
                                user_domain_id='default', project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=OPS_PROJECT,
                            project_domain_id='default')
                try:
                    fl = Flavors.objects.get(id=request.POST['flavorid'])
                    connect.deleteFlavor(i_d=fl.i_d)
                    fl.delete()
                except:
                    return HttpResponse('Xảy ra lỗi! Vui lòng thử lại sau!')
        return render(request, 'kvmvdi/flavors.html',{'username': mark_safe(json.dumps(user.username)),
                                                        'DISK_SSD': DISK_SSD,
                                                        'DISK_HDD': DISK_HDD,
                                                        'flavors': Flavors.objects.filter(ops=ops)
                                                        })
    else:
        return HttpResponseRedirect('/')

def users(request):
    user = request.user
    list_ops = Ops.objects.all()
    ops = Ops.objects.get(ip=OPS_IP)
    if user.is_authenticated  and user.is_adminkvm:
        if 'userid' in request.POST:
                try:
                    connect = keystone(ip=OPS_IP, username=OPS_ADMIN, password=OPS_PASSWORD, project_name=OPS_PROJECT,
                            user_domain_id='default', project_domain_id='default')
                    u = MyUser.objects.get(id=request.POST['userid'])
                    connect.delete_user(name=u.username)
                    connect.delete_project(name=u.username)
                    u.delete()
                except:
                    return HttpResponse('Xảy ra lỗi! Vui lòng thử lại sau!')
        return render(request, 'kvmvdi/user.html',{'username': mark_safe(json.dumps(user.username)),
                                                        'users': MyUser.objects.filter(is_adminkvm=0)
                                                        })
    else:
        return HttpResponseRedirect('/')

def home_data(request, ops_ip):
    user = request.user
    if user.is_authenticated  and user.is_adminkvm:
        if Ops.objects.get(ip=ops_ip):
            thread = check_ping(host=ops_ip)
            if thread.run():
                ops = Ops.objects.get(ip=ops_ip)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=ops.ip, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=ops.ip, token_id=user.token_id, project_name=user.username,
                               project_domain_id=ops.projectdomain)
                # print(thread.list_networks())
                data = []
                for item in connect.list_server():
                    # print(dir(item))
                    # print(item._info['OS-EXT-STS:power_state'])
                    try:
                        host = '<p>'+item._info['OS-EXT-SRV-ATTR:host']+'</p>'
                    except:
                        host = '<p></p>'
                    try:
                        name = '<p>'+item._info['name']+'</p>'
                    except:
                        name = '<p></p>'

                    # try:
                    #     image_name = '<p>'+connect.find_image(image=item._info['image']['id']).name+'</p>'
                    # except:
                    #     image_name = '<p></p>'

                    try:
                        ip = '<p>'+next(iter(item.networks.values()))[0]+'</p>'
                    except:
                        ip = '<p></p>'

                    # try:
                    #     network = '<p>'+list(item.networks.keys())[0]+'</p>'
                    # except:
                    #     network = '<p></p>'

                    # try:
                    #     flavor = '<p>'+connect.find_flavor(id=item._info['flavor']['id']).name+'</p>'
                    # except:
                    #     flavor = '<p></p>'

                    if item._info['status'] == 'ACTIVE':
                        status = '<span class="label label-success">'+item._info['status']+'</span>'
                    else:
                        status = '<span class="label label-danger">'+item._info['status']+'</span>'

                    created = '<p>'+item._info['created']+'</p>'

                    try:
                        actions = '''
                        <div class="btn-group">
                            <button type="button" class="btn btn-danger delete" name="'''+ops_ip+'''" id="del_'''+item._info['id']+'''">
                                <i class="fa fa-trash" data-toggle="tooltip" title="Delete"></i>
                            </button>
                            <button type="button" class="btn btn-success console" data-title="console" id="'''+item.get_console_url("novnc")["console"]["url"]+'''">
                                <i class="fa fa-bars" data-toggle="tooltip" title="Console"></i>
                            </button>
                        </div>
                        '''
                    except:
                        actions = '''
                        <div class="btn-group">
                            <button type="button" class="btn btn-danger delete" name="'''+ops_ip+'''" id="del_'''+item._info['id']+'''">
                                <i class="fa fa-trash" data-toggle="tooltip" title="Delete"></i>
                            </button>
                        </div>
                        '''
                    # data.append([host, name, image_name, ip, network, flavor, status, created, actions])
                    data.append([host, name, ip, status, created, actions])
                big_data = {"data": data}
                json_data = json.loads(json.dumps(big_data))
                return JsonResponse(json_data)
            else:
                data = []
                data.append(['<p></p>', '<p></p>', '<p></p>', '<p></p>', '<p></p>', '<p></p>', '<p></p>', '<p></p>', '<p></p>'])
                big_data = {"data": data}
                json_data = json.loads(json.dumps(big_data))
                return JsonResponse(json_data)

def user_login(request):
    user = request.user
    mess_register_ok = 'Hãy kiểm tra email của bạn để hoàn tất đăng ký'
    if user.is_authenticated  and user.is_adminkvm:
        return HttpResponseRedirect('/home')
    elif user.is_authenticated  and user.is_adminkvm == False:
        return HttpResponseRedirect('/client')
    else:
        if request.method == 'POST':
            # post form để User yêu cầu reset mật khẩu, gửi link về mail
            if 'uemail' in request.POST:
                form = UserResetForm(request.POST)
                if form.is_valid():
                    to_email = form.cleaned_data['uemail']
                    current_site = get_current_site(request)
                    user = get_user_email(to_email)
                    mail_subject = 'Reset password your account.'
                    message = render_to_string('kvmvdi/resetpwd.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.id)).decode(),
                        'token':account_activation_token.make_token(user),
                    })
                    email = EmailMessage(
                                mail_subject, message, to=[to_email]
                    )
                    thread = EmailThread(email)
                    thread.start()
                    return render(request, 'kvmvdi/login.html', {'mess': 'Please check email to reset your password!'})
                else:
                    error = ''
                    for field in form:
                        error += field.errors
                    return render(request, 'kvmvdi/login.html', {'error': error})
            elif 'agentname' and 'agentpass' in request.POST:
                username = request.POST['agentname']
                password = request.POST['agentpass']
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active and user.is_adminkvm:
                        print(username)
                        login(request, user)
                        if user.token_id is None or user.check_expired() == False:
                            user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                            user.token_id = getToken(ip=OPS_IP, username=OPS_ADMIN, password=OPS_PASSWORD, project_name=OPS_PROJECT,
                                        user_domain_id='default', project_domain_id='default')
                            user.save()
                        return HttpResponseRedirect('/home')
                    elif user.is_active and user.is_adminkvm == False:
                        login(request, user)
                        if user.token_id is None or user.check_expired() == False:
                            user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                            user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                                     project_name=user.username, user_domain_id='default',
                                                     project_domain_id='default')
                            user.save()
                        return HttpResponseRedirect('/client')
                    else:
                        return render(request, 'kvmvdi/login.html',{'error':'Your account is blocked!'})
                else:
                    return render(request, 'kvmvdi/login.html',{'error':'Invalid username or password '})
            elif 'firstname' and 'email' and 'password2' in request.POST:
                user_form = UserForm(request.POST)
                if user_form.is_valid():
                    current_site = get_current_site(request)
                    user = user_form.save()

                    mail_subject = 'Activate your blog account.'
                    message = render_to_string('kvmvdi/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.id)).decode(),
                        'token':account_activation_token.make_token(user),
                    })
                    to_email = user.email
                    email = EmailMessage(
                                mail_subject, message, to=[to_email]
                    )
                    thread = EmailThread(email)
                    thread.start()
                    return render(request, 'kvmvdi/login.html',{'error':mess_register_ok})
                    
                    # if user.username != 'admin':
                    #     connect = keystone(ip=OPS_IP, username=OPS_ADMIN, password=OPS_PASSWORD, project_name=OPS_PROJECT,
                    #                     user_domain_id='default', project_domain_id='default')
                    #     connect.create_project(name=user.username, domain='default')
                    #     check = False
                    #     while check == False:
                    #         if connect.find_project(user.username):
                    #             connect.create_user(name=user.username, domain='default', project=user.username,
                    #                                 password=user.username, email=request.POST['email'])
                    #             check = True
                    #     check1 = False
                    #     while check1 == False:
                    #         if connect.find_user(user.username):
                    #             check1 = True
                    #     connect.add_user_to_project(user=user.username, project=user.username)
                else:
                    error = ''
                    for field in user_form:
                        error += field.errors
                    return render(request, 'kvmvdi/login.html',{'error':error})
        return render(request, 'kvmvdi/login.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        if user.username != 'admin':
            connect = keystone(ip=OPS_IP, username=OPS_ADMIN, password=OPS_PASSWORD, project_name=OPS_PROJECT,
                            user_domain_id='default', project_domain_id='default')
            connect.create_project(name=user.username, domain='default')
            check = False
            while check == False:
                if connect.find_project(user.username):
                    connect.create_user(name=user.username, domain='default', project=user.username,
                                        password=user.username, email=user.email)
                    check = True
            check1 = False
            while check1 == False:
                if connect.find_user(user.username):
                    check1 = True
            connect.add_user_to_project(user=user.username, project=user.username)
            connect_user = keystone(ip=OPS_IP, username=user.username, password=user.username, project_name=user.username,
                            user_domain_id='default', project_domain_id='default')
            try:
                net_id = connect_user.create_network(user.username)
                net = connect_user.show_network(net_id)
                subnet = connect_user.show_subnet(net['network']['subnets'][0])
                if net['network']['shared'] == False:
                    shared = 0
                else:
                    shared = 1
                if net['network']['admin_state_up'] == False:
                    admin_state_up = 0
                else:
                    admin_state_up = 1
                if net['network']['router:external'] == False:
                    external = 0
                else:
                    external = 1
                Networks.objects.create(owner=user, name=user.username, subnets_associated=subnet['subnet']['cidr'], shared=shared, external=external, status=net['network']['status'], admin_state_up=admin_state_up)
            except:
                pass
        return redirect('/')
    else:
        return HttpResponse('Đường dẫn không hợp lệ!')

def resetpwd(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = ResetForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data)
                user.save()
                return redirect('/')
            else:
                return redirect('/')
        return render(request, 'kvmvdi/formresetpass.html', {})
    else:
        return HttpResponse('Link is invalid!')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_profile(request):
    user = request.user
    if user.is_authenticated  and user.is_adminkvm:
        return render(request, 'kvmvdi/profile.html', {'username': mark_safe(json.dumps(user.username))})
    else:
        return HttpResponseRedirect('/')

def payment(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            # Process input data and build url payment
            form = PaymentForm(request.POST)
            if form.is_valid():
                order_type = form.cleaned_data['order_type']
                order_id = form.cleaned_data['order_id']
                amount = form.cleaned_data['amount']
                order_desc = form.cleaned_data['order_desc']
                bank_code = form.cleaned_data['bank_code']
                language = form.cleaned_data['language']
                ipaddr = get_client_ip(request)
                # Build URL Payment
                vnp = vnpay()
                vnp.requestData['vnp_Version'] = '2.0.0'
                vnp.requestData['vnp_Command'] = 'pay'
                vnp.requestData['vnp_TmnCode'] = VNPAY_TMN_CODE
                vnp.requestData['vnp_Amount'] = amount * 100
                vnp.requestData['vnp_CurrCode'] = 'VND'
                vnp.requestData['vnp_TxnRef'] = order_id
                vnp.requestData['vnp_OrderInfo'] = order_desc
                vnp.requestData['vnp_OrderType'] = order_type
                # Check language, default: vn
                if language and language != '':
                    vnp.requestData['vnp_Locale'] = language
                else:
                    vnp.requestData['vnp_Locale'] = 'vn'
                    # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
                if bank_code and bank_code != "":
                    vnp.requestData['vnp_BankCode'] = bank_code

                vnp.requestData['vnp_CreateDate'] = timezone.datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
                vnp.requestData['vnp_IpAddr'] = ipaddr
                vnp.requestData['vnp_ReturnUrl'] = VNPAY_RETURN_URL
                vnpay_payment_url = vnp.get_payment_url(VNPAY_PAYMENT_URL, VNPAY_HASH_SECRET_KEY)
                print(vnpay_payment_url)
                if request.is_ajax():
                    # Show VNPAY Popup
                    result = JsonResponse({'code': '00', 'Message': 'Init Success', 'data': vnpay_payment_url})
                    return result
                else:
                    # Redirect to VNPAY
                    return redirect(vnpay_payment_url)
            else:
                print("Form input not validate")
        else:
            return render(request, "client/payment.html", {"title": "Thanh toán"})

def payment_ipn(request):
    user = request.user
    if user.is_authenticated:
        inputData = request.GET
        if inputData:
            vnp = vnpay()
            vnp.responseData = inputData.dict()
            order_id = inputData['vnp_TxnRef']
            amount = inputData['vnp_Amount']
            order_desc = inputData['vnp_OrderInfo']
            vnp_TransactionNo = inputData['vnp_TransactionNo']
            vnp_ResponseCode = inputData['vnp_ResponseCode']
            vnp_TmnCode = inputData['vnp_TmnCode']
            vnp_PayDate = inputData['vnp_PayDate']
            vnp_BankCode = inputData['vnp_BankCode']
            vnp_CardType = inputData['vnp_CardType']
            if vnp.validate_response(VNPAY_HASH_SECRET_KEY):
                # Check & Update Order Status in your Database
                # Your code here
                firstTimeUpdate = True
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    # Return VNPAY: Merchant update success
                    result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    # Already Update
                    result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})

            else:
                # Invalid Signature
                result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
        else:
            result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

        return result

def payment_return(request):
    user = request.user
    if user.is_authenticated:
        inputData = request.GET
        if inputData:
            vnp = vnpay()
            vnp.responseData = inputData.dict()
            order_id = inputData['vnp_TxnRef']
            amount = int(inputData['vnp_Amount']) / 100
            order_desc = inputData['vnp_OrderInfo']
            vnp_TransactionNo = inputData['vnp_TransactionNo']
            vnp_ResponseCode = inputData['vnp_ResponseCode']
            vnp_TmnCode = inputData['vnp_TmnCode']
            vnp_PayDate = inputData['vnp_PayDate']
            vnp_BankCode = inputData['vnp_BankCode']
            vnp_CardType = inputData['vnp_CardType']
            if vnp.validate_response(VNPAY_HASH_SECRET_KEY):
                if vnp_ResponseCode == "00":
                    user.money = str(float(user.money) + float(amount))
                    user.save()
                    return render(request, "client/payment_return.html", {"title": "Kết quả thanh toán",
                                                                           "result": "Thành công", "order_id": order_id,
                                                                           "amount": amount,
                                                                           "order_desc": order_desc,
                                                                           "vnp_TransactionNo": vnp_TransactionNo,
                                                                           "vnp_ResponseCode": vnp_ResponseCode})
                else:
                    return render(request, "client/payment_return.html", {"title": "Kết quả thanh toán",
                                                                           "result": "Lỗi", "order_id": order_id,
                                                                           "amount": amount,
                                                                           "order_desc": order_desc,
                                                                           "vnp_TransactionNo": vnp_TransactionNo,
                                                                           "vnp_ResponseCode": vnp_ResponseCode})
            else:
                return render(request, "client/payment_return.html",
                              {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                               "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                               "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"})
        else:
            return render(request, "client/payment_return.html", {"title": "Kết quả thanh toán", "result": ""})

def query(request):
    if request.method == 'GET':
        return render(request, "client/query.html", {"title": "Kiểm tra kết quả giao dịch"})
    else:
        # Add paramter
        vnp = vnpay()
        vnp.requestData = {}
        vnp.requestData['vnp_Command'] = 'querydr'
        vnp.requestData['vnp_Version'] = '2.0.0'
        vnp.requestData['vnp_TmnCode'] = VNPAY_TMN_CODE
        vnp.requestData['vnp_TxnRef'] = request.POST['order_id']
        vnp.requestData['vnp_OrderInfo'] = 'Kiem tra ket qua GD OrderId:' + request.POST['order_id']
        vnp.requestData['vnp_TransDate'] = request.POST['trans_date']  # 20150410063022
        vnp.requestData['vnp_CreateDate'] = timezone.datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
        vnp.requestData['vnp_IpAddr'] = get_client_ip(request)
        requestUrl = vnp.get_payment_url(VNPAY_API_URL, VNPAY_HASH_SECRET_KEY)
        responseData = urllib.request.urlopen(requestUrl).read().decode()
        print('RequestURL:' + requestUrl)
        print('VNPAY Response:' + responseData)
        data = responseData.split('&')
        for x in data:
            tmp = x.split('=')
            if len(tmp) == 2:
                vnp.responseData[tmp[0]] = urllib.parse.unquote(tmp[1]).replace('+', ' ')

        print('Validate data from VNPAY:' + str(vnp.validate_response(VNPAY_HASH_SECRET_KEY)))
        return render(request, "client/query.html", {"title": "Kiểm tra kết quả giao dịch", "data": vnp.responseData})

def refund(request):
    return render(request, "client/refund.html", {"title": "Gửi yêu cầu hoàn tiền"})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

