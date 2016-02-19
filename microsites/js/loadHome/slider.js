var $fDataServicesContainer;
var $fDataServicesContainers;

$(document).ready(function(){
    $fDataServicesContainer = $("#id_dataservices_container");

    initCharts();
    initDataServices();
    initSlider();
});

function restartCharts(){
    var $lCharts = $('[id*=id_chartBox_]');

    for (var i = 0; i < $lCharts.size() ; i++){
        var l$Chart     = $lCharts.eq(i);
        var lSov_id     = l$Chart.data("sov_id");
        var _var        = "chart_" + lSov_id;
        window[_var].renderChart();
    };
}

function initCharts(){
    var $lCharts = $('[id*=id_chartBox_]');
    for (var i = 0; i < $lCharts.size() ; i++){
        var l$Chart     = $lCharts.eq(i);
        var lDs_id     = l$Chart.data("dataservice_id");
        var lSov_id     = l$Chart.data("sov_id");
        var lEndPoint   = l$Chart.data("end_point");
        var lImplDetails = l$Chart.data("implType");
        var _var        = "chart_" + lSov_id;

        window[_var] = new HomeChart({'chartJson' : lImplDetails, '$Container': l$Chart, 'dataStreamId' : lDs_id, 'endPoint': lEndPoint});
    };
}
function initDataServices(){

    $fDataServicesContainers = $fDataServicesContainer.find("div[id*=id_dataservice_container_]");

    $fDataServicesContainers.each(function(){
        var lDataServiceId = jQuery.data(this, "dataservice_id");
        initDataService(lDataServiceId);
    });
}

function initDataService(pDataServiceId){

    container = $('#id_dataservice_container_' + pDataServiceId);

    var $lDataServiceContainer = $fDataServicesContainer.find('#id_dataservice_container_' + pDataServiceId);
    var $lIframe = $lDataServiceContainer.find('#id_dataservice_' + pDataServiceId);

    startWaitMessage($lIframe);

    invokeDataService(container.data("jsonURL"),container.data("pId"));
}

function startWaitMessage(pHTMLElement){

    var lHtml = "<table class='Loading'><tr><td>&nbsp";
    lHtml = lHtml + "</td></tr></table>";

    pHTMLElement.html(lHtml);
}

function invokeDataService(lUrl, pDataServiceId){

    var lData= $.param({limit: 50, revision_id: pDataServiceId});
    
    if ( pDataServiceId != undefined ){

        $.ajax({ url: lUrl
            , type:'GET'
            , data: lData
            , dataType: 'json'
            , timeoutNumber : 30000
            , success: onSuccessDataServiceExecute
            , error: onErrorDataServiceExecute
        });
    }
}

