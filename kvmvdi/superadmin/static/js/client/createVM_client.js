$(document).ready(function(){
    $("#i_submit").click(function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var svname = $("input[name=svname]").val();
        var description = $("input[name=description]").val();
        var rootpass = $("input[name=rootpass]").val();
        // var image = document.getElementById("mySelect_image").value;
        var type_disk = document.getElementById("type_disk").value;
        var private_network;
        if ($('#private_network').checked == true){
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
        
        
        var project = $("input[name=project]").val();
        // var flavor = document.getElementById("mySelect").value;
        $('.flavor_select').find('label').children().each(function() {
            if ($(this).is(':checked')){
                flavor = $(this).val().replace("[", "");
                flavor = flavor.replace("]", "");
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
        if ((svname == '') || (type_disk == '') || (price == '') || (image == '') || (flavor == '') || (count == '') || (rootpass == '')){
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
            $.ajax({
                type:'POST',
                url:location.href,
                data: {'svname': svname, 'type_disk': type_disk, 'private_network': private_network, 'rootpass': rootpass, 'sshkey': sshkey, 'price': price, 'description': description, 'csrfmiddlewaretoken':token, 'image': image, 'flavor': flavor, 'count': count, 'project': project},
                success: function(msg){
                    if ((msg == "Vui long nap them tien vao tai khoan!") || (msg == "No IP availability!") || (msg == "Xay ra loi khi tao volume!")  || (msg == "Xay ra loi khi tao Server!") || (msg == "Xay ra loi khi check flavor!") || (msg == "Xay ra loi khi check image!") || (msg == "Xay ra loi khi check network!") || (msg == "Tên server bị trùng!")){
                        swal({
                            type: 'warning',
                            title: msg,
                        });
                    }else{
                        setTimeout(function(){
                            $('.list_vm_client').DataTable().ajax.reload(null,false);
                            swal.close();
                        }, 0);
                    }
                 },
            });
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
                flavor = $(this).val().replace("[", "");
                flavor = flavor.replace("]", "");
            }
        });
        var ram = flavor.split(',')[0];
        var vcpus = flavor.split(',')[1];
        var disk = flavor.split(',')[2];
        var count = $("body input[name=count]").val();
        var price_new = ((parseInt(ram)/1024) * 3 + parseInt(vcpus) * 2 + parseInt(disk) * 1) * parseInt(count) * 10000;
        $("body input[name=price]").val(price_new);
    });
    

    $('body .flavor_').click(function(){
        var flavor = $(this).prev().val().replace("[", "");
        flavor = flavor.replace("]", "");
        var ram = flavor.split(',')[0];
        var vcpus = flavor.split(',')[1];
        var disk = flavor.split(',')[2];
        var count = $("body input[name=count]").val();
        var price_new = ((parseInt(ram)/1024) * 3 + parseInt(vcpus) * 2 + parseInt(disk) * 1) * parseInt(count) * 10000;
        $("body input[name=price]").val(price_new);
    });

    $('#close_modal_sshkey').click(function(){
        setTimeout(function(){
            $("#create_vm").click();
        }, 1000);
    });

});