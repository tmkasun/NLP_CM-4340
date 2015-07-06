/*
 *  Copyright (c) 2005-2010, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
 *
 *  WSO2 Inc. licenses this file to you under the Apache License,
 *  Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

var defaultOSM = L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: 'Map data © OpenStreetMap contributors <a href="http://openstreetmap.org/" target="_blank">Openstreetmap</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">. Map data (c) <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA.'
});

var baseLayers = {
    "Open Street Maps": defaultOSM
};

function removeGeoFence(geoFenceElement) {
    var queryName = $(geoFenceElement).attr('data-queryName');
    var areaName = $(geoFenceElement).attr('data-areaName');

    data = {
        'executionPlanName': createExecutionPlanName(queryName),
        'queryName': queryName,
        'cepAction': 'undeploy'

    };
    $.post('controllers/remove_alerts.jag', data, function (response) {
        $.UIkit.notify({
            message: '<span style="color: dodgerblue">' + response.status + '</span><br>' + response.message,
            status: (response.status == 'success' ? 'success' : 'danger'),
            timeout: 3000,
            pos: 'top-center'
        });
        closeAll();
    }, 'json');
}

// TODO:this is not a remote call , move this to application.js
function closeAll() {
    $('.modal').modal('hide');
    setTimeout(function () {
        $.UIkit.offcanvas.hide()
    }, 100);
}

