$(document).ready(function(){
    $("#flavor_submit").click(function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var flavorname = $("input[name=flavorname]").val();
        var ram = $("input[name=ram1]").val();
        var vcpus = $("input[name=vcpus1]").val();
        var disk = $("input[name=disk1]").val();
        var type_disk = document.getElementById("type_disk").value;
        $.ajax({
            type:'POST',
            url:location.href,
            data: {'csrfmiddlewaretoken':token, 'ram': ram, 'vcpus': vcpus,'disk': disk, 'type_disk': type_disk, 'flavorname': flavorname},
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
});