

window.onload = function(){
    if($('.designDataTr').length !== 0){
        $('.designDataTr').eq(0).trigger('click');
    }
};

function deleteDesign(id) {
    console.log(id);
    $.ajax({
        url: '/design_data/delete',
        type: 'POST',
        cache: false,
        data: {
            designId: id
        },
        dataType: 'json',
        async: false,
        success: function (response) {
            console.log(response);
            searchDesign();
        }
    });
}

function searchDesign() {
    $('.designDataTr').remove();
    $.ajax({
        url: '/design_data/getList',
        type: 'POST',
        cache: false,
        data: {
            searchName: $('#searchName').val()
        },
        dataType: 'json',
        async: false,
        success: function (response) {
            response.forEach(function (obj) {
                var tr = document.createElement('tr');
                tr.className = 'designDataTr';
                tr.setAttribute('onclick', 'setDesignData(' + obj.id + ')');
                tr.id = 'designData' + obj.id;

                var td = document.createElement('td');
                td.innerHTML = obj.id;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.name;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = obj.date;
                tr.append(td);

                $('#designDataList > table > tbody').append(tr);
            });
            if(response.length > 16 && os != 'Mac OS'){
                $('#designData').css('display','block');
                $('#designDataList td:last-child').css('width', '133px');
            }
            if(response.length > 0){
                $('#showDesingData').find('.noSearchDiv').remove();
                $('.designDataTr').eq(0).trigger('click');
                /*$('#designDataList tr:nth-of-type(1)').trigger('click');*/
            }else{
                $('#designData').css('display','none');
                $('#designDataDelete').css('display','none');
                $('#showDesingData').find('.noSearchDiv').remove();
                $('#showDesingData').append('<div class="noSearchDiv">Design data does not exist</div>');
            }
        }
    });
}

function setDesignData(id) {
    $('.selected').removeClass('selected');
    $('#designData' + id).addClass('selected');
    $('.new').remove();
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
            if(response.length !== 0){
                $('#designData').css('display','block');
                $('#designDataDelete').css('display','block');
            }
            console.log(response);
            $('#deleteButton').attr('onclick', 'deleteDesign(' + id + ')');
            $('#designName').html('Name : ' + response.CAD_Design_Data_name);
            $('#designCode').html('CODE : ' + response.CAD_Design_Data_code);
            $('#date').html('DATE : ' + response.CAD_Design_Data_create_date);
            response.FSTY_CAD_Layer.forEach(function (layer) {
                var tr = document.createElement('tr');
                tr.className = 'new';

                var td = document.createElement('td');
                td.innerHTML = layer.CAD_Layer_name;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.FSTY_CAD_Yarn.CAD_Yarn_idx;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.FSTY_CAD_Yarn.CAD_Yarn_maker;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.FSTY_CAD_Yarn.CAD_Yarn_spec;
                tr.append(td);

                td = document.createElement('td');
                var colorDiv = document.createElement('div');
                colorDiv.style.backgroundColor = 'rgb(' + layer.FSTY_CAD_Yarn.CAD_Yarn_rgb_color + ')';
                colorDiv.style.width = '80%';
                colorDiv.style.height = '15px';
                colorDiv.style.margin = '0 auto';
                colorDiv.style.border = '1px solid rgb(215, 216, 216)';
                td.append(colorDiv);
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.FSTY_CAD_Yarn.CAD_Yarn_code;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.CAD_Layer_ratio;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.CAD_Layer_mm_rack;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.CAD_Layer_use;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.CAD_Layer_beam;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.CAD_Layer_total;
                tr.append(td);

                $('#yarnTable>tbody').append(tr);
            });

            response.FSTY_CAD_Production.FSTY_CAD_Fabric.forEach(function (fabric) {
                var tr = document.createElement('tr');
                tr.className = 'new';

                var td = document.createElement('td');
                if(fabric.CAD_Fabric_type == 'R')
                    td.innerHTML = 'greige';
                else
                    td.innerHTML = '[processingpaper]';
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = fabric.CAD_Fabric_wpi + ' w/inch';
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = fabric.CAD_Fabric_cpi + ' c/cm';
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = fabric.CAD_Fabric_width + ' inch';
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = fabric.CAD_Fabric_weight_per_width + ' g/y';
                tr.append(td);

                $('#fabricTable>tbody').append(tr);
            });

            response.FSTY_CAD_Layer.forEach(function (layer) {
                var tr = document.createElement('tr');
                tr.className = 'new';

                var td = document.createElement('td');
                td.innerHTML = layer.CAD_Layer_name;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.FSTY_CAD_Yarn.CAD_Yarn_rgb_color;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.FSTY_CAD_Yarn.CAD_Yarn_lab_color;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.FSTY_CAD_Yarn.CAD_Yarn_pantone_color;
                tr.append(td);

                $('#colorTable>tbody').append(tr);

                tr = document.createElement('tr');
                tr.className = 'new';

                td = document.createElement('td');
                td.innerHTML = layer.CAD_Layer_name;
                tr.append(td);

                td = document.createElement('td');
                td.innerHTML = layer.FSTY_CAD_Chain_Link.CAD_Chain_Link_course;
                tr.append(td);

                $('#layerTable>tbody').append(tr)
            });
            /*
            $('.output').html('일일생산량 :' + response.FSTY_CAD_Production.CAD_Production_quota_per_day);

            response.FSTY_CAD_Layer.forEach(function (layer) {

                var div = document.createElement('div');
                div.className = 'course new';

                var span = document.createElement('span');
                span.innerHTML = layer.CAD_Layer_name;

                div.append(span);
                div.append(layer.FSTY_CAD_Chain_Link.CAD_Chain_Link_course);

                $('#layerArray').append(div)
            });
            */
            response.FSTY_CAD_Layer.forEach(function (layer) {

                var div = document.createElement('div');
                div.className = 'course new';

                var span = document.createElement('span');
                span.innerHTML = layer.CAD_Layer_name;

                div.append(span);
                div.append(layer.CAD_Layer_iodata);

                $('#productionTable tbody > tr:nth-child(1) > td:nth-child(2)').append(div)
            });

            $('#productionTable tbody > tr:nth-child(2) > td:nth-child(2)').empty();
            $('#productionTable tbody > tr:nth-child(2) > td:nth-child(2)').append(response.FSTY_CAD_Production.CAD_Production_note);
            $('#imgTable thead > tr > th:nth-child(2)').html('배율 : ' + response.CAD_Design_Data_magnification);

            $('#imgTable > tbody > tr > td:nth-child(1) > div').css('background-image', 'url(' + response.CAD_Design_Data_pattern_image + ')');/*.attr('src', response.CAD_Design_Data_simulation_image);*/
            $('#imgTable > tbody > tr > td:nth-child(2) > div').css('background-image', 'url(' + response.CAD_Design_Data_simulation_image + ')');

            $('#yarnDiv > div').css('height', $('#yarnDiv > table').outerHeight());
            console.log($('#yarnDiv > table').outerHeight());
            $('#layerDiv > div').css('height', $('#layerDiv > table').outerHeight());
            $('#productionDiv > div').css('height', $('#productionDiv > table').outerHeight());
            $('#colorDiv > div').css('height', $('#colorDiv > table').outerHeight());
            $('#fabricDiv > div').css('height', $('#fabricDiv > table').outerHeight());

        },

        error: function () {
            alert('Deleting category has Failed');
        }
    });
}

function printwep() {
    window.print()
}