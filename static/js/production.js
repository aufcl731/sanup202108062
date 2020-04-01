function warpSheet(){
    window.open('/order/warpWorkSheet', 'WorkSheet', 'width=900, height=800')
}

function knitSheet(id){
    window.open('/production/detail/'+id, 'WorkSheet', 'width=1100, height=800')
}

function showQrCode(id) {
    window.open('/order/showQr/'+id, 'showQr', 'width=200, height=200')
}

/*
IE 접속 막기

window.onload = function(){
    var brower = navigator.userAgent.toLowerCase();
    if(brower.indexOf('msie') != -1){
        alert('크롬 다운로드 페이지로 이동합니다.');
        history.href = 'https://www.google.com/intl/ko/chrome/';
    }
};

*/