import urllib

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import logout

from django.utils.safestring import mark_safe
import json
import threading


from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from superadmin.models import MyUser, Oders, Server, Sshkeys, Flavors, Images, Ops, Networks
import binascii, os

from superadmin.plugin.novaclient import nova
from superadmin.plugin.get_tokens import getToken
from superadmin.plugin.neutronclient_ import neutron_

from django.utils import timezone
from kvmvdi.settings import OPS_IP, list_net_provider, DISK_HDD, DISK_SSD, \
    OPS_TOKEN_EXPIRED, OPS_ADMIN, OPS_IP, OPS_PASSWORD, OPS_PROJECT, PRICE_RAM, PRICE_VCPUS, PRICE_DISK_HDD ,PRICE_DISK_SSD, DISK_HDD, DISK_SSD
import time

import django_rq
q = django_rq.get_queue('default', default_timeout=900)
# redis_conn = django_rq.get_connection()
# worker = django_rq.get_worker()
# worker.
# worker = django_rq.get_worker('low', 'high')

# from rq import Queue
# from redis import Redis

# redis_conn = Redis()
# q = Queue(connection=redis_conn)
class EmailThread(threading.Thread):
    def __init__(self, email):
        threading.Thread.__init__(self)
        # self._stop_event = threading.Event()
        self.email = email

    def run(self):
        try:
            self.email.send()
        except Exception as e:
            print(e)
        else:
            print('Sent!')

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

def createServer(type_disk, flavor, image, svname, private_network, count, user, root_pass, price, o_s, cloudinit=None, sshkey=None):
    user_admin = MyUser.objects.get(username='admin')
    if user_admin.is_active and user_admin.is_adminkvm:
        if user_admin.token_id is None or user_admin.check_expired() == False:
            user_admin.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
            user_admin.token_id = getToken(ip=OPS_IP, username=OPS_ADMIN, password=OPS_PASSWORD, project_name=OPS_PROJECT, user_domain_id='default', project_domain_id='default')
            user_admin.save()
    connect_neutron = neutron_(ip=OPS_IP, token_id=user_admin.token_id, project_name=OPS_PROJECT, project_domain_id='default')
    ops = Ops.objects.get(ip=OPS_IP)
    if not user.check_expired():
        user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
        user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                    project_name=user.username, user_domain_id='default',
                                    project_domain_id='default')
        user.save()
    connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                    project_domain_id='default')
    net = ''
    try:
        fl = connect.find_flavor(id=flavor.split(',')[3])
    except:
        return "Xay ra loi khi check flavor!"
    try:
        im = connect.find_image(image)
    except:
        return "Xay ra loi khi check image!"
    for network in list_net_provider:
        try:
            ip_net = connect.find_network(network)
        except:
            return "Xay ra loi khi check network!"
        if connect_neutron.free_ips(ip_net=ip_net) > 2:
            net = ip_net
            break
    if net == '':
        return "No IP availability!"
    try:
        volume = connect.create_volume(name=svname, size=flavor.split(',')[2], imageRef=im.id, volume_type=type_disk)
    except:
        return "Xay ra loi khi tao volume!"
    if volume:
        check = False
        while check == False:
            if connect.check_volume(id=volume.id).status == 'error':
                return "Xay ra loi khi tao volume!"
            elif connect.check_volume(id=volume.id).status == 'available':
                volume_id = volume.id
                break
            else:
                time.sleep(2)
    else:
        return "Xay ra loi khi tao volume!"
    try:
        if o_s is not None:
            serverVM = connect.createVM(svname=svname, flavor=fl, image=im, network_id=net, private_network=private_network, volume_id=volume_id, max_count=count)
        else:
            serverVM = connect.createVM(svname=svname, flavor=fl, image=im, network_id=net, private_network=private_network, volume_id=volume_id, max_count=count, userdata=cloudinit, key_name=sshkey,)
    except:
        try:
            connect.delete_volume(volume=volume_id)
        except:
            pass
        return "Xay ra loi khi create Server!"
    user.money = str(float(user.money) - float(price))
    user.save()
    Server.objects.create(project=user.username, description='test', name=svname, ram=flavor.split(',')[0], vcpus=flavor.split(',')[1], disk=flavor.split(',')[2], owner=user)
    Oders.objects.create(service='cloud', price=price, created=timezone.now(), owner=user, server=svname)
    time.sleep(5)
    while (1):
        if connect.get_server(serverVM.id).status != 'BUILD':
            break
        else:
            time.sleep(2)
    mail_subject = 'Thông tin server của bạn là: '
    private_network = ''
    if private_network == '0':
        IP_Private = 'Khong co'
    else:
        try:
            IP_Private = connect.get_server(serverVM.id).networks[user.username][0]
        except:
            IP_Private = ''
    
    if o_s is not None:
        rootpassword = 'Cloud@intercom'
    else:
        rootpassword = root_pass

    ssh_key = ''
    if sshkey == None:
        ssh_key = 'Khong co'
    else:
        ssh_key = sshkey
    message = render_to_string('client/send_info_server.html', {
        'user': user,
        'IP_Public': connect.get_server(serverVM.id).networks[network][0],
        'IP_Private': IP_Private,
        'Key_pair': ssh_key,
        'Pass_Login': rootpassword
    })
    to_email = user.email
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()
    return 'Da tao xong server!'

