var fDataServiceId;
var $fDataService;
var $fDataServiceContainer;

$(document).ready(function(){
    $fDataServiceContainer              = $("#id_dataservice_container");
    fDataServiceId                      = $fDataServiceContainer.data('datastream_id');
    fDataStreamRevisionId               = $fDataServiceContainer.data('datastreamrevision_id');
    $fDataService                       = $fDataServiceContainer.find('#id_dataservice_' + fDataServiceId);
    fHeaderHtml                         = $('<div>').append($fDataService.find('h2').clone()).remove().html();
    initDataService();

    if((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)) || (navigator.userAgent.match(/iPad/i)) || (navigator.userAgent.match(/Andriod/i))){
        $('.gotosource .gotosourceInner').css('width', 'auto');
        $fDataServiceContainer.wrap('<div id="id_wrap"></div>');
        var lHeight = $(window).height();
        var lWidth = $(window).width();
        $('#id_wrap').css({'width' : lWidth, 'height' : lHeight, 'overflow' : 'auto'});
    }

});

function stripColumns(pColumns) {
    // pull out first column:
    var nt = $('<table id="nameTable" cellpadding="3" cellspacing="0"></table>');
    $('#ladderTable tr').each(function(i)
    {
        nt.append('<tr><td class="freezeRow">'+$(this).children('td:first').html()+'</td></tr>');
    });
    nt.appendTo('#id_fixedColumn');
    // remove original first column
    $('#ladderTable tr').each(function(i)
    {
        $(this).children('td:first').remove();
    });
}

function fixHeights() {
    // change heights:
    var curRow = 1;
    $('#ladderTable tr').each(function(i){
        // get heights
        var c1 = $('#nameTable tr:nth-child('+curRow+')').height();    // column 1
        var c2 = $(this).height();    // column 2
        var c3 = $('#totalTable tr:nth-child('+curRow+')').height();    // column 3
        var maxHeight = Math.max(c1, Math.max(c2, c3));

        //$('#log').append('Row '+curRow+' c1=' + c1 +' c2=' + c2 +' c3=' + c3 +'  max height = '+maxHeight+'<br/>');

        // set heights
        //$('#nameTable tr:nth-child('+curRow+')').height(maxHeight);
        $('#nameTable tr:nth-child('+curRow+') td:first').height(maxHeight);
        //$('#log').append('NameTable: '+$('#nameTable tr:nth-child('+curRow+')').height()+'<br/>');
        //$(this).height(maxHeight);
        $(this).children('td:first').height(maxHeight);
        //$('#log').append('MainTable: '+$(this).height()+'<br/>');
        //$('#totalTable tr:nth-child('+curRow+')').height(maxHeight);
        $('#totalTable tr:nth-child('+curRow+') td:first').height(maxHeight);
        //$('#log').append('TotalTable: '+$('#totalTable tr:nth-child('+curRow+')').height()+'<br/>');

        curRow++;
    });

    if ($.browser.msie)
        $('#id_mainTable').height($('#id_mainTable').height()+18);
}

