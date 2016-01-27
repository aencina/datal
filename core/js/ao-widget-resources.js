/*
 * jQuery UI Widget Resources Dashboards, Visualizations and Data Streams @VERSION
 * Created by : DATAL
 * 
 * Depends:
 *	jquery.ui.core.js
 *	jquery.ui.widget.js
 * 
 */
(function($, undefined){
    $.widget("ui.widgetResources", {
        options: {
			apiUrl : '',
			apiKey : '',
			metaData : '',
			page : '',
			limit : ''
        },
        _create: function(){
            var self = this,
                options = self.options;
			
			self.json = '';
            self._getResources();
        },
		_getResources : function(){
			var self = this;
			var lUrl  = self.options.apiUrl + '/resources/search/';
			var lData = "&auth_key=" + self.options.apiKey;
			if(self.options.searchTerms != ""){
                lData += "&q=" + self.options.searchTerms;
            }
			if(self.options.metaData != ""){
                lData += "&meta=" + self.options.metaData;
            }
            if(self.options.page != ""){
                lData += "&page=" + self.options.page;
            }
            if(self.options.limit != ""){
                lData += "&limit=" + self.options.limit;
            }
			
			self.element.html('<div class="ao-loading">Cargando...</div>');
			
		    $.ajax({ url: lUrl
			            , data:lData
			            , dataType: 'jsonp'
						, context : self
			            , success: function(pResponse){
							this.json = pResponse;
							this._parseResources();
						}, 
						error : function(pResponse){
							this.element.html('<span class="ao-error">An error has ocurred trying to load your widget! Please refresh page</span');
						}
		            });
		},
		_parseResources : function(){
			var self = this;
			var lJson = self.json;
			var lHtml = '';
			lHtml += '<div class="ao-resources"><table class="ao-resources-table">';
			
			for (var i =0; i< lJson.length; i++){
				var lValue = lJson[i];
				lHtml += '<tr class="ao-resources-row">';
				lHtml += '<td class="ao-resources-cell ao-resources-text">';
				if(lValue.type == "datastream"){
                    lHtml += '<a href="'+lValue.link+'" title="'+lValue.title+' - '+lValue.subtitle+'" class="ao-resources-text-link"><strong>'+lValue.title+'</strong><span class="ao-sep"> - </span>'+lValue.subtitle+'</a>';
                }
                if(lValue.type == "dashboard"){
                    lHtml += '<a href="'+lValue.link+'" title="'+lValue.title+'" class="ao-resources-text-link">'+lValue.title+'</a>';
                }
				
				lHtml += '<div class="ao-resources-text-description">'+lValue.description+'</div>';
				lHtml += '<div class="ao-resources-tags"><div class="ao-resources-tags-title">Tags: </div>';
				var lTags = lJson[i].tags;
				for (var j = 0; j < lTags.length; j++) {
					if(lTags.length-1 == j){
						lHtml += '<a href="" title="'+lTags[j]+'" class="ao-resources-tags-item">'+lTags[j]+'</a>';
					}else{
						lHtml += '<a href="" title="'+lTags[j]+'" class="ao-resources-tags-item">'+lTags[j]+'</a><span class="ao-comma">,</span> ';
					}
				}
				lHtml += '</div></td>';
                lHtml += '<td class="ao-resources-cell ao-resources-type"><a href="'+lValue.link+'" title="View '+lValue.type+'" class="ao-resources-'+lValue.type+'-link">View '+lValue.type+'</a></td>';
			};
			
			lHtml += '</table></div>';
			
			this.element.html(lHtml);
		},
        destroy: function(){
            var self = this;
            //jQuery.widget.prototype.destroy.apply(self, arguments);
        }
    });
    jQuery.extend(jQuery.ui, {
        version: "@VERSION"
    });
}(jQuery));