def deleteServer(svid, svname, user):
    try:
        ops = Ops.objects.get(ip=OPS_IP)
        if not user.check_expired():
            user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
            user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                        project_name=user.username, user_domain_id='default',
                                        project_domain_id='default')
            user.save()
        connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                        project_domain_id='default')
        connect.delete_vm(svid=svid)
        server = Server.objects.get(name=svname, owner=user)
        server.delete()
    except:
        return "Đã có lỗi xảy ra!"
    return 'Da xoa xong'

def home(request):
    user = request.user
    if user.is_authenticated and user.is_adminkvm == False:
        return render(request, 'client/home.html',{'username': mark_safe(json.dumps(user.username)),
                                                    'money': user.money,
                                                    'count_sv': Oders.objects.filter(owner=user).count()
                                                    })
    else:
        return HttpResponseRedirect('/')

def show_instances(request, serverid):
    user = request.user
    if user.is_authenticated and user.is_adminkvm == False:
        if Ops.objects.get(ip=OPS_IP):
            thread = check_ping(host=OPS_IP)
            if thread.run():
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username, project_domain_id='default')
                sv = connect.get_server(serverid=serverid)
        if request.method == 'POST':
            if 'snapshot' in request.POST:
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username, project_domain_id='default')
                svid = request.POST['snapshot']
                try:
                    snapshotname = request.POST['snapshotname']
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
                
                # print(request.POST)
                connect.snapshot_vm(svid=svid, snapshotname=snapshotname)
            elif 'resetpass' in request.POST:
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                svid = request.POST['resetpass']
                newpass = request.POST['pass']
                # print(request.POST)
                try:
                    connect.resetpass(svid=svid, newpass=newpass)
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
            elif 'hardreboot' in request.POST:
                print(request.POST)
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                svid = request.POST['hardreboot']
                try:
                    connect.reboot_vm_hard(svid=svid)
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
            elif 'rebuild' in request.POST:
                # print(request.POST)
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                svid = request.POST['rebuild']
                try:
                    connect.rebuild(svid=svid, image=connect.find_image(request.POST['image']), disk_config=request.POST['disk_partition'])
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
        return render(request, 'client/show_instances.html',{'username': mark_safe(json.dumps(user.username)),
                                                                'servername': sv._info['name'],
                                                                'serverid': sv._info['id'],
                                                                'console': sv.get_console_url("novnc")["console"]["url"],
                                                                'serverip': next(iter(sv.networks.values()))[0],
                                                                'ram': str(connect.find_flavor(id=sv._info['flavor']['id']).ram),
                                                                'vcpus': str(connect.find_flavor(id=sv._info['flavor']['id']).vcpus),
                                                                'disk': str(connect.find_flavor(id=sv._info['flavor']['id']).disk),
                                                                'status': sv._info['status'],
                                                                })
    else:
        return HttpResponseRedirect('/')

