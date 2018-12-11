$(document).ready(function(){
    $("#i_submit").click(function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var svname = $("input[name=svname]").val();
        // var description = $("input[name=description]").val();
        // var rootpass = $("input[name=rootpass]").val();
        // var image = document.getElementById("mySelect_image").value;
        var type_disk = document.getElementById("type_disk").value;
        var private_network;
        if ($('#private_network input:checkbox').is(":checked")){
            private_network = 1;
        }else{
            private_network = 0;
        }
        var image;
        var flavor;
        var sshkey;
        $('.image_select input[name="image"]').each(function() {
            if ($(this).is(':checked')){
                image = $(this).val();
            }
        });

        $('.snapshot_select input[name="sn"]').each(function() {
            if ($(this).is(':checked')){
                image = $(this).val();
            }
        });
        
        // var flavor = document.getElementById("mySelect").value;
        $('.flavor_select').find('label').children().each(function() {
            if ($(this).is(':checked')){
                flavor = $(this).val();
            }
        });

        $('.sshkey_select').find('label').children().each(function() {
            if ($(this).is(':checked')){
                sshkey = $(this).val();
            }
        });


        // var ram = $("input[name=ram]").val();
        // var vcpus = $("input[name=vcpus]").val();
        // var disk = $("input[name=disk]").val();
        var count = $("input[name=count]").val();
        var price = $("input[name=price]").val();
        if ((svname == '') || (type_disk == '') || (price == '') || (image == '') || (flavor == '') || (count == '')){
            swal({
                type: 'warning',
                title: "Vui lòng điền đầy đủ thông tin",
            });
        }else{
            swal({
                imageUrl: '/static/images/spinner-sample.gif',
                imageHeight: 120,
                imageAlt: 'wait',
                title: "Please wait...",
                showConfirmButton: false
            });
            document.getElementById("close_modal").click();
            if ((image.includes("wi")) || (image.includes("Wi"))){
                $.ajax({
                    type:'POST',
                    url:location.href,
                    data: {'svname': svname, 'type_disk': type_disk, 'private_network': private_network, 'os': 'win', 'price': price, 'csrfmiddlewaretoken':token, 'image': image, 'flavor': flavor},
                    success: function(msg){
                        if ((msg == "Vui long nap them tien vao tai khoan!") || (msg == "Dung luong disk qua nho!") || (msg == "No IP availability!") || (msg == "Xay ra loi khi tao volume!")  || (msg == "Xay ra loi khi tao Server!") || (msg == "Xay ra loi khi check flavor!") || (msg == "Xay ra loi khi check image!") || (msg == "Xay ra loi khi check network!") || (msg == "Tên server bị trùng!")){
                        // if (msg != ''){
                            swal({
                                type: 'warning',
                                title: msg,
                            });
                        }else{
                            swal.close();
                            $("#success").html('Tao server thanh cong!').removeClass("hide").hide().fadeIn()
                            setTimeout(function(){
                                $("#success").fadeOut("slow");
                                opsSocket.send(JSON.stringify({
                                    'message' : msg,
                                }));
                            }, 4000);
                            setTimeout(function(){
                                $('.list_vm_client').DataTable().ajax.reload(null,false);
                            }, 6000);
                        }
                    },
                });
            }else{
                $.ajax({
                    type:'POST',
                    url:location.href,
                    data: {'svname': svname, 'type_disk': type_disk, 'private_network': private_network, 'sshkey': sshkey, 'price': price, 'csrfmiddlewaretoken':token, 'image': image, 'flavor': flavor},
                    success: function(msg){
                        if ((msg == "Vui long nap them tien vao tai khoan!") || (msg == "Dung luong disk qua nho!") || (msg == "No IP availability!") || (msg == "Xay ra loi khi tao volume!")  || (msg == "Xay ra loi khi tao Server!") || (msg == "Xay ra loi khi check flavor!") || (msg == "Xay ra loi khi check image!") || (msg == "Xay ra loi khi check network!") || (msg == "Tên server bị trùng!")){
                        // if (msg != ''){
                            swal({
                                type: 'warning',
                                title: msg,
                            });
                        }else{
                            swal.close();
                            $("#success").html('Tao server thanh cong!').removeClass("hide").hide().fadeIn()
                            setTimeout(function(){
                                $("#success").fadeOut("slow");
                                opsSocket.send(JSON.stringify({
                                    'message' : msg,
                                }));
                            }, 6000);
                            setTimeout(function(){
                                $('.list_vm_client').DataTable().ajax.reload(null,false);
                            }, 6000);
                        }
                    },
                });
            }
        }

    });

    $("#id02").on('show.bs.modal', function(event){
        var button = $(event.relatedTarget);
        var project = button.data('project');
        $("input[name=project]").val(project);
        $("input[name=svname]").val("");
        $("input[name=description]").val("");
        $("input[name=ram]").val("0.5");
        $("input[name=vcpus]").val("1");
        $("input[name=disk]").val("20");
        $("input[name=count]").val("1");
        // opsSocket.send(JSON.stringify({
        //     'message' : ip+'abcxyz'+userName,
        // }));
    });

    $('body .price').change(function(){
        var flavor;
        $('.flavor_select input[name="image"]').each(function() {
            if ($(this).is(':checked')){
                flavor = $(this).val();
            }
        });
        var ram = flavor.split(',')[0];
        var vcpus = flavor.split(',')[1];
        var disk = flavor.split(',')[2];
        var count = $("body input[name=count]").val();
        var type_disk = document.getElementById("type_disk").value;
        var price_new;
        if (type_disk == 'ceph-hdd'){
            price_new = (parseInt(ram) * 50000 + parseInt(vcpus) * 60000 + parseInt(disk) * 3000) * parseInt(count);
        }else{
            price_new = (parseInt(ram) * 50000 + parseInt(vcpus) * 60000 + parseInt(disk) * 5000) * parseInt(count);
        }
        $("body input[name=price]").val(price_new);
    });

    $('body .flavor_').click(function(){
        var flavor = $(this).prev().val();
        var ram = flavor.split(',')[0];
        var vcpus = flavor.split(',')[1];
        var disk = flavor.split(',')[2];
        // var count = $("body input[name=count]").val();
        var type_disk = document.getElementById("type_disk").value;
        var price_new;
        if (type_disk == 'ceph-hdd'){
            price_new = (parseInt(ram) * 50000 + parseInt(vcpus) * 60000 + parseInt(disk) * 3000);
        }else{
            price_new = (parseInt(ram) * 50000 + parseInt(vcpus) * 60000 + parseInt(disk) * 5000);
        }
        $("body input[name=price]").val(price_new);
    });

    $('body .hide_image').click(function(){
        var image = $(this).prev().data('name');
        if ((image.includes("wi")) || (image.includes("Wi"))){
            $('.flavor_select input[name="image"]').each(function() {
                $(this).prop('checked',false);
            });
            $('.sshkey_hide').hide();
            $('.price_step').text('6');
            $('body .disk_').each(function(){
                var disk = $(this).text().split(' GB disk')[0];
                if (parseInt(disk) < 30){
                    $(this).parent().parent().parent().hide();
                }
            });
        }else{
            $('.flavor_select input[name="image"]').each(function() {
                $(this).prop('checked',false);
            });
            $('.sshkey_hide').show();
            $('.price_step').text('7');
            $('body .disk_').each(function(){
                $(this).parent().parent().parent().show();
            });
        }
    });

    $('#type_disk').on('change', function() {
        var flavor;
        $('.flavor_select').find('label').children().each(function() {
            if ($(this).is(':checked')){
                flavor = $(this).val();
            }
        });
        var ram = flavor.split(',')[0];
        var vcpus = flavor.split(',')[1];
        var disk = flavor.split(',')[2];
        var type_disk = document.getElementById("type_disk").value;
        var price_new;
        if (type_disk == 'ceph-hdd'){
            price_new = (parseInt(ram) * 50000 + parseInt(vcpus) * 60000 + parseInt(disk) * 3000);
        }else{
            price_new = (parseInt(ram) * 50000 + parseInt(vcpus) * 60000 + parseInt(disk) * 5000);
        }
        $("body input[name=price]").val(price_new);
    });

    $('#type_image').on('change', function() {
        $('.image_select input[name="image"]').each(function() {
            $(this).prop('checked',false);
        });
        $('.snapshot_select input[name="sn"]').each(function() {
            $(this).prop('checked',false);
        });
        var type_image = $(this).val();
        if (type_image == 'snapshot'){
            $('.snapshot_select').show();
            $('.image_select').hide();
        }else if (type_image == 'image'){
            $('.image_select').show();
            $('.snapshot_select').hide();
        }
    });

    $('#close_modal_sshkey').click(function(){
        setTimeout(function(){
            $("#create_vm").click();
        }, 1000);
    });

    $(".seepass").on('click',function(){ 
        var x = document.getElementById("password");
        if (x.type === "password") {
            x.type = "text";
        } else {
            x.type = "password";
        }
    });
});