function onSuccessDataServiceExecute(pResponse){

    ds_results = pResponse; //global, for later use
    $.url.setUrl(this.url);
    var lDataServiceId          = $.url.param("revision_id");
    var $lDataServiceContainer  = $fDataServicesContainer.find('#id_dataservice_container_' + lDataServiceId);
    var lDataserviceId          = $lDataServiceContainer.data('dataservice_id');

    var lHtml = '';

    if( pResponse != null && pResponse.fType != 'ERROR' ){

        // si es array
        if(pResponse.fType!='ARRAY'){
            var lValue = '';
            if(pResponse.fType == 'TEXT'){
                var str = String(pResponse.fStr);
                str = str.replace(/(<([^>]+)>)/ig," ");
                lValue = '<table class="Texto"><tr><td>' + str + '</td></tr></table>';
            }else if(pResponse.fType == 'DATE'){
                var format = pResponse.fDisplayFormat;
                var number = pResponse.fNum;
                var str = '';
                if (! _.isUndefined(format)){
                    // sometimes are seconds, sometimes miliseconds
                    if (number < 100000000000) number = number * 1000;
                    var dt = new Date(number);
                    dt.setTime( dt.getTime() + dt.getTimezoneOffset()*60*1000 );
                    var local = format.fLocale;
                    //(?) if I use "en" doesn't work, I must use "" for "en"
                    if (undefined === local || local === "en" || local.indexOf("en_")) local = "";
                    if (local === "es" || local.indexOf("es_")) local = "es";
                    str = $.datepicker.formatDate(format.fPattern, dt, {
                        dayNamesShort: $.datepicker.regional[local].dayNamesShort,
                        dayNames: $.datepicker.regional[local].dayNames,
                        monthNamesShort: $.datepicker.regional[local].monthNamesShort,
                        monthNames: $.datepicker.regional[local].monthNames
                    });
                }else{
                    str = String(number);
                }

                lValue = '<table class="Numero"><tr><td>' + str + '</td></tr></table>';
            } else if(pResponse.fType == 'NUMBER'){
                var displayFormat = pResponse.fDisplayFormat;
                if (displayFormat != undefined) {
                    var number = $.formatNumber(pResponse.fNum, {format:displayFormat.fPattern, locale:displayFormat.fLocale});
                } else {
                    var number = pResponse.fNum;
                }
                lValue = '<table class="Numero"><tr><td>' + String(number) + '</td></tr></table>';
            } else if(pResponse.fType == 'LINK'){
                lValue = '<table class="Texto"><tr><td><a target="_blank" href="' + pResponse.fUri + '" rel="nofollow" title="' + pResponse.fStr + '">' + pResponse.fStr + '</a></td></tr></table>';
            }
            lHtml  = lHtml + '<div class="dataStreamResult clearfix"><div class="Mensaje">' + lValue +'</div></div></div>';

        // si no es array
        }else {
            i = 0;
            var headerCells = [];
            lHtml  = lHtml + '<div class="dataStreamResult clearfix"><div class="Mensaje"><table class="Tabla"><tbody>';
            for(var lRow=1;lRow<=pResponse.fRows;lRow++){
                lHtml  = lHtml + '<tr>';
                for(var lColumns=1;lColumns <= pResponse.fCols;lColumns++){
                    var lCell = pResponse.fArray[i];
                    var lValue = '';

                    if(lCell.fType == 'TEXT'){
                        if(lCell.fStr.length == 1){
                            lValue = lCell.fStr.replace('-','&nbsp;');
                        }else{
                            lValue = String(lCell.fStr);
                            lValue = lValue.replace(/(<([^>]+)>)/ig," ");
                            if(lValue.length >= 40){
                                lValue = lValue.substring(0,37) + '...';
                            }
                        }
                    } else if(lCell.fType == 'DATE'){
                        var format = lCell.fDisplayFormat;
                        var number = lCell.fNum;
                        if (! _.isUndefined(format)){
                            // sometimes are seconds, sometimes miliseconds
                            if (number < 100000000000) number = number * 1000;
                            var dt = new Date(number);
                            dt.setTime( dt.getTime() + dt.getTimezoneOffset()*60*1000 );
                            var local = format.fLocale;
                            //(?) if I use "en" doesn't work, I must use "" for "en"
                            if (undefined === local || local === "en" || local.indexOf("en_")) local = "";
                            if (local === "es" || local.indexOf("es_")) local = "es";
                            lValue = $.datepicker.formatDate(format.fPattern, dt, {
                                dayNamesShort: $.datepicker.regional[local].dayNamesShort,
                                dayNames: $.datepicker.regional[local].dayNames,
                                monthNamesShort: $.datepicker.regional[local].monthNamesShort,
                                monthNames: $.datepicker.regional[local].monthNames
                            });
                        }else{
                            lValue = String(number);
                        }
                    } else if(lCell.fType == 'NUMBER'){
                        var displayFormat = lCell.fDisplayFormat;
                        if (displayFormat != undefined) {
                            var number = $.formatNumber(lCell.fNum, {format:displayFormat.fPattern, locale:displayFormat.fLocale});
                            lValue = String(number);
                        } else {
                            lValue = String(lCell.fNum);
                        }
                    } else if(lCell.fType == 'LINK'){
                        var cellStr = '';
                        if(lCell.fStr.length >= 40){
                            cellStr = lCell.fStr.substring(0,37) + '...';
                        }else{
                            cellStr = lCell.fStr;
                        }

                        lValue = '<a target="_blank" href="' + lCell.fUri + '" rel="nofollow" title="' + lCell.fStr + '">' + cellStr + '</a>';
                    }
                    if(typeof lCell.fHeader !== "undefined" && lCell.fHeader == true){
                        headerCells.push(lValue);
                    }else{
                        lHtml  = lHtml + '<td><div>' + lValue + '</div></td>';
                    }
                    i++;
                }
                lHtml  = lHtml +'</tr>';
            }
            lHtml  = lHtml +'</tbody><thead><tr>';
            _.each(headerCells, function(cell) {
                lHtml  = lHtml + '<th><div>' + cell + '</div></th>';
            });
            lHtml  = lHtml +'</tr></thead></table></div></div></div>';
        }
        $lDataServiceContainer.find('#id_dataservice_' + lDataserviceId).html(lHtml);
        $lDataServiceContainer.removeClass('DN');
    } 
}