def instances(request):
    user = request.user
    if user.is_authenticated and user.is_adminkvm == False:
        if request.method == 'POST':
            if 'image' in request.POST:
                if Ops.objects.get(ip=OPS_IP):
                    # print(request.POST)
                    svname = request.POST['svname']
                    # description = request.POST['description']
                    image = request.POST['image']
                    flavor = request.POST['flavor']
                    private_network = request.POST['private_network']
                    if private_network == '1':
                        private_network = user.username
                    
                    try:
                        sshkey = request.POST['sshkey']
                    except:
                        sshkey = None
                    
                    try:
                        o_s = request.POST['os']
                        root_pass = 'Cloud@intercom'
                    except:
                        o_s = None
                        root_pass = binascii.hexlify(os.urandom(12)).decode("utf-8")
                        cloudinit = "#cloud-config\npassword: "+root_pass+"\nssh_pwauth: True\nchpasswd:\n expire: false"
                    type_disk = request.POST['type_disk']
                    # ram = int(float(request.POST['ram']) * 1024)
                    # vcpus = int(request.POST['vcpus'])
                    # disk = int(request.POST['disk'])

                    # count = int(request.POST['count'])
                    count = 1

                    # if [ram, vcpus, disk] in connect.list_flavor():
                    #     fl = connect.find_flavor(ram=ram, vcpus=vcpus, disk=disk)
                    #     im = connect.find_image(image)
                    #     net = connect.find_network(network)
                    #     connect.createVM(svname=svname, flavor=fl, image=im, network_id=net, max_count=count)
                    # else:
                    #     connect.createFlavor(svname=svname, ram=ram, vcpus=vcpus, disk=disk)
                    #     check = False
                    #     while check == False:
                    #         if connect.find_flavor(ram=ram, vcpus=vcpus, disk=disk):
                    #             check = True
                    #     connect.createVM(svname=svname, flavor=connect.find_flavor(ram=ram, vcpus=vcpus, disk=disk), image=connect.find_image(image), network_id=connect.find_network(network), max_count=count)
                    if svname == '' or image == '' or flavor == '' or request.POST['type_disk'] == '':
                        return HttpResponse('Xay ra loi khi tao Server!')
                    price = 0
                    if type_disk == DISK_HDD:
                        price = (int(flavor.split(',')[0]) * PRICE_RAM + int(flavor.split(',')[1]) * PRICE_VCPUS + int(flavor.split(',')[2]) * PRICE_DISK_HDD) * count
                    elif type_disk == DISK_SSD:
                        price = (int(flavor.split(',')[0]) * PRICE_RAM + int(flavor.split(',')[1]) * PRICE_VCPUS + int(flavor.split(',')[2]) * PRICE_DISK_SSD) * count
                    if price > float(user.money):
                        return HttpResponse("Vui long nap them tien vao tai khoan!")
                    try:
                        Server.objects.get(name=svname, owner=user)
                        return HttpResponse('Tên server bị trùng!')
                    except:
                        pass
                    if o_s is None:
                        x = q.enqueue(createServer, type_disk, flavor, image, svname, private_network, count, user, root_pass, price, o_s, cloudinit, sshkey)
                    else:
                        x = q.enqueue(createServer, type_disk, flavor, image, svname, private_network, count, user, root_pass, price, o_s)
                    # createServer(type_disk=type_disk, flavor=flavor, image=image, svname=svname, private_network=private_network, cloudinit=cloudinit, sshkey=sshkey, count=count, user=user, root_pass=root_pass, price=price)
                    return HttpResponse(x.id)
                else:
                    return HttpResponseRedirect('/')
            elif 'delete' in request.POST:
                svid = request.POST['delete']
                svname = request.POST['svname']
                y = q.enqueue(deleteServer, svid, svname, user)
                return HttpResponse(y.id)
            elif 'start' in request.POST:
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                svid = request.POST['start']
                try:
                    connect.start_vm(svid=svid)
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
            elif 'reboot' in request.POST:
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                svid = request.POST['reboot']
                try:
                    connect.reboot_vm(svid=svid)
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
                
                # server = Server.objects.get(name=request.POST['svname'])
                # server.delete()
            elif 'stop' in request.POST:
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                svid = request.POST['stop']
                try:
                    connect.stop_vm(svid=svid)
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
                
                # server = Server.objects.get(name=request.POST['svname'])
                # server.delete()
            elif 'snapshot' in request.POST:
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                svid = request.POST['snapshot']
                snapshotname = request.POST['snapshotname']
                # print(request.POST)
                try:
                    connect.snapshot_vm(svid=svid, snapshotname=snapshotname)
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
                
                # server = Server.objects.get(name=request.POST['svname'])
                # server.delete()
            elif 'backup' in request.POST:
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                svid = request.POST['backup']
                backup_name = request.POST['backupname']
                backup_type = request.POST['backup_type']
                rotation = request.POST['rotation']
                # print(request.POST)
                try:
                    connect.backup_vm(svid=svid, backup_name=backup_name, backup_type=backup_type, rotation=rotation)
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
                
                # server = Server.objects.get(name=request.POST['svname'])
                # server.delete()
            elif 'sshkeyname' in request.POST:
                try:
                    Sshkeys.objects.get(name=request.POST['sshkeyname'])
                    return HttpResponse('Tên ssh key đã tồn tại!')
                except:
                    pass
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                sshkeyname = request.POST['sshkeyname']
                # print(request.POST)
                try:
                    key = connect.create_sshkey(sshkeyname=sshkeyname)
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
                mail_subject = 'Thông tin key pair: '+sshkeyname
                message = render_to_string('client/send_info_key.html', {
                    'user': user,
                    'private_key': key.private_key,
                    'public_key': key.public_key,
                    'key_name': key.name
                })
                to_email = user.email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                thread = EmailThread(email)
                thread.start()
                Sshkeys.objects.create(ops=ops, name=sshkeyname,owner=user)
        images = []
        sshkeys = []
        for im in Images.objects.filter(ops=Ops.objects.get(ip=OPS_IP)).values('name'):
            images.append((im['name']))
        for sshkey in Sshkeys.objects.filter(ops=Ops.objects.get(ip=OPS_IP), owner=user).values('name'):
            sshkeys.append((sshkey['name']))
        return render(request, 'client/instances.html',{'username': mark_safe(json.dumps(user.username)),
                                'DISK_SSD': DISK_SSD,
                                'DISK_HDD': DISK_HDD,
                                'flavors': Flavors.objects.filter(ops=Ops.objects.get(ip=OPS_IP)),
                                'images': images,
                                'sshkeys': sshkeys
                                })
    else:
        return HttpResponseRedirect('/')

