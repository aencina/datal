var FinishWebserviceModel = FinishModel.extend({

	setDataFromOutput: function(){

		var output = this.get('output'),
			data = this.get('data');

		data.mbox = output.mbox;
		data.end_point = output.end_point;
		data.impl_type = output.impl_type;
		data.path_to_headers = output.path_to_headers;
		data.path_to_data = output.path_to_data;
		data.token = output.token;
		data.algorithm = output.algorithm;
		data.username = output.username;
		data.password = output.password;
		data.signature = output.signature;
		data.method_name = output.method_name;
		data.namespace = output.namespace;
		data.use_cache = output.use_cache;
		data.att_headers = output.att_headers;
		data.param_name = output.param_name;
		data.default_value = output.default_value;
		data.enable_editable = output.enable_editable;
		data.spatial = output.spatial;
		data.license_url = output.license_url;
		data.frequency = output.frequency;
		data.collect_type = output.collect_type;
		
		// Prepare Params for Data
		data['params-TOTAL_FORMS'] = output.params.length;
		data['params-INITIAL_FORMS'] = '0';
		data['params-MAX_NUM_FORMS'] = '';
		for( var i=0;i<output.params.length;i++ ){
			for( var paramName in output.params[i] ){
				data['params-'+i+'-'+paramName] = output.params[i][paramName]
			}
		}
		
		this.set('data',data);

	}

});