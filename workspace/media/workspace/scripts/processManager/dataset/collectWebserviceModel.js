var CollectWebserviceModel = StepModel.extend({

	defaults:{
		end_point: "",
		impl_type: 14,
		impl_details: "",
		path_to_headers: "",
		path_to_data: "",
		token: "",
		algorithm: "",
		username: "",
		password: "",
		signature: "",
		method_name: "",
		namespace: "",
		use_cache: "",
		params: [],
		collect_type: 2
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
		path_to_data: function(value, attr, computedState){

			var impl_type = parseInt(computedState.impl_type);

			if(impl_type == 14){
				if($.trim(value).length == 0){
					return gettext('VALIDATE-REQUIREDFIELD-TEXT');
				}
			}

		},
		signature: {
			maxLength: 256,
			msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 256 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
		},
		token: {
			maxLength: 256,
			msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 256 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
		}
	},

	setOutput: function(){

		var output = this.get('output');
		
		output.end_point = $.trim( this.get('end_point') );
		output.impl_type = $.trim( this.get('impl_type') );
		output.path_to_headers = $.trim( this.get('path_to_headers') );
		output.path_to_data = $.trim( this.get('path_to_data') );
		output.token = $.trim( this.get('token') );
		output.algorithm = $.trim( this.get('algorithm') );
		output.username = $.trim( this.get('username') );
		output.password = this.get('password');
		output.signature = $.trim( this.get('signature') );
		output.method_name = $.trim( this.get('method_name') );
		output.namespace = $.trim( this.get('namespace') );
		output.use_cache = $.trim( this.get('use_cache') );
		output.collect_type = this.get('collect_type');
		output.params = this.get('params');

		// Set new output
		this.set('output',output);

	},

	parseImplDetails: function(){

		var impl_details = this.get('impl_details');
			$impl_details = $(_.unescape( this.get('impl_details') ) ),
			$parsedXML = $($.parseXML( _.unescape( this.get('impl_details') ) ) ),
			use_cache = false,
			signature = '';	
		
		if($impl_details.attr('useCache') == "True") {
			use_cache = true;
		}
		this.set('use_cache', use_cache);
				
		if( this.get('impl_type') == 1 ){
			this.set('method_name', $impl_details.find('methodName').text());
			this.set('namespace', $impl_details.find('targetNamespace').text());
		}else if( this.get('impl_type') == 14 ){
			this.set('path_to_headers', $impl_details.find('pathToHeaders').text());
			this.set('path_to_data', $impl_details.find('pathToData').text());
			this.set('token', $impl_details.find('token').text());
			this.set('algorithm', $impl_details.find('algorithm').text());
			this.set('username', $impl_details.find('userName').text());
			this.set('password', $impl_details.find('password').text());
			if( $parsedXML.find('uriSignatures > *').length > 0 ) {
				signature = $parsedXML.find('uriSignatures > *').get(0).nodeName;
				if(signature == 'sign_name'){
					signature = '';
				}
			}
			this.set('signature', signature);
		}

		// Params
		var $args = $parsedXML.find('args > *'),
			params = [];

		$args.each(function(){
			
			var name = this.nodeName,
				element = $(this),
				default_value = element.text(),
				editable = false;

			if(typeof element.attr('editable') != "undefined" && element.attr('editable') != "false"){
				editable = true;
			}

			params.push({
				name: name,
				default_value: default_value,
				editable: editable
			});

		});

		this.set('params',params);

	}

});