function initDataService(){
    $fDataServiceContainer.find('a[id*=id_resetDataServiceButton_]').bind('click', onResetDataServiceButtonClicked);
    startWaitMessage($fDataService);
    var lEndPoint = $fDataServiceContainer.data('dataservice_end_point');

    invokeDataService(lEndPoint);

    if (areEmbedOptionsEnabled) {
        var lActionsMenu = new ActionsMenu();

        var lUrl        = $fDataServiceContainer.data("permalink");
        var lName       = $fDataServiceContainer.data('dataservice_title');
        $('a[id*=id_menuShareDataServiceButton_]').click(onClickShareMenu);
        $('div[id*=id_tooltipShareDataServiceButton_]').mouseleave(closeDataServiceShareTooltip);
        $('div[id*=id_tooltipShareDataServiceButton_] .J .ic_Menu').click(closeDataServiceShareTooltip);
//		try{
//			var lInputShareBox = new InputShareBox({
//				'$Container': $('.shareMenu .share_url_input')
//				, 'shortUrl': lUrl
//				, 'longUrl': lUrl
//			});
//
//			var lTwitterShareBox = new TwitterShareBox({
//				'$Container': $('.shareMenu li.twitter iframe')
//				, 'shortUrl': lUrl
//				, 'longUrl': lUrl
//				, 'title': lName
//				, 'count': 'horizontal'
//				, 'width': 20
//				, 'height': 112
//			});
//
//			var lFacebookShareBox = new FacebookShareBox({
//				'$Container': $('.shareMenu li.facebook iframe')
//				, 'shortUrl': lUrl
//				, 'longUrl': lUrl
//				, 'layout': 'button_count'
//				, 'width': 20
//				, 'height': 112
//			});
//
//			var lGooglePlusShareBox = new GooglePlusShareBox({
//				'$Container': $('.shareMenu li.google div')
//				, 'shortUrl': lUrl
//				, 'longUrl': lUrl
//				, 'size': 'medium'
//			});
//
//			var lLinkedinShareBox = new LinkedinShareBox({
//				'$Container': $('.shareMenu li.linkedin iframe')
//				, 'shortUrl': lUrl
//				, 'longUrl': lUrl
//				, 'data_counter': 'right'
//			});
//
//			lShareBoxes = new ShareBoxes();
//			lShareBoxes.add(lInputShareBox);
//			lShareBoxes.add(lTwitterShareBox);
//			lShareBoxes.add(lFacebookShareBox);
//			lShareBoxes.add(lGooglePlusShareBox);
//			lShareBoxes.add(lLinkedinShareBox);
//
//			if (typeof(BitlyClient) != 'undefined') {
//				BitlyClient.shorten(lUrl, 'onSuccessUrlShortened');
//			}
//		}catch(e){
//		}

        $(':not(.actionsMenu,.actionsMenu *,.shareMenu *,.shareMenu)').click(function(event){
            event.stopPropagation();
            $('[id*=id_tooltipDataServiceButton_]').fadeOut('fast');
            closeDataServiceShareTooltip();
		});
    }

}

function startWaitMessage(pHTMLElement){

    var lHtml = "<table class='Loading'><tr><td>&nbsp";
    lHtml = lHtml + "</td></tr></table>";
    pHTMLElement.html(lHtml);
}

function invokeDataService(pEndPoint){

    var lUrl     = '/rest/datastreams/' + fDataStreamRevisionId + '/data.json/';
    var lData    = '&limit=50'
    			+ pEndPoint;

    $.ajax({ url: lUrl
            , type:'GET'
            , data: lData
            , dataType: 'json'
            , success: onSuccessDataServiceExecute
            , error: onErrorDataServiceExecute
            }
    );
}