function onErrorDataServiceExecute(pRequest){
    $.url.setUrl(this.url);
    var lDataServiceId = $.url.param("revision_id");

    var $lDataServiceContainer         = $fDataServicesContainer.find('#id_dataservice_container_' + lDataServiceId);
    var lRetries                       = jQuery.data($lDataServiceContainer[0], "retries");
    var lFirstDisplayedDataStreamId = jQuery.data($('div[id*=id_dataservice_container_]:nth-child(1)')[0], 'dataservice_id');
    var lSecondDisplayedDataStreamId= jQuery.data($('div[id*=id_dataservice_container_]:nth-child(2)')[0], 'dataservice_id');
    var lIsDataStreamBeingDisplayed = true;

    if (lDataServiceId != lFirstDisplayedDataStreamId && lDataServiceId != lSecondDisplayedDataStreamId) {
        lIsDataStreamBeingDisplayed = false;
    }

    if (lRetries < 2) {
        if (!lIsDataStreamBeingDisplayed) {
            $lDataServiceContainer.detach().appendTo($fDataServicesContainer);
        }
        jQuery.data($lDataServiceContainer[0], "retries", ++lRetries);
        initDataService(lDataServiceId);
    } else {
        removeIfIsNotBeingDisplayed(lDataServiceId);
    }
    return false;
}

function removeIfIsNotBeingDisplayed(lDataServiceId){

    var lFirstDisplayedDataStreamId  = jQuery.data($('div[id*=id_dataservice_container_]:nth-child(1)')[0], 'dataservice_id');
    var lSecondDisplayedDataStreamId = jQuery.data($('div[id*=id_dataservice_container_]:nth-child(2)')[0], 'dataservice_id');
    if (lDataServiceId != lFirstDisplayedDataStreamId && lDataServiceId != lSecondDisplayedDataStreamId) {
        $('#id_dataservice_container_' + lDataServiceId).remove();
    } else {
        // retry later!
        setTimeout('removeIfIsNotBeingDisplayed('+lDataServiceId+')', 5000);
    }
}

var HomeChart = Backbone.Model.extend({
    defaults: {
        $Container : null,
        dataStreamId : 0,
        endPoint : '',
        index : 0,
        dataStreamJson : '',
        chartJson : '',
        $DataTableObject : null,
        chartObject : null
    },
    initialize : function(){
        this.executeDataStream();
    },
    executeDataStream : function(){
        var att     = this.attributes;
        var lUrl    = '/rest/datastreams/' + att.dataStreamId + '/data.json/';
        var lData   = '';

        startWaitMessage(att.$Container.find('#id_chartDisplay'));

        $.ajax({
            url: lUrl,
            type: 'GET',
            data: lData,
            cache: false,
            dataType: 'json',
            success: _.bind(this.onSuccessDataStreamExecute, this),
            error: _.bind(this.onErrorDataSreamExecute, this)
        });
    },
    onSuccessDataStreamExecute : function(pResponse){
        ds_results = pResponse; //global, for later use
        var att = this.attributes;
        att.dataStreamJson = pResponse;
        if (pResponse.fType != "ERROR") {
            this.loadDataTable();
            this.loadChart();
            this.renderChart(false);
        }else{
            this.onErrorDataSreamExecute(pResponse);
        }
    },
    onErrorDataSreamExecute : function(pResponse){
        this.attributes.$Container.parents('.dataStreamContainer').remove()
    },
    loadDataTable : function(){
        this.attributes.$DataTableObject = new renderChartsDataTable({'jsonResponse' : this.attributes.dataStreamJson});
    },
    loadChart : function(){
        var att     = this.attributes;
        var lJson   = JSON.parse(att.chartJson);
        var lChart  = lJson.format.type;

        switch(lChart){
            case "barchart":
                att.chartObject = new BarChart({'$DataTable' : att.$DataTableObject, 'chartType' : lChart, 'manager' : this});
                break;
            case "columnchart":
                att.chartObject = new ColumnChart({'$DataTable' : att.$DataTableObject, 'chartType' : lChart, 'manager' : this});
                break;
            case "linechart":
                att.chartObject = new LineChart({'$DataTable' : att.$DataTableObject, 'chartType' : lChart, 'manager' : this});
                break;
            case "piechart":
                att.chartObject = new PieChart({'$DataTable' : att.$DataTableObject, 'chartType' : lChart, 'manager' : this});
                break;
            case "areachart":
                att.chartObject = new AreaChart({'$DataTable' : att.$DataTableObject, 'chartType' : lChart, 'manager' : this});
                break;
            case "geochart":
                att.chartObject = new GeoChart({'$DataTable' : att.$DataTableObject, 'chartType' : lChart, 'manager' : this});
                break;
            case "mapchart":
                att.chartObject = new MapChart({'$DataTable' : att.$DataTableObject, 'chartType' : lChart, 'manager' : this});
                break;
        }

        att.chartObject.loadJson(lJson);
    },
    renderChart : function(){
        startWaitMessage(this.attributes.$Container.find('#id_chartDisplay'));
        var lChart = this.attributes.chartObject;
        lChart.loadJson(JSON.parse(this.attributes.chartJson));
        lChart.convertSelections();
        lChart.renderHome(this.attributes.$Container.find('#id_chartDisplay'), '100%', 200);
    }
})
