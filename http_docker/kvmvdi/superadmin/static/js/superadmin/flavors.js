$(document).ready(function(){
    $("#flavor_submit").click(function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var flavorname = $("input[name=flavorname]").val();
        var ram = $("input[name=ram1]").val();
        var vcpus = $("input[name=vcpus1]").val();
        var disk = $("input[name=disk1]").val();
        $.ajax({
            type:'POST',
            url:location.href,
            data: {'csrfmiddlewaretoken':token, 'ram': ram, 'vcpus': vcpus,'disk': disk, 'flavorname': flavorname},
        });
        document.getElementById("close_modal_flavor").click();
        setTimeout(function(){
            $("body .list_flavors").load(location.href + " .list_flavors");
        }, 1000);
    });


    $("#flavor").on('show.bs.modal', function(event){
        $("input[name=ram]").val("1");
        $("input[name=vcpus]").val("1");
        $("input[name=disk]").val("20");
    });

    $("body").on('click', '.delete_flavor', function(){
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var flavorid = $(this).attr('id');
        swal({
                title: 'Are you sure?',
                type: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes!'
            }).then(function(result){
                if(result.value){
                    swal({
                                imageUrl: '/static/images/spinner-sample.gif',
                                imageHeight: 120,
                                imageAlt: 'wait',
                                title: "Please wait...",
                                title: "Please wait...",
                                showConfirmButton: false
                            });
                    $.ajax({
                        type:'POST',
                        url:location.href,
                        data: {'flavorid':flavorid, 'csrfmiddlewaretoken':token},
                        success: function(msg){
                            if ((msg == 'Xảy ra lỗi! Vui lòng thử lại sau!') || (msg == 'Tên flavor không tồn tại!')){
                                swal({
                                    type: 'error',
                                    title: msg,
                                });
                            }else{
                                swal.close();
                                $("body .list_flavor_client").load(location.href + " .list_flavor_client");
                            }
                        }
                    });
                }
            });
    });
});