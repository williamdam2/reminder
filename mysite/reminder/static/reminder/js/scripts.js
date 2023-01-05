/*********************Var************************/
var c_OK = "#5aeab0";
var c_NG = "#f18787";
var c_SETTING = "#ecf187";

/*********************Form update status************************/
var ui_numberOfNG = document.getElementById('numberOfNG');
var ui_numberOfMachines = document.getElementById("numberOfMachines");
var formPopupUpdateStatus = document.getElementById("form-popup-update-status");
var formPopupUpdateStatusContainer = formPopupUpdateStatus.getElementsByClassName("form-update-status-container")[0];
var _fUpdateInfo = formPopupUpdateStatusContainer.getElementsByTagName("h2")[0];
var _fUpdateStatus = formPopupUpdateStatusContainer.getElementsByTagName("select")[0];
var _fUpdateMId = formPopupUpdateStatusContainer.getElementsByTagName("h6")[0];
var _fUpdateConfig = document.getElementById("fUpdateConfig");
var _fUpdateLOT = document.getElementById("fUpdateLOT");
var _fupdateSW = document.getElementById("fUpdateSW");
var _fUpdateDetails = document.getElementById("fUpdateDetails");

const reminderSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/reminder/'
    + '/'
);

reminderSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly, check the consumer');
};

setTimeout(() => {
    reminderSocket.send(JSON.stringify({
        'message': "new commer"
    }));
}, 5000);


reminderSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    if(data["type"]=="UDUI")
    {
        console.log("updating UI");
        let machine = data["machine"];
        ui_UpdateGridEyeStatus(machine);
        ui_UpdateNumberOfNG();
        console.log("update completed");
    }
    else
    {
        console.log("unknow data");
    }
};

function ui_UpdateGridEyeStatus(machine) {
    //console.log(machine)
    let ui_GridEye = document.getElementById(machine.macId);
    if(ui_GridEye)
    {
        let macStatusText = ui_GridEye.getElementsByClassName("mStatusTextInG")[0];
        let macBuildText = ui_GridEye.getElementsByTagName("span")[3];
        let macLotText = ui_GridEye.getElementsByTagName("span")[4];
        let sw = ui_GridEye.getElementsByTagName("span")[5];
        let macDetailText = ui_GridEye.getElementsByTagName("textarea")[0];

        if (machine.status == 0) {
            macStatusText.innerHTML = "NG";
            ui_GridEye.style.backgroundColor = c_NG; //NG
        } else if (machine.status == 1) {
            macStatusText.innerHTML = "OK";
            ui_GridEye.style.backgroundColor = c_OK; //OK
        } else if (machine.status == 2) {
            macStatusText.innerHTML = "SETTING";
            ui_GridEye.style.backgroundColor = c_SETTING; //setting
        }

        macBuildText.innerHTML = machine.buildConfig;
        macLotText.innerHTML = machine.lotId;
        macDetailText.innerHTML = machine.curDetail;
        sw.innerHTML = machine.sw;
    }   
    //return machine.status;
};

const rgb2hex = (rgb) => `#${rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/).slice(1).map(n => parseInt(n, 10).toString(16).padStart(2, '0')).join('')}`
function ui_UpdateNumberOfNG()
{
    let NGCounter = 0;
    for(let i = 0 ; i < listGridEye.length ; i++)
    {
        // console.log(rgb2hex(listGridEye[i].style.backgroundColor));
        if(rgb2hex(listGridEye[i].style.backgroundColor) == c_NG)
        {
            NGCounter+=1;
        }
    }
    ui_numberOfNG.innerHTML = String(NGCounter);
}


function ui_UpdateGridStatus(list_mac_object) {
    ui_numberOfMachines.innerHTML = list_mac_object.length;
    for(let i = 0 ; i < list_mac_object.length ; i ++)
    {
        machine = list_mac_object[i];
        ui_UpdateGridEyeStatus(machine);
    }
    ui_UpdateNumberOfNG();
};

