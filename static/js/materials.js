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


    /* ??????????????? */
    if(!yarnForm.yarnName.value){
        alert('???????????? ??????????????????');
        yarnForm.yarnName.focus();
        return;
    }
    if(!yarnForm.yarnCode.value){
        alert('??????????????? ??????????????????');
        yarnForm.yarnCode.focus();
        return;
    }
    if(!yarnForm.yarnMaker.value){
        alert('?????????????????? ??????????????????');
        yarnForm.yarnMaker.focus();
        return;
    }

    // ?????? ??????????????? ??????????????? ??????????????????. disabled ??? ??????.
    if(!yarnForm.yarnCount.value){
        alert('??????????????? ??????????????????');
        yarnForm.yarnCount.focus();
        return;
    }
    if(!yarnForm.yarnFilament.value){
        alert('??????????????? ??????????????????');
        yarnForm.yarnFilament.focus();
        return;
    }
    if(!yarnForm.yarnContraction.value){
        alert('???????????? ??????????????????');
        yarnForm.yarnContraction.focus();
        return;
    }
    if(!yarnForm.yarnMaterial.value){
        alert('????????? ??????????????????');
        yarnForm.yarnMaterial.focus();
        return;
    }
    if(!yarnForm.yarnKind.value){
        alert('??????????????? ??????????????????');
        yarnForm.yarnKind.focus();
        return;
    }
    if(!yarnForm.yarnColor.value){
        alert('???????????? ??????????????????');
        yarnForm.yarnColor.focus();
        return;
    }
    if(!yarnForm.yarnQty.value){
        alert('??????????????? ??????????????????');
        yarnForm.yarnQty.focus();
        return;
    }

    if(!exp_number.test(yarnForm.yarnCount.value)){
        alert('??????????????? ????????? ?????????????????????.');
        yarnForm.yarnCount.focus();
        return;
    }
    if(!exp_number.test(yarnForm.yarnFilament.value)){
        alert('??????????????? ????????? ?????????????????????.');
        yarnForm.yarnFilament.focus();
        return;
    }
    if(!exp_number.test(yarnForm.yarnContraction.value)){
        alert('???????????? ????????? ?????????????????????.');
        yarnForm.yarnContraction.focus();
        return;
    }

    if(!exp_number.test(yarnForm.yarnWeight.value)){
        alert('????????? ????????? ?????????????????????.');
        yarnForm.yarnWeight.focus();
        return;
    }
    if(!exp_number.test(yarnForm.yarnQty.value)){
        alert('???????????? ????????? ?????????????????????.');
        yarnForm.yarnQty.focus();
        return;
    }

    yarnForm.submit();

}

function createBeam() {

    var exp_number = /^[0-9]*$/;


    /* ??????????????? */
    if(!beamForm.beamName.value){
        alert('??? ????????? ??????????????????');
        beamForm.beamName.focus();
        return;
    }
    if(!beamForm.beamSize.value){
        alert('??? ???????????? ??????????????????');
        beamForm.beamSize.focus();
        return;
    }

    if(!exp_number.test(beamForm.beamSize.value)){
        alert('??? ???????????? ????????? ?????????????????????.');
        beamForm.beamSize.focus();
        return;
    }

    beamForm.submit();

}

function delBeamData(bid) {
    var result = confirm('?????? ?????????????????????????');
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
                    alert('?????????????????????.')
                }else{
                    alert('?????????????????????.')
                }
                window.location.reload();
            },
            error: function (e) {

            }
        })
    }
}

function delGreigeData(gpk){
    var result = confirm('????????? ?????????????????????????');
    if(result){
        $.ajax({
            url: '/material/greigeDelete',
            type: 'POST',
            cache: false,
            data: {
                gpk: gpk
            },
            dataType: 'json',
            async: false,
            success: function (response) {
                if(response.success){
                    alert('?????????????????????.')
                }else{
                    alert('?????????????????????.')
                }
                window.location.reload();
            },
            error: function (e) {

            }
        })
    }
}

function delRollData(rid){
    var result = confirm('?????? ?????????????????????????');
    if(result){
        $.ajax({
            url: '/material/rollDelete',
            type: 'POST',
            cache: false,
            data: {
                rid: rid
            },
            dataType: 'json',
            async: false,
            success: function (response) {
                if(response.success){
                    alert('?????????????????????.')
                }else{
                    alert('?????????????????????.')
                }
                window.location.reload();
            },
            error: function (e) {

            }
        })
    }
}

function delYarnData(id) {
    var result = confirm('????????? ?????????????????????????');
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
                    alert('?????????????????????.')
                }else{
                    alert('?????????????????????.')
                }
                window.location.reload();
            },
            error: function (e) {

            }
        })
    }
}

function getRealTimeMachineData() {

}
function createRoll() {
     /* ??????????????? */
    if(!rollForm.rollname.value){
        alert('?????? ????????? ??????????????????');
        rollForm.rollname.focus();
        return;
    }
    if(!rollForm.rollfabricname.value){
        alert('?????? ?????? ????????? ????????? ??????????????????');
        rollForm.rollfabricname.focus();
        return;
    }
    if(!rollForm.rollfabricdate.value){
        alert('?????? ?????? ????????? ???????????? ??????????????????');
        rollForm.rollfabricdate.focus();
        return;
    }
    if(!rollForm.rollcount.value){
        alert('?????? ????????? ??????????????????');
        rollForm.rollcount.focus();
        return;
    }
    if(!rollForm.rollfabricerror.value){
        alert('?????? ????????? ????????? ??????????????????');
        rollForm.rollfabricerror.focus();
        return;
    }
    if(!rollForm.rollfabriclength.value){
        alert('?????? ?????? ????????? ????????? ??????????????????');
        rollForm.rollfabriclength.focus();
        return;
    }
    if(!rollForm.rollfabricweight.value){
        alert('?????? ????????? ??????????????????');
        rollForm.rollfabricweight.focus();
        return;
    }

    rollForm.submit();
}

function createDiplay1(type){
    $('#'+type).css('display','block');
    $("#materialsBot").css('display','none');
    $("#rollFrame").css('display','none');
}

function createDiplay2(type){
    $('#'+type).css('display','block');
    $("#materialsTop").css('display','none');
    $("#rollFrame").css('display','none');
}

function createDiplay3(type){
    $('#'+type).css('display','block');
    $("#materialsBot").css('display','none');
    $("#materialsTop").css('display','none');
}