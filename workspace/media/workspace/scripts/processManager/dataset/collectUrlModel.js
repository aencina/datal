var CollectUrlModel = StepModel.extend({
	
	defaults:{
		end_point: "",
		mbox: "",
		license_url: "",
		license_url_other: null,
		spatial: "",
		frequency: 'ondemand',
		frequency_other: null,
		collect_type:1,
		impl_type: ""
	},

	validation: {
		end_point: [
			{
				required: true,
				msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
			},{
				pattern: /^(?:(ht|f|sf)tp(s?)\:\/\/)/,
				msg: gettext('VALIDATE-PROTOCOLNOTALLOWED-TEXT')
			},{
				pattern: 'url',
				msg: gettext('VALIDATE-URLNOTVALID-TEXT')
			}
		],
		mbox: [
			{
				required: false
			},{
				pattern: 'email',
				msg: gettext('VALIDATE-EMAILNOTVALID-TEXT')
			}
		],
		license_url: function(value, attr, computedState){
			if(value === 'other' && $.trim(computedState.license_url_other) === '' ) {
				return gettext('VALIDATE-REQUIREDFIELD-TEXT');
			}
		},
		license_url_other: [
			{
				required: false
			},{
				pattern: /^(?:(ht|f|sf)tp(s?)\:\/\/)/,
				msg: gettext('VALIDATE-PROTOCOLNOTALLOWED-TEXT')
			},{
				pattern: 'url',
				msg: gettext('VALIDATE-URLNOTVALID-TEXT')
			}
		],
		frequency: function(value, attr, computedState){
			if(value === 'other' && $.trim(computedState.frequency_other) === '' ) {
				return gettext('VALIDATE-REQUIREDFIELD-TEXT');
			}
		}
	},

	setOutput: function(){

		var output = this.get('output');
		
		output.end_point = $.trim( this.get('end_point') );
		output.mbox = $.trim( this.get('mbox') );
		output.spatial = $.trim( this.get('spatial') );
		output.license_url = $.trim( this.get('license_url') );
		output.frequency = $.trim( this.get('frequency') );
		output.collect_type = this.get('collect_type');
		output.impl_type = this.get('impl_type');

		// Check if license is "other"
		if( output.license_url == 'other' ){
			output.license_url = $.trim( this.get('license_url_other') );
		}

		// Check if frequency is "other"
		if( output.frequency == 'other' ){
			output.frequency = $.trim( this.get('frequency_other') );
		}

		// Set new output
		this.set('output',output);

	},

	setImplementationTypeByMimeType : function(mimeType){
		
		var impl_type = '',
			mimeType = mimeType.split(";")[0].trim(),
			end_point = this.get('end_point');

		switch(mimeType) {
			
			// 0 = HTML
			case "text/html":
				impl_type = 0;
				break;

			// 3 = XML
			case "application/xml":
				impl_type = 3;
				break;
			case "text/xml":
				impl_type = this.checkExtension(end_point);
				if(impl_type == ''){
					impl_type = 3
				}
				break;

			// 4 = XLS
			case "application/vnd.ms-excel":
			case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
				impl_type = 4;
				break;

			// 5 = PDF
			case "application/pdf" :
				impl_type = 5;
				break;

			// 6 = DOC
			case "application/msword":
			case "application/vnd.ms-xpsdocument":
				impl_type = 6;
				break;

			// 7 = ODT
			case "application/vnd.oasis.opendocument.text":
			case "application/vnd.oasis.opendocument.text-web":
				impl_type = 7;
				break;

			// 9 = ODS
			case "application/vnd.oasis.opendocument.spreadsheet":
				impl_type = 9;
				break;

			// 10 = CSV / TXT
			case "text/x-comma-separated-values":
			case "application/csv":
			case "text/plain":
			case "text/csv":
				impl_type = 10;
				break;

			// 11 = KML
			case "application/kml":
			case "application/vnd.google-earth.kml+xml" :
				impl_type = 11;
				break;

			// 12 = KMZ
			case "application/kmz":
			case "application/vnd.google-earth.kmz":
			case "application/vnd.google-earth.kmz .kmz":
				impl_type = 12;
				break;

			// 20 = TSV
			case "text/tab-separated-values":
				impl_type = 20;
				break;
				
            // 24 = RDF
			case "text/turtle":
				impl_type = 24;
				break;

			// Spreadsheet or Word processor
			case "application/octet-stream" :
				impl_type = this.checkExtension(end_point);
				break;

			// Default: set to 0
			default:
				impl_type = 0;

		}

		return impl_type;

	},

	checkExtension : function(filename){
		var filename = filename.split('/');
		filename = filename[filename.length - 1];
		var extension = filename.split('.')[1].toLowerCase();

		var impl_type = '';
		switch(extension) {
			
			// 0 = HTML
			case "html":
				impl_type = 0;
				break;

			// 3 = XML
			case "xml" :
				impl_type = 3;
				break;

			// 4 = XLS
			case "xlsx":
			case "xls":
			case "xlsm":
			case "xltx":
			case "xltm":
			case "xlsb":
			case "xlam":
			case "xll":            	
				impl_type = 4;
				break;

			// 5 = PDF
			case "pdf" :
				impl_type = 5;
				break;

			// 6 = DOC
			case "doc":
			case "docx":
			case "docm":
			case "dotx":
			case "dotm":
				impl_type = 6;
				break;
			
			// 7 = ODT
			case "odt":
				impl_type = 7;
				break;

			// 9 = ODS
			case "ods":
				impl_type = 9;
				break;
			
			// 10 = CSV
			case "csv":
			case "txt":
				impl_type = 10;
				break;

			// 11 = KML
			case "kml":
				impl_type = 11;
				break;

			// 12 = KMZ
			case "kmz":
				impl_type = 12;
				break;

			// 18 = IMAGE
			case "png":
			case "jpg":
			case "jpeg":
			case "gif":
				impl_type = 18;
				break;

			// 19 = ZIP
			case "zip":
			case "rar":
				impl_type = 19;
				break;

			// 20 = TSV
			case "tsv":
				impl_type = 20;
				break;
				
			// 24 = RDF
			case "rdf":
				impl_type = 24;
				break;
			
		}

		return impl_type;
	}

});