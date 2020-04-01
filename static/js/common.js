var mou = 0;
$(function(){
    $('.alram').mouseover(function(){
       mou=1;
       console.log(mou);
    });
    $('.alram').mouseleave(function(){
       mou=0;
       console.log(mou);
    });

});

function closeMask(){
    activeModal = $('.modalOn');
    $(activeModal).removeClass('modalOn');
    $(activeModal).addClass('modalOff')

}


function alrammove() {

    $('.alram').css({"right":"0px", "transition":"1s"});
    $('#gnb').css({"margin-left":"-240px", "transition":"1s"});
    $('#contentsWrap').css({"margin-left": "0px", "transition":"1s"});
    $('#orderContentWrap').css({"margin-left": "0px", "transition":"1s"});
    $('#settingContentWrap').css({"margin-left":"0px", "transition":"1s"});
    $('#ContentWrap').css({"margin-left":"0px", "transition":"1s"});
}
function alramout() {

    if(mou == 0) {

        $('.alram').css({"right":"-300px", "transition":"1s"});
        $('#gnb').css({"margin-left":"0px", "transition":"1s"});
        $('#contentsWrap').css({"margin-left": "240px", "transition":"1s"});
        $('#orderContentWrap').css({"margin-left": "240px", "transition":"1s"});
        $('#settingContentWrap').css({"margin-left":"240px", "transition":"1s"});
        $('#ContentWrap').css({"margin-left":"240px", "transition":"1s"});

    }

}

function cheakchange() {

    var oid = $('#orderidval').val();

    $.ajax({
        url:"ordercheack",
        type : "POST",
        datatype : "json",
        data : {oid: oid},
        success : function () {
            $.ajax({
                url:'/order/detail/'+oid,
                type : "POST",
                datatype: "json",
                success : function (res) {
                    $('#mask').css('display','block');
                    $('#detailOrderModal').css('display','block');
                    $('#detailSubOrder').empty();
                    $('#detailCompany').val(res.order.company);
                    $('#detailCode').val(res.order.code);
                    $('#detailBuyer').val(res.order.buyer);
                    $('#detailManager').val(res.order.Manager);
                    $('#detailOrderDate').val(res.order.order_date);
                    $('#detailDueDate').val(res.order.due_date);
                    $('#detailRound').val(res.order.order_round);
                    $('#detailManager').val(res.order.manager);
                    $('#oid').val(oid);
                    console.log(res);

                    var orderType = "detailOrderType";
                    if(res.order.type == 0){
                        orderType += "<option value='0'>샘플</option><option value='1'>메인</option>";
                    }else{
                        orderType += "<option value='1'>메인</option><option value='0'>샘플</option>";
                    }

                    var orderInout = "";
                    if(res.order.order_inout == 0){
                        orderInout += "<option value='0'>내수</option><option value='1'>외수</option>";
                    }else{
                        orderInout += "<option value='1'>외수</option><option value='0'>내수</option>";
                    }

                    $('#').append(orderType);
                    $('#detailOrderInout').append(orderInout);
                    var subOrder = "";
                    for (var i = 0; i < res.order.subOrder.length; i++){
                        subOrder += "<option value='"+i+"'>"+res.order.subOrder[i].code+"</option>";
                    }
                    $('#subDesign').val(res.order.subOrder[0].design_data.CAD_Design_Data_name);
                    $('#subOrderCode').append(subOrder);
                    /* $('#subDesignImgBox').find('span').css('background-image','url("'+res.order.subOrder[0].design_data.CAD_Design_Data_simulation_image+'")') */
                    $('#subDesignImgBox').find('img').attr('src', res.order.subOrder[0].design_data.CAD_Design_Data_simulation_image);
                    $('#subDesignQty').val(res.order.subOrder[0].design_qty);

                    /* selectBox Design Function */
                    createSelectBox2();
                },
                error :function () {
                    alert('다시')
                }});

        },
        error:function () {
          alert('구현중');
        }
    });
}