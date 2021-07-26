function searchDesign() {
    $('#designListTable tbody tr').remove();
    $.ajax({
        url: '/design_data/getList',
        type: 'POST',
        cache: false,
        data: {
            searchName: $('#designSearchBox input').val()
        },
        dataType: 'json',
        async: false,
        success: function (response) {
            console.log(response);
            response.forEach(function (obj) {
                var tr = document.createElement('tr');
                tr.setAttribute('onclick', 'setDesignData(' + obj.id + ')');
                tr.id = 'designData' + obj.id;
                tr.className = 'designDataTr';

                var td = document.createElement('td');
                td.innerHTML = obj.name;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.date;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.date;
                tr.append(td);

                $('#designListTable tbody').append(tr);
            });

            if(response.length > 13 && os != 'Mac OS'){
                $('#designListTable td:last-child').css('width', '105px');
            }
        }
    });
}

function setDesignData(id) {
    $('.selected').removeClass('selected');
    $('#designData' + id).addClass('selected');

    $.ajax({
        url: '/design_data/designdata',
        type: 'POST',
        cache: false,
        data: {
            designId: id
        },
        dataType: 'json',
        async: false,
        success: function (response) {
            $('#designTopInfo input:nth-of-type(1)').val(response.CAD_Design_Data_name);
            $('#designTopInfo input:nth-of-type(2)').val(response.CAD_Design_Data_create_date);

            $('#designImgBox > img').attr('src', response.CAD_Design_Data_simulation_image);

            response.FSTY_CAD_Production.FSTY_CAD_Fabric.forEach(function (fabricObj) {
                if(fabricObj.CAD_Fabric_type == 'R'){
                    $('#designInfo p:nth-of-type(1)').html('WPI : ' + fabricObj.CAD_Fabric_wpi + 'w/inch');
                    $('#designInfo p:nth-of-type(2)').html('CPC : ' + fabricObj.CAD_Fabric_cpi + 'c/cm');
                    $('#designInfo p:nth-of-type(3)').html('Width : ' + fabricObj.CAD_Fabric_width + 'inch');
                }
            });

        },
        error: function () {
            alert('Deleting category has Failed');
        }
    });
}

function addDesignData() {
    var id = parseInt($('.designDataTr.selected').attr('id').substring(10));
    var name = $('.designDataTr.selected>td:eq(0)').text();

    var selectDesign = "<tr id='orderData"+id+"'><td>"+name+"</td><td class='designQtyTd'><input type='hidden' name='designID' class='designID' value="+id+"><input type='text' class='designQty' name='designQty'></td><td><span class='removeBtn' onclick='delOrderDesign(this)'>Remove</span></td></tr>";
    if($("#orderData"+id).length == 0){
        $('#designOrderTable>tbody').append(selectDesign)
    }else{
        alert('이미 선택된 디자인입니다.');
    }

    if(os != 'Mac OS' && $('#designOrderTable > tbody > tr').length > 4){
        $('#designOrderTable td:nth-of-type(3)').css('width', '83px');
    }
    console.log($('#designOrderTable > tbody > tr').length);
}

function delOrderDesign(removeDesign) {
    removeDesign.parentNode.parentNode.remove();
}

function createOrder() {

    var designQty = $('.designQty');
    var orderStr = orderForm.order_date.value.replace(/-/g,"");
    var dueStr = orderForm.due_date.value.replace(/-/g,"");
    var exp_number = /^[0-9]*$/;


    /* 유효성검사 */
    if(!orderForm.company.value){
        alert('사업장을 입력해주세요');
        orderForm.company.focus();
        return;
    }
    if(!orderForm.buyer.value){
        alert('거래처를 입력해주세요');
        orderForm.buyer.focus();
        return;
    }
    if(!orderForm.username.value){
        alert('담당자를 입력해주세요');
        orderForm.username.focus();
        return;
    }

    // 사실 오더일자를 구분하는게 필요없어보임. disabled 로 막음.
    if(!orderForm.order_date.value){
        alert('오더일자를 입력해주세요');
        orderForm.order_date.focus();
        return;
    }
    if(!orderForm.due_date.value){
        alert('납기일자를 입력해주세요');
        orderForm.due_date.focus();
        return;
    }
    if(parseInt(orderStr) > parseInt(dueStr)){
        alert('납기일을 확인해주세요');
        orderForm.due_date.focus();
        return;
    }
    if(!orderForm.order_round.value){
        alert('차수를 입력해주세요');
        orderForm.order_round.focus();
        return;
    }

    if(designQty.length == 0){
        alert('디자인을 선택해주세요');
        return;
    }

    for(var i = 0; i < designQty.length; i++){
        if(!exp_number.test(designQty[i].value)){
            alert('디자인 수량은 숫자만 입력해주세요');
            designQty[i].focus();
            return;
        }

        if(designQty[i].value == ''){
            alert('디자인수량을 입력해주세요');
            designQty[i].focus();
            return;
        }
    }

    orderForm.submit();

}