function work_requestAndUpdateUi()
{
    json = {"request_type":"getmulti","list_id":listIdMacRequire};
    json = JSON.stringify(json);
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200)
        {
            //console.log(this.responseText)
            let json = JSON.parse(this.responseText);
            // console.log(json);
            ui_UpdateGridStatus(json);
        }
    };
    xhttp.open("POST", "/reminder/api/getMachineStatus_multi", true);
    xhttp.send(json);
}

var listGridEye = document.getElementsByClassName("grid-eye");
var listIdMacRequire = [];
setTimeout(function(){
    for (let i = 0; i < listGridEye.length; i++) {
        let GridEye = listGridEye[i];
        listIdMacRequire.push(GridEye.getElementsByClassName("mPkIdText")[0].innerHTML);
    }
    //init update routine
    work_requestAndUpdateUi();
    setInterval(work_requestAndUpdateUi, 100000);
}, 1000);


// Script for form update  status 
function openFormUpdateStatus(mGridEyeId) {

    formPopupUpdateStatus.style.display = "block";
    //console.log(this_id);
    //get grid eye
    let thisEye = document.getElementById(mGridEyeId);
    let mStatus = thisEye.getElementsByClassName("mStatusTextInG")[0].innerHTML;
    let mType = thisEye.getElementsByClassName("mInfoTextInG")[0].getElementsByTagName("span")[0].innerHTML;
    let mLine = thisEye.getElementsByClassName("mInfoTextInG")[1].getElementsByTagName("span")[0].innerHTML;
    let mModel = thisEye.getElementsByClassName("mInfoTextInG")[2].getElementsByTagName("span")[0].innerHTML;
    let mConfig = thisEye.getElementsByClassName("mInfoTextInG")[3].getElementsByTagName("span")[0].innerHTML;
    let mLotId = thisEye.getElementsByClassName("mInfoTextInG")[4].getElementsByTagName("span")[0].innerHTML;
    let mDetails = thisEye.getElementsByTagName("textarea")[0].innerHTML;
    let mId = thisEye.getElementsByClassName("mPkIdText")[0].innerHTML;

    //update form change
    _fUpdateInfo.innerHTML = "Update Machine " + mType + " " + mLine + " " + mModel;
    if (mStatus == "OK") {
        _fUpdateStatus.value = 1;
    } else if (mStatus == "NG") {
        _fUpdateStatus.value = 0;
    } else if (mStatus == "SETTING") {
        _fUpdateStatus.value = 2;
    }
    _fUpdateConfig.value = mConfig;
    _fUpdateLOT.value = mLotId;
    _fUpdateDetails.value = mDetails;
    _fUpdateMId.innerHTML = mId;
    document.getElementById("gridView").style.opacity="0.5";
}

function closeFormUpdateStatus() {
    document.getElementById("gridView").style.opacity = "1";
    formPopupUpdateStatus.style.display = "none";
}

function updateMachineStatusData() {
    let xhttp = new XMLHttpRequest();
    // prepare update data
    list = []; // list update data

    let status = _fUpdateStatus.value;
    let macId = _fUpdateMId.innerHTML;
    let buildConfig = _fUpdateConfig.value;
    let lotId = _fUpdateLOT.value;
    let curDetail = _fUpdateDetails.value;
    let sw = _fupdateSW.value;
    let machine = {
        macId: macId,
        status: status,
        buildConfig: buildConfig,
        lotId: lotId,
        curDetail: curDetail,
        sw : sw
    };

    list.push(machine);
    json = JSON.stringify(list);
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            closeFormUpdateStatus();
        }
    };
    xhttp.open("POST", "/reminder/api/updateMachineStatus", true);
    xhttp.send(json);
    // console.log(machine);
    reminderSocket.send(JSON.stringify(
        {"type":"UDUI","machine":machine}
    ))
}

//Clock
setInterval(() => {
    const now = new Date();
    let h = now.getHours();
    let m = now.getMinutes();
    let s = now.getSeconds();
    let year = now.getFullYear();
    let mon = now.getMonth();
    let day = now.getDay();
    document.getElementById('clock').innerHTML = year + "\\" + mon + "\\" + day + " " + h + ":" + m + ":" + s;

}, 1000);