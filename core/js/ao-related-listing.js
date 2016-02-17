/*
 * jQuery UI Widget Related Dashboards, Visualizations and Data Streams @VERSION
 * Created by : DATAL
 * 
 * Depends:
 *	jquery.ui.core.js
 *	jquery.ui.widget.js
 * 
 */
(function($, undefined){
    $.widget("ui.widgetRelated", {
        options: {
			apiUrl : '',
			apiKey : '',
			widgetTitle : '',
            searchTerms : '', 
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
			var lData = "auth_key=" + self.options.apiKey + "&" + $.param(self.options.metaData);
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

			lHtml += '<div class="ao-related"><div class="ao-related-title">'+self.options.widgetTitle+'</div>';
			lHtml += '<div class="ao-related-content">';

			for (var i =0; i < lJson.length ; i++){
				var lValue = lJson[i];
				if(lValue.type == "datastream"){
				    lHtml += '<div class="ao-related-item"><a href="'+lValue.link+'" title="'+lValue.title+ ' - '+ lValue.subtitle + '" class="ao-related-item-link"><strong>'+lValue.title+'</strong> <span class="ao-sep"> - </span> '+ lValue.subtitle+'</a>';
				}
				if(lValue.type == "dashboard"){
                    lHtml += '<div class="ao-related-item"><a href="'+lValue.link+'" title="'+lValue.title+'" class="ao-related-item-link">'+lValue.title+'</a>';
                }
				lHtml += '<div class="ao-related-item-description">'+lValue.description+'</div></div>';
			};
			
			lHtml += '</div></div>';
			
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