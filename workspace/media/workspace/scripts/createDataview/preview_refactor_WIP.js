
if(result.fType != 'ARRAY'){
	var value = '';
	switch(result.fType ){
		case "TEXT":
			var str = String(result.fStr);
			str = str.replace(/(<([^>]+)>)/ig," ");
			value = '<table class="text"><tr><td>' + str + '</td></tr></table>';
			break;
		case "DATE":
			value = '<table class="number"><tr><td></td></tr></table>';
			break;
		case "NUMBER":
			var format = result.fDisplayFormat;
			var number = ( _.isUndefined(format) ) ? result.fNum : $.formatNumber( result.fNum, {format:format.fPattern, locale:format.fLocale} );
			value = '<table class="number"><tr><td>' + String(number) + '</td></tr></table>';
			break;
		case "LINK":
			value = '<table class="text"><tr><td><a target="_blank" href="' + result.fUri + '" rel="nofollow" title="' + result.fStr + '">' + result.fStr + '</a></td></tr></table>';
			break;
		case "ERROR":
			value = '<table class="null"><tr><td> ' + gettext( "APP-NODATAFOUD-TEXT" ) + '. <span>' + gettext( "APP-PLEASE-TEXT" ) + ' <a id="id_retryButton" title="' + gettext( "APP-TRYAGAIN-TITLE" ) + '">' + gettext( "APP-TRYAGAIN-TEXT" ) + '</a>.</span></td></tr></table>';
			break;
	}

	return value;

} else {
	var output = '<table class="array">';

	var firstHeader = false,
			stopHeaders = false,
			i = 0;

	result.headerCells = [];

	for(var row=0; row < result.fRows;row++){
		output += '<tr>';

		for(var col=0;col<result.fCols;col++){
			var cell = result.fArray[i],
				value = '';

			if (cell.fType == "TEXT" && ! _.isUndefined(cell.fDisplayFormat))	{
				fmt = cell.fDisplayFormat.fPattern;
				if (fmt.indexOf("#") == -1) {
					cell.fType = "DATE";
				}
			}

			switch(cell.fType){
				case "TEXT":
					value = ( cell.fStr.length != 1 ) ? cell.fStr : cell.fStr.replace('-', '&nbsp;');
					value = value.replace(/(<([^>]+)>)/ig," ");
					break;
				case "DATE":
					var format = cell.fDisplayFormat;
					var number = cell.fNum;
					if (! _.isUndefined(format)) {
						// sometimes are seconds, sometimes miliseconds
						if (number < 100000000000) number = number * 1000;
						var dt = new Date(number);
						var local = format.fLocale;
						//(?) if I use "en" doesn't work, I must use "" for "en"
						if (undefined === local || local === "en" || local.indexOf("en_")) local = "";
						if (local.indexOf("es_")) local = "es";

						value = $.datepicker.formatDate(format.fPattern, dt, {
							dayNamesShort: $.datepicker.regional[local].dayNamesShort,
							dayNames: $.datepicker.regional[local].dayNames,
							monthNamesShort: $.datepicker.regional[local].monthNamesShort,
							monthNames: $.datepicker.regional[local].monthNames
						});
					} else {
						value = String(number);
					}
					break;
				case "NUMBER":
					var format = cell.fDisplayFormat,
					number = ( _.isUndefined(format) ) ? cell.fNum : $.formatNumber( cell.fNum, {format:format.fPattern, locale:format.fLocale} );
					value = String(number);
					break;
				case "LINK":
					value = '<a target="_blank" href="' + cell.fUri + '" rel="nofollow" title="' + cell.fStr + '">' + cell.fStr + '</a>';
					break;
			}

			if(cell.fHeader && !stopHeaders){
				firstHeader = true;
				result.headerCells.push(value);
			}	else {
				output += '<td>' + value + '</td>';
			}

			i++;

		}

		if(firstHeader){
			stopHeaders = true;
		}

		output += '</tr>';

	}

	output += '</table>';
}