function onSuccessDataServiceExecute(pResponse){

    var lDataserviceId = $fDataServiceContainer.data('datastream_id');
    var lHtml = '<div class="dataStreamBox clearfix">';
        lHtml += fHeaderHtml;

    if(pResponse.fType!='ARRAY'){
        var lValue = '';
        if(pResponse.fType == 'TEXT'){
            var str = String(pResponse.fStr);
            str = str.replace(/(<([^>]+)>)/ig," ");
            lValue = '<table class="Texto"><tr><td>' + str + '</td></tr></table>';
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
        } else if(pResponse.fType == 'ERROR'){
            lValue = '<table class="Nulo"><tr><td> ' + gettext( "APP-NODATAFOUD-TEXT" ) + '. <span>' + gettext( "APP-PLEASE-TEXT" ) + ' <a id="id_retryDataServiceButton" href="javascript:;" title="' + gettext( "APP-TRYAGAIN-TITLE" ) + '">' + gettext( "APP-TRYAGAIN-TEXT" ) + '</a>.</span></td></tr></table>';
        }
        lHtml  = lHtml + '<div class="dataStreamResult clearfix"><div class="Mensaje">' + lValue +'</div></div>';
    } else {
        i = 0;
        lHtml  = lHtml + '<div class="dataStreamResult clearfix"><div class="Mensaje"><div id="id_fixedColumn" style="float:left;"></div><div id="id_mainTable" style="width:100%;"><table id="ladderTable" class="Tabla" >';
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
                    lValue = '<a target="_blank" href="' + lCell.fUri + '" rel="nofollow" title="' + lCell.fStr + '">' + lCell.fStr + '</a>';
                }

                if (typeof lCell.fHeader !== "undefined" && lCell.fHeader == true) {
                    lHtml  = lHtml + '<th><div>' + lValue + '</div></th>';
                }else{
                    lHtml  = lHtml + '<td><div>' + lValue + '</div></td>';
                }
                i++;
            }
            lHtml  = lHtml +'</tr>';
        }

        if(pResponse.fLength > 50){
            var lURL = $fDataServiceContainer.data("permalink");
            lHtml  = lHtml +'</table><a href="'+lURL+'" target="_blank" class="viewMoreLink">' + gettext( "APP-VIEWMORE-TEXT" ) + '</a></div></div>';
        }else{
            lHtml  = lHtml +'</table></div></div>';
        }
    }
    lHtml = lHtml + '</div>';
    $fDataService.html(lHtml);

    // tables long text rendering fix
    var $lTable = $fDataServiceContainer.find('.Tabla');
    if ($lTable.size() == 1) {
        var lMaxWidth = 150;
        for(var lColumn = 1; lColumn <=pResponse.fCols; lColumn++){
            var $lColumns = $lTable.find('tr td:nth-child('+ lColumn +')');
            var lWidth = 0;
            $lColumns.each(function(){
                var $lTd = $(this);
                var lTdWidth = $lTd.width();
                if (lTdWidth > lWidth) {
                    lWidth = lTdWidth;
                }
                if (lWidth > lMaxWidth) {
                    lWidth = lMaxWidth;
                }
            });

            $lColumns.each(function(){
                $(this).width(lWidth + 29);// plus paddings + 5px width for IE
            });
        }
        $lTable.addClass('tableFix').animate({opacity: 1}, 1000);
    }
    var lWidth = $fDataServiceContainer.find(".Mensaje table").width();
    $fDataServiceContainer.find('.dataStreamBox').css('width', lWidth);

    var lHeaderRow = $fDataServiceContainer.data('header_row');
    if (lHeaderRow) {
        $fDataService.find('.Tabla').before($('<table>').addClass('Tabla tableFix headerRows').html($fDataService.find('tr:lt('+lHeaderRow+')').detach()));
        var lMarginTop = 36 + ( 20 * lHeaderRow);
        $fDataService.find('.Mensaje').css('margin-top', lMarginTop + 'px');
        $fDataService.find('.headerRows').css('width', lWidth);
        $(window).scroll(function(pEvent) {
            var lLeft = $('a.clearfix').offset().left;
            $fDataService.find('.headerRows').css('left', '-' + lLeft + 'px');
         });
    }

    $fDataServiceContainer.find('#id_retryDataServiceButton').bind('click', onResetDataServiceButtonClicked);
    
    if($fDataServiceContainer.data('fixed_column')){
        stripColumns($fDataServiceContainer.data('fixed_column'));
        fixHeights();
    }
}

function onErrorDataServiceExecute(pRequest){

    if(pRequest.status != ''){
        var lMessage   = pRequest.status + ': ' + pRequest.statusText;
    }

    var lEndPoint = $fDataServiceContainer.data('dataservice_end_point');

    var lHtml  = '<div class="dataStreamBox clearfix" >';
    lHtml += fHeaderHtml;

    lHtml        = lHtml + '<div class="dataStreamResult clearfix"><div class="Mensaje clearfix">';
    lHtml        = lHtml + '<table class="Nulo">';
    lHtml        = lHtml + '<tr>';
    lHtml        = lHtml + '<td><div> ' + gettext( "APP-OOPS-TEXT" ) + ' <span>' + gettext( "DS-CANTLOADDATA-TEXT" ) + '.</span><span>' + gettext( "APP-PLEASE-TEXT" ) + ' <a id="id_retryDataServiceButton" href="javascript:;" title="' + gettext( "APP-TRYAGAIN-TITLE" ) + '">' + gettext( "APP-TRYAGAIN-TEXT" ) + '</a>.</span></div></td>';
    lHtml        = lHtml + '</tr>';
    lHtml        = lHtml + '</table>';
    lHtml        = lHtml + '</div></div></div>';

    $fDataService.html(lHtml);

    $fDataServiceContainer.find('#id_retryDataServiceButton').bind('click', onResetDataServiceButtonClicked);
}

function onResetDataServiceButtonClicked(pEvent){
    startWaitMessage($fDataService);
    var lEndPoint   = $fDataServiceContainer.data('dataservice_end_point');
    invokeDataService(lEndPoint);
    return false;
}
