$(document).ready(function(){
    $("body").on('click', '.delete_user', function(){
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var userid = $(this).attr('id');
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
                        data: {'userid':userid, 'csrfmiddlewaretoken':token},
                        success: function(msg){
                            if ((msg == 'Xảy ra lỗi! Vui lòng thử lại sau!') || (msg == 'Tên user không tồn tại!')){
                                swal({
                                    type: 'error',
                                    title: msg,
                                });
                            }else{
                                swal.close();
                                $("body .list_user_client").load(location.href + " .list_user_client");
                            }
                        }
                    });
                }
            });
    });
});