def home_data(request):
    user = request.user

    # ip = OPS_IP
    # username = 'admin'
    # password = 'ok123'
    # project_name = 'admin'
    # user_domain_id = 'default'
    # project_domain_id = 'default'
    # connect = keystone(ip=ip, username=username, password=password, project_name=project_name, user_domain_id=user_domain_id, project_domain_id=project_domain_id)
    # # connect.add_user_to_project()
    # connect.get_role()
    if user.is_authenticated and user.is_adminkvm == False:
        if Ops.objects.get(ip=OPS_IP):
            thread = check_ping(host=OPS_IP)
            if thread.run():
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                # print(connect.find_hypervisor('2'))
                data = []
                for item in connect.list_server():
                    # print(item.status)
                    # print(dir(item))
                    # print(item.networks)
                    try:
                        name = '''<a href="/client/show_instances/'''+item._info['id']+'''"><p>'''+item._info['name']+'''</p></a>'''
                    except:
                        name = '<p></p>'

                    try:
                        ip = '<p>'
                        for key, value in item.networks.items():
                            ip += key + '<br>'
                            for i_p in value:
                                ip += i_p + '<br>'
                        ip += '</p>'
                    except:
                        ip = '<p></p>'
                    try:
                        ram = '<p>'+str(connect.find_flavor(id=item._info['flavor']['id']).ram)+'</p>'
                    except:
                        ram = '<p></p>'
                    try:
                        vcpus = '<p>'+str(connect.find_flavor(id=item._info['flavor']['id']).vcpus)+'</p>'
                    except:
                        vcpus = '<p></p>'
                    try:
                        xx = Server.objects.get(name=item._info['name'], owner=user)
                        disk = '<p>'+str(xx.disk)+'</p>'
                    except:
                        disk = '<p>'+str(connect.find_flavor(id=item._info['flavor']['id']).disk)+'</p>'
                    try:
                        if item._info['status'] == 'ACTIVE':
                            status = '<span class="label label-success">'+item._info['status']+'</span>'
                            try:
                                actions = '''
                                <div>
                                    <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown">
                                    Actions <span class="caret"></span></button>
                                    <ul class="dropdown-menu dropdown-menu-right" role="menu" id= "nav_ul" style="position: relative !important;">
                                        <li>
                                            <a data-batch-action="true" class="data-table-action control" name="'''+item._info['name']+'''" id="del_'''+item._info['id']+'''" type="submit"> Delete Instance</a>
                                        </li>
                                        <li>
                                            <a data-batch-action="true" data-toggle="modal" data-target="#backup" class="data-table-action control" name="'''+item._info['name']+'''" id="backup_'''+item._info['id']+'''" type="submit" data-backdrop="false">Backup</a>
                                        </li>
                                        <li>
                                            <a data-batch-action="true" class="data-table-action console" data-title="console" id="'''+item.get_console_url("novnc")["console"]["url"]+'''" type="submit"> Console Instance</a>
                                        </li>
                                        <li>
                                            <a data-batch-action="true" class="data-table-action control" name="'''+item._info['name']+'''" id="reboot_'''+item._info['id']+'''" type="submit"> Reboot Instance</a>
                                        </li>
                                        <li>
                                            <a data-batch-action="true" class="data-table-action control" name="'''+item._info['name']+'''" id="stop_'''+item._info['id']+'''" type="submit"> Stop Instance</a>
                                        </li>

                                    </ul>
                                <div>
                                '''
                            except:
                                actions = '''
                                <div>
                                    <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown">
                                    Actions <span class="caret"></span></button>
                                    <ul class="dropdown-menu dropdown-menu-right" role="menu" id= "nav_ul" style="position: relative !important;">
                                        <li>
                                            <a data-batch-action="true" class="data-table-action control" name="'''+item._info['name']+'''" id="del_'''+item._info['id']+'''" type="submit"> Delete Instance</a>
                                        </li>
                                        <li>
                                            <a data-batch-action="true" data-toggle="modal" data-target="#backup" class="data-table-action control" name="'''+item._info['name']+'''" id="backup_'''+item._info['id']+'''" type="submit" data-backdrop="false">Backup</a>
                                        </li>
                                        <li>
                                            <a data-batch-action="true" class="data-table-action control" name="'''+item._info['name']+'''" id="reboot_'''+item._info['id']+'''" type="submit"> Reboot Instance</a>
                                        </li>
                                        <li>
                                            <a data-batch-action="true" class="data-table-action control" name="'''+item._info['name']+'''" id="stop_'''+item._info['id']+'''" type="submit"> Stop Instance</a>
                                        </li>
                                    </ul>
                                <div>
                                '''
                        elif item._info['status'] == 'SHUTOFF':
                            status = '<span class="label label-danger">'+item._info['status']+'</span>'
                            actions = '''
                                <div class='nav-item'>
                                    <button type="button" class="btn btn-primary dropdown-toggle nav-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    Actions <span class="caret"></span></button>
                                    <ul class="dropdown-menu dropdown-menu-right" role="menu" id= "nav_ul">
                                        <li>
                                            <a data-batch-action="true" class="data-table-action control" name="'''+item._info['name']+'''" id="del_'''+item._info['id']+'''" type="submit"> Delete Instance</a>
                                        </li>
                                        <li>
                                            <a data-batch-action="true" data-toggle="modal" data-target="#snapshot" class="data-table-action control" name="'''+item._info['name']+'''" id="snapshot_'''+item._info['id']+'''" type="submit" data-backdrop="false"> Create Snapshot</a>
                                        </li>
                                        <li>
                                            <a data-batch-action="true" class="data-table-action control" name="'''+item._info['name']+'''" id="start_'''+item._info['id']+'''" type="submit"> Start Instance</a>
                                        </li>
                                    </ul>
                                <div>
                                '''
                        elif item._info['status'] == 'BUILD':
                            status = '<p>BUILD</p><div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated active" style="width:100%"></div></div>'
                            actions = '''
                                <div class='nav-item'>
                                    <button type="button" class="btn btn-primary dropdown-toggle nav-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    Actions <span class="caret"></span></button>
                                    <ul class="dropdown-menu dropdown-menu-right" role="menu" id= "nav_ul">
                                        <li>
                                            <a data-batch-action="true" class="data-table-action control" name="'''+item._info['name']+'''" id="del_'''+item._info['id']+'''" type="submit"> Delete Instance</a>
                                        </li>
                                    </ul>
                                <div>
                                '''
                        else:
                            status = '<span class="label label-danger">'+item._info['status']+'</span>'
                            actions = '''
                                <div class='nav-item'>
                                    <button type="button" class="btn btn-primary dropdown-toggle nav-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    Actions <span class="caret"></span></button>
                                    <ul class="dropdown-menu dropdown-menu-right" role="menu" id= "nav_ul">
                                        <li>
                                            <a data-batch-action="true" class="data-table-action control" name="'''+item._info['name']+'''" id="del_'''+item._info['id']+'''" type="submit"> Delete Instance</a>
                                        </li>
                                    </ul>
                                <div>
                                '''
                    except:
                        status = '<span class="label label-danger"></span>'
                        actions = ''
                    try:
                        created = '<p>'+item._info['created']+'</p>'
                    except:
                        created = '<p></p>'
                    
                    # data.append([host, name, image_name, ip, network, flavor, status, created, actions])
                    data.append([name, ip, ram, vcpus, disk, status, created, actions])
                big_data = {"data": data}
                json_data = json.loads(json.dumps(big_data))
                return JsonResponse(json_data)
            else:
                data = []
                data.append(['<p></p>', '<p></p>', '<p></p>', '<p></p>', '<p></p>', '<p></p>', '<p></p>', '<p></p>'])
                big_data = {"data": data}
                json_data = json.loads(json.dumps(big_data))
                return JsonResponse(json_data)

