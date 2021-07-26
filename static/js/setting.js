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
                    alert('수락하였습니다.');
                    window.location.reload();
                }else{
                    alert('실패하였습니다.');
                }
            },
            error: function (e) {
                console.log(e);
                alert('false');
            }
        });
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
            console.log(e);
            alert('실패');
        }
    }

    )

});
var clickch = 0;
function userdetail(id) {
    if(clickch ==0){
        $.ajax({
        url : "/setting/userdetailtest/"+id,
        type : "POST",
        cache :false,
        data : {},
        dataType:"json",
        async: false,
        success: function (res) {
            $('#userdetail').css('display','block');
            $('#userdphone').val(res.user.dephone);
            $('#userdemail').val(res.user.deemail);
            $('#userids').val(res.user.deuserdid);
            var userType = "";
                    if(res.user.delevel == 3){
                        userType += "<option value='3'>총관리자</option><option value='2'>관리자</option><option value='1'>작업자</option>";
                    }if(res.user.delevel == 2){
                        userType += "<option value='2'>관리자</option><option value='3'>총관리자</option><option value='1'>작업자</option>";
                    }if(res.user.delevel == 1) {
                        userType += "<option value='1'>작업자</option><option value='3'>총관리자</option><option value='2'>관리자</option>";
                    }
                    $('#userdlevel').append(userType);
                    $('#userdid').append("<h3>"+res.user.dename+"("+res.user.deusername+")"+"</h3>");
                    $('#userimg').find('img').attr('src', res.user.deuserimg);
                    clickch = 1;
            },
        });
    }
}
function usermodelclose() {
    $('#userdetail').css('display','none');
    window.location.reload();
}
function usermodelupdate() {
    userid = $('#userids').val();
    userlevel = $('#userdlevel').val();
    userdphone = $('#userdphone').val();
    userdemail = $('#userdemail').val();
    $.ajax({
        url: "/setting/userupdate",
        type : "POST",
        cache :false,
        data : {'userid':userid,'userlevel':userlevel,'userdphone':userdphone,'userdemail':userdemail},
        dataType:"json",
        async: false,
        complete:function () {
            alert('수정되었습니다')
        }
    });
}
function userdelete() {
    userid = $('#userids').val();
    $.ajax({
        url:"/setting/userdel",
        type:"POST",
        cache:false,
        data:{'userid':userid},
        dataType:"json",
        async:true,
        complete:function () {
            alert('삭제 되었습니다');
            window.location.reload();
        }
    });

}
function langchange() {
    var lang_theme = $('input[name=lang_theme]:checked').val();
    $.ajax({
        url:"/setting/languagech",
        type:"POST",
        cache:false,
        data:{'lang':lang_theme},
        dataType:"json",
        async:false,
        success:function () {
            window.location.reload();
        },
        error:function () {
            alert('다시 시도해 주세요');
        }
    });

}
function accountselect(id){
    $.ajax({
        url:"/setting/accountselect",
        type:"POST",
        cache:false,
        data:{'accountid':id},
        dataType:"json",
        async:false,
        success:function(res) {
            $('#accountid').val(res.accountinfo.accountid);
            $('#accountname').val(res.accountinfo.accountname);
            $('#accountmanage').val(res.accountinfo.accountmanager);
            $('#accountwork').val(res.accountinfo.accountwork);
            $('#accounttype').val(res.accountinfo.accounttype);
            $('#accountnum').val(res.accountinfo.accountnum);
            $('#accountaddress').val(res.accountinfo.accountaddress);
        },
        error:function () {
            alert('거래처 정보를 불러오는데 실패했습니다.')
        }
    });
}
function accountmodi(){
    accountidd = $('#accountid').val();
    accountnamed = $('#accountname').val();
    accountmanaged = $('#accountmanage').val();
    accountworkd = $('#accountwork').val();
    accounttyped = $('#accounttype').val();
    accountnumd = $('#accountnum').val();
    accountaddressd = $('#accountaddress').val();
    $.ajax({
        url:'/setting/accountmodify',
        type:"POST",
        cache:false,
        data:{'accountname':accountnamed,'accountmanage':accountmanaged,'accountwork':accountworkd,
            'accountnum':accountnumd,'accounttype':accounttyped,'accountaddress':accountaddressd,
            'accountidd':accountidd},
        dataType:"json",
        async:false,
        complete:function () {
            alert('거래처 정보가 수정되었습니다');
            window.location.reload();
        }
    });
}
function accountdel(){
    id =$('#accountid').val();
    $.ajax({
        url:'/setting/accountdel',
        type:'POST',
        data:{'accountid':id},
        dataType:'json',
        cache:false,
        async:false,
        complete:function () {
            alert('삭제 되었습니다');
            window.location.reload();
        }
    });
}

$(document).ready(function(){
    $("input#accountnum").blur(function(){
    	var num = $("#accountnum").val();
    	blur(num);
    });
    $("input#accountnum").click(function(){
    	var num = $("#accountnum").val();
    	focus(num);
    });
});
function focus(num) {
	num = num.replace(/[^0-9]/g, '');
	$("#accountnum").val(num);
};
function blur(num) {
	num = num.replace(/[^0-9]/g, '');
	var tmp = '';
	tmp += num.substr(0, 3);
	tmp += '-';
	tmp += num.substr(3, 2);
	tmp += '-';
	tmp += num.substr(7);
	$("#accountnum").val(tmp);
	if ($('#accountnum').val().length===2){
	    $('#accountnum').val('');
    }
};



