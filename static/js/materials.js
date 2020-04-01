function createModal(type){
    $('#mask').css('display','block');
    $('#'+type+'Modal').css('display','block');
}

function closeModal(type){
    $('#mask').css('display','none');
    $('#'+type+'Modal').css('display','none');
}
function delyarnsearch() {
    var el = document.getElementsByClassName('yarnseach');
    var ent = $.Event("keydown");
    ent.keyCode = 13;

    for (var i=0; i<el.length; i++){
        el[i].value = '';
    }
    $('input[name=searchYarn]').focus();
    $('input[name=searchYarn]').trigger(ent);
}
$(document).keydown(function (event) {
    if (event.which == 13 && event.keyCode == 115) {
        alert("enter");
        $(document).trigger(e);
    }


});
function delbeamsearch() {
    var el = document.getElementsByClassName('beamsearch');


    for (var i = 0; i < el.length; i++) {
        el[i].value = '';
    }
    $('input[name=searchBeam]').focus();
    $('.beamsearch').submit();

}
function delrawsearch() {
    var el = document.getElementsByClassName('rawsearch');

    for (var i = 0; i < el.length; i++) {
        el[i].value = '';
    }
}
function searchYarn() {
    $('.yarnTr').remove();
    $.ajax({
        url: '/material/searchYarn',
        type: 'POST',
        cache: false,
        data: {
            searchName: $('#searchYarn').val()
        },
        dataType: 'json',
        async: false,

        success: function (response) {
            console.log(response);
            response.forEach(function (obj) {
                var tr = document.createElement('tr');
                tr.className = 'yarnTr';

                var td = document.createElement('td');
                td.innerHTML = obj.id;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.name;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.code;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.maker;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.count;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.filament;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.contraction + '%';
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.material;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.kind;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.color;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.lab;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.qty;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.Receivingdate;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = "<span class='removeBtn' onclick='delYarnData(" + obj.id + ")'>Remove</span>";
                tr.append(td);

                $('#yarnTableBox > table > tbody').append(tr);
            });
            /*
            if(response.length > 16 && os != 'Mac OS'){
                $('#designData').css('display','block');
                $('#designDataList td:last-child').css('width', '133px');
            }
            if(response.length > 0){
                $('#showDesingData').find('.noSearchDiv').remove();
                $('.designDataTr').eq(0).trigger('click');
            }else{
                $('#designData').css('display','none');
                $('#designDataDelete').css('display','none');
                $('#showDesingData').find('.noSearchDiv').remove();
                $('#showDesingData').append('<div class="noSearchDiv">Design data does not exist</div>');
            }
            */
        }

    });
}



function searchBeam() {
    $('.beamTr').remove();
    $.ajax({
        url: '/material/searchBeam',
        type: 'POST',
        cache: false,
        data: {
            searchName: $('#searchBeam').val()
        },
        dataType: 'json',
        async: false,
        success: function (response) {
            console.log(response);
            response.forEach(function (obj) {
                var tr = document.createElement('tr');
                tr.className = 'beamTr';

                var td = document.createElement('td');
                td.innerHTML = obj.id;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.name;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.yarn_name;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.yarn_qty;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.size;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.Receivingdate;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = "<span class='removeBtn' onclick='delBeamData(" + obj.id + ")'>Remove</span>";
                tr.append(td);

                $('#beamTableBox > table > tbody').append(tr);
            });
            /*
            if(response.length > 16 && os != 'Mac OS'){
                $('#designData').css('display','block');
                $('#designDataList td:last-child').css('width', '133px');
            }
            if(response.length > 0){
                $('#showDesingData').find('.noSearchDiv').remove();
                $('.designDataTr').eq(0).trigger('click');
            }else{
                $('#designData').css('display','none');
                $('#designDataDelete').css('display','none');
                $('#showDesingData').find('.noSearchDiv').remove();
                $('#showDesingData').append('<div class="noSearchDiv">Design data does not exist</div>');
            }
            */
        }
    });
}