function modifyOrder(){

    var orderStr = modifyOrderForm.detailOrderDate.value.replace(/-/g,"");
    var dueStr = modifyOrderForm.detailDueDate.value.replace(/-/g,"");

    var exp_number = /^[0-9]*$/;


    if(!modifyOrderForm.detailBuyer.value){
        alert('거래처를 입력해주세요');
        modifyOrderForm.detailBuyer.focus();
        return;
    }

    if(!modifyOrderForm.detailOrderDate.value){
        alert('오더일자를 입력해주세요');
        modifyOrderForm.detailOrderDate.focus();
        return;
    }
    if(!modifyOrderForm.detailDueDate.value){
        alert('납기일자를 입력해주세요');
        orderForm.due_date.focus();
        return;
    }
    if(parseInt(orderStr) > parseInt(dueStr)){
        alert('납기일을 확인해주세요');
        orderForm.due_date.focus();
        return;
    }

    if(!exp_number.test(modifyOrderForm.subDesignQty.value)){
        alert('디자인 수량은 숫자만 입력해주세요');
        modifyOrderForm.subDesignQty.focus();
        return;
    }

    if(!modifyOrderForm.subDesignQty.value){
        alert('디자인수량을 입력해주세요');
        modifyOrderForm.subDesignQty.focus();
        return;
    }
    modifyOrderForm.append({'oid':oid});
    modifyOrderForm.submit();
}

function deleteOrder(){
    var orderForm = document.createElement('Form');
    orderForm.action = '/order/delete';
    orderForm.method = 'post';

    var oid = document.createElement('input');
    oid.name = 'orderId';
    oid.value = $('#oid').val();

    orderForm.append(oid);
    $('body').append(orderForm);
    orderForm.submit();
}
function modifyStyle(){
    var oid = $('#stoid').val();
    $.ajax({
        url:'/order/style_modify/'+oid,
        type:'POST',
        data:{
            FabricVersion:$('#FabricVersion').val(),
            FabricCode:$('#FabricCode').val(),
            FabricName:$('#FabricName').val(),
            FabricSize:$('#FabricSize').val(),
            SMeterWeight:$('#SMeterWeight').val(),
            YardWeight:$('#YardWeight').val(),
            FabricPart:$('#FabricPart').val(),
            FabricConstruction:$('#FabricConstruction').val(),
            FabricWidth:$('#FabricWidth').val(),
            CuttableWidth:$('#CuttableWidth').val(),
            Unit:$('#Unit').val(),
            FabricCsm:$('#FabricCsm').val(),
            FabricLoss:$('#FabricLoss').val(),
            DyeProcessTypeCode:$('#DyeProcessTypeCode').val(),
            ContentRate:$('#ContentRate').val(),
            YarnCode:$('#YarnCode').val(),
            YarnName:$('#YarnName').val(),
            YarnColor:$('#YarnColor').val(),
            YarnCount:$('#YarnCount').val(),
            YnDye:$('#YnDye').val(),
        },
        dataType:'json',
        success:function (res){
          alert('suc')
        },

    })
}
function deleteStyle(){
    var oid = $('#stoid').val();
    $.ajax({
        url:'/order/style_suc/'+oid,
        type:'POST',
        dataType:'json',
        success:function (res){
            alert('suc')
        }
    })
}
function chagneStyle(){
    var oid = $('#stoid').val();
    $.ajax({
        url:'/order/change_style/'+oid,
        type:'POST',
        dataType:'json',
        success:function (res){
            alert('suc')
        }
    })
}
function openRawRoll(id){
    window.open('/order/rawroll/'+id,'RawRoll', 'width=1100, height=800', encoding='UTF-8');
}

function openRawRoll(id){
    window.open('/order/rawroll/'+id,'RawRoll', 'width=1100, height=800', encoding='UTF-8');
}