def networks(request):
    user = request.user
    if user.is_authenticated and user.is_adminkvm == False:
        return render(request, 'client/networks.html',{'username': mark_safe(json.dumps(user.username)),
                                'networks': Networks.objects.filter(owner=user)
                                })
    else:
        return HttpResponseRedirect('/')

def sshkeys(request):
    user = request.user
    if user.is_authenticated and user.is_adminkvm == False:
        if request.method == 'POST':
            if 'sshkeyname' in request.POST:
                try:
                    Sshkeys.objects.get(name=request.POST['sshkeyname'])
                    return HttpResponse('Tên ssh key đã tồn tại!')
                except:
                    pass
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                sshkeyname = request.POST['sshkeyname']
                # print(request.POST)
                try:
                    key = connect.create_sshkey(sshkeyname=sshkeyname)
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
                mail_subject = 'Thông tin key pair: '+sshkeyname
                message = render_to_string('client/send_info_key.html', {
                    'user': user,
                    'private_key': key.private_key,
                    'public_key': key.public_key,
                    'key_name': key.name
                })
                to_email = user.email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                thread = EmailThread(email)
                thread.start()
                Sshkeys.objects.create(ops=ops, name=sshkeyname,owner=user)
            elif 'delete_sshkey' in request.POST:
                try:
                    Sshkeys.objects.get(name=request.POST['delete_sshkey'])
                except:
                    return HttpResponse('Tên ssh key không tồn tại!')
                ops = Ops.objects.get(ip=OPS_IP)
                if not user.check_expired():
                    user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                    user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                             project_name=user.username, user_domain_id='default',
                                             project_domain_id='default')
                    user.save()
                connect = nova(ip=OPS_IP, token_id=user.token_id, project_name=user.username,
                               project_domain_id='default')
                sshkeyname = request.POST['delete_sshkey']
                try:
                    key = connect.delete_sshkey(sshkeyname=sshkeyname)
                    Sshkeys.objects.get(name=request.POST['delete_sshkey']).delete()
                except:
                    return HttpResponse("Đã có lỗi xảy ra!")
        return render(request, 'client/sshkeys.html',{'username': mark_safe(json.dumps(user.username)),
                                'sshkeys': Sshkeys.objects.filter(owner=user)
                                })
    else:
        return HttpResponseRedirect('/')

def volumes(request):
    user = request.user
    if user.is_authenticated and user.is_adminkvm == False:
        return render(request, 'client/volumes.html',{'username': mark_safe(json.dumps(user.username)),
                                })
    else:
        return HttpResponseRedirect('/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_profile(request):
    user = request.user
    if user.is_authenticated and user.is_adminkvm == False:
        return render(request, 'client/profile.html', {'username': mark_safe(json.dumps(user.username))})
    else:
        return HttpResponseRedirect('/')

def user_oders(request):
    user = request.user
    oders = Oders.objects.filter(owner=user)
    if user.is_authenticated and user.is_adminkvm == False:
        return render(request, 'client/oders.html', {'username': mark_safe(json.dumps(user.username)), 'oders': oders})
    else:
        return HttpResponseRedirect('/')