function createYarn() {

    var exp_number = /^[0-9]*$/;


    /* 유효성검사 */
    if(!yarnForm.yarnName.value){
        alert('원사명을 입력해주세요');
        yarnForm.yarnName.focus();
        return;
    }
    if(!yarnForm.yarnCode.value){
        alert('원사코드를 입력해주세요');
        yarnForm.yarnCode.focus();
        return;
    }
    if(!yarnForm.yarnMaker.value){
        alert('원사메이커를 입력해주세요');
        yarnForm.yarnMaker.focus();
        return;
    }

    // 사실 오더일자를 구분하는게 필요없어보임. disabled 로 막음.
    if(!yarnForm.yarnCount.value){
        alert('원사굵기를 입력해주세요');
        yarnForm.yarnCount.focus();
        return;
    }
    if(!yarnForm.yarnFilament.value){
        alert('필라멘트를 입력해주세요');
        yarnForm.yarnFilament.focus();
        return;
    }
    if(!yarnForm.yarnContraction.value){
        alert('수축률을 입력해주세요');
        yarnForm.yarnContraction.focus();
        return;
    }
    if(!yarnForm.yarnMaterial.value){
        alert('재료를 입력해주세요');
        yarnForm.yarnMaterial.focus();
        return;
    }
    if(!yarnForm.yarnKind.value){
        alert('원사종류를 입력해주세요');
        yarnForm.yarnKind.focus();
        return;
    }
    if(!yarnForm.yarnColor.value){
        alert('원사색을 입력해주세요');
        yarnForm.yarnColor.focus();
        return;
    }
    if(!yarnForm.yarnQty.value){
        alert('입고수량을 입력해주세요');
        yarnForm.yarnQty.focus();
        return;
    }

    if(!exp_number.test(yarnForm.yarnCount.value)){
        alert('원사굵기는 숫자만 입력가능합니다.');
        yarnForm.yarnCount.focus();
        return;
    }
    if(!exp_number.test(yarnForm.yarnFilament.value)){
        alert('필라멘트는 숫자만 입력가능합니다.');
        yarnForm.yarnFilament.focus();
        return;
    }
    if(!exp_number.test(yarnForm.yarnContraction.value)){
        alert('수축률은 숫자만 입력가능합니다.');
        yarnForm.yarnContraction.focus();
        return;
    }
<<<<<<< HEAD
=======
    if(!exp_number.test(yarnForm.yarnWeight.value)){
        alert('무게은 숫자만 입력가능합니다.');
        yarnForm.yarnWeight.focus();
        return;
    }
>>>>>>> master
    if(!exp_number.test(yarnForm.yarnQty.value)){
        alert('입고량은 숫자만 입력가능합니다.');
        yarnForm.yarnQty.focus();
        return;
    }

    yarnForm.submit();

}

function createBeam() {

    var exp_number = /^[0-9]*$/;


    /* 유효성검사 */
    if(!beamForm.beamName.value){
        alert('빔 이름을 입력해주세요');
        beamForm.beamName.focus();
        return;
    }
    if(!beamForm.beamSize.value){
        alert('빔 사이즈를 입력해주세요');
        beamForm.beamSize.focus();
        return;
    }

    if(!exp_number.test(beamForm.beamSize.value)){
        alert('빔 사이즈는 숫자만 입력가능합니다.');
        beamForm.beamSize.focus();
        return;
    }

    beamForm.submit();

}

function delBeamData(bid) {
    var result = confirm('빔을 삭제하시겠습니까?');
    if(result){
        $.ajax({
            url: '/material/beamDelete',
            type: 'POST',
            cache: false,
            data: {
                bid: bid
            },
            dataType: 'json',
            async: false,
            success: function (response) {
                if(response.success){
                    alert('삭제되었습니다.')
                }else{
                    alert('실패하였습니다.')
                }
            },
            error: function (e) {

            }
        })
    }
}

function delYarnData(id) {
    var result = confirm('원사를 삭제하시겠습니까?');
    if(result){
        $.ajax({
            url: '/material/yarnDelete',
            type: 'POST',
            cache: false,
            data: {
                id: id
            },
            dataType: 'json',
            async: false,
            success: function (response) {
                if(response.success){
                    alert('삭제되었습니다.')
                }else{
                    alert('실패하였습니다.')
                }
            },
            error: function (e) {

            }
        })
    }
}

function getRealTimeMachineData() {

}
function createRoll() {
     /* 유효성검사 */
    if(!rollForm.rollname.value){
        alert('롤의 품명을 입력해주세요');
        rollForm.rollname.focus();
        return;
    }
    if(!rollForm.rollfabricname.value){
        alert('롤에 감긴 생지의 품명을 입력해주세요');
        rollForm.rollfabricname.focus();
        return;
    }
    if(!rollForm.rollfabricdate.value){
        alert('롤에 감긴 생지의 출고일을 입력해주세요');
        rollForm.rollfabricdate.focus();
        return;
    }
    if(!rollForm.rollcount.value){
        alert('롤의 수량을 입력해주세요');
        rollForm.rollcount.focus();
        return;
    }
    if(!rollForm.rollfabricerror.value){
        alert('롤의 난단의 길이를 입력해주세요');
        rollForm.rollfabricerror.focus();
        return;
    }
    if(!rollForm.rollfabriclength.value){
        alert('롤에 감긴 원단의 길이를 입력해주세요');
        rollForm.rollfabriclength.focus();
        return;
    }
    if(!rollForm.rollfabricweight.value){
        alert('롤의 무게를 입력해주세요');
        rollForm.rollfabricweight.focus();
        return;
    }

    rollForm.submit();
}