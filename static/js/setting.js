function activeUser(id){
    var result = confirm('수락하시겠습니까?');
    if(result){
        $.ajax({
            url: '/setting/activeUser',
            type: 'POST',
            cache: false,
            data: { id: id },
            dataType: 'json',
            async: false,
            success: function (response) {
                if(response.success){
                    alert('수락하였습니다.')
                }else{
                    alert('실패하였습니다.')
                }
            },
            error: function (e) {
                console.log(e)
                alert('false')
            }
        })
    }
}

$("#activeUser").click(function () {
    var id = $("#userid").val();
    $.ajax({
        url : "/setting/activeUser",
        type : "POST",
        cache : false,
        data : {id:id},
        dataType: "json",
        success : function () {
            alert('수락');
        },
        error : function (e) {
            console.log(e)
            alert('실패');
        }
    }

    )

});