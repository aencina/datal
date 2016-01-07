/*
 * jQuery UI TaggingSource @VERSION
 * Created by : mmenafra
 *
 * Depends:
 *	jquery.ui.core.js
 *	jquery.ui.widget.js
 *  jquery.ui.autocomplete.js
 *
 */
(function($, undefined){
    $.widget("ui.taggingSources", {
        options: {
            source : '',
            minLength : 0,
            sourceContainer : null,
           	sources: [],
           	prefixId : 'id_source_'
        },
        _create: function(){
            var self = this,
                options = self.options;
			
			self.$SourceName 	= $('#id_source_name');
			self.$SourceUrl 	= $('#id_source_url');
			
            if(typeof options.sourceContainer === "string"){
                self.sourceContainer = jQuery(options.sourceContainer);
		self.element.after(self.sourceContainer);
            }else if (options.sourceContainer == null) {
                self.sourceContainer = jQuery('<div id="id_source_container" class="tagsContent"></div>');
                self.element.after(self.sourceContainer);
            } else {
                self.sourceContainer = options.sourceContainer;
            }

            if (options.sources != null) {
            	jQuery.each(options.sources, function(pIndex, pValue){
            		self._createSource(pValue.value, pValue.url, pValue.id, pValue.type);
            	});
            }
			
            //dependency with autocomplete widget
            self.element.autocomplete({
                source: options.source,
                minLength: options.minLength,
                select: function(pEvent, ui){
                    if (self.options.disabled) {
                        return;
                    }
                    self._onSourceSelected(pEvent, ui);
                    return false;
                }

            	
            }).data( "ui-autocomplete" )._renderItemData = function( ul, item ) {
                var iconType
            	switch(item.type)
                {
                      case "dt":
                		iconType = "ic_Dset";
                		break;
                	case "ds":
                		iconType = "ic_Data";
                		break;
                	
                	case "vz":
                		iconType = "ic_Chart";
                		break;

                	case "db":
                		iconType = "ic_Dashboard";
                		break;
                			
                			
                    default:
                    	iconType = ""
                        break;
                			
                }
            	$( "<li></li>" ).data( "ui-autocomplete-item", item ).append( "<a><span class='" + iconType + "'>" + item.label + "</span></a>" ).appendTo( ul);          	
            	return;
            	
            };
            self.sourceContainer.bind('click', function(pEvent){
                if (self.options.disabled) {
                    return;
                }
                self._onRemoveSource(pEvent);
            });
			
			$('#id_addSource').bind('click', function(pEvent){
                if (self.options.disabled) {
                    return;
                }
                self._onAddNewSource(pEvent);
            });
        },
		_onAddNewSource : function(pEvent){
			var self = this;
            self._trigger('sourceSelected', pEvent);
			
			var l$Name = self.$SourceName;
			var lUrl = jQuery.trim( self.$SourceUrl.val() );
			
			//if(self.$SourceForm.valid()){
				self._addSource(l$Name, lUrl, '', '');
	            self._trigger('sourceAdded', pEvent);
			//}

            return;
		},
        _onSourceSelected: function(pEvent, ui){
            var self = this;
            self._trigger('sourceSelected', pEvent, ui);
			
            var key = jQuery.ui.keyCode;
            var $Source = jQuery(pEvent.target);
            var idResource = ui.item.id
            var typeResource = ui.item.type
            $Source.val(ui.item.value);
			
            if (pEvent.keyCode == key.ENTER) {
                self._addSource($Source, '', idResource, typeResource);
                self._trigger('sourceAdded', pEvent);
                $Source.val('');
            }
            if (pEvent.button == 0) {
                self._addSource($Source, '', idResource, typeResource);
                self._trigger('sourceAdded', pEvent);
                $Source.val('');
            }
            return;
        },
        _addSource: function(pNewSource, pUrl, pIdResource, typeResource){
            var $NewSource = jQuery(pNewSource);
            this._createSource($NewSource.val(), pUrl, pIdResource, typeResource);
            $NewSource.val('');
			this.$SourceUrl.val('');
        },
        _createSource: function(pSource, pUrl, pIdResource, pTypeResource){
        	var id;
        	var typeResource
        	// if (undefined == pSource) pSource = "";
            var name = jQuery.trim(pSource.replace(/[^a-zA-Z0-9 áéíóúAÉÍÓÚÑñ]/g, " "));
            if (name.length > 0) {
            	if (typeof pIdResource !== 'undefined' && pIdResource.length > 0){
            		id = pIdResource;
            	}
            	else{
            		id = this.options.prefixId + name.replace(/\s+/g, "").toLowerCase();
            	}
            	
            	switch(pTypeResource){
        		case 'dt':
        			typeResource = 'ic_Dset';
        			break;
        		case 'ds':
        			typeResource = 'ic_Data';
        			break;
        		case 'vz':
        			typeResource = 'ic_Chart';
        			break;
        		case 'db':
        			typeResource = 'ic_Dashboard';
        			break;
        	}
                var $SourcesContainer = this.sourceContainer;
                if ($SourcesContainer.find('#' + id + '_tag').length == 0) {
                    var html = '<span id="' + id + '_tag" class="tag">';
                    html += '<span class="tagInner clearfix">';
                    html += '<span class="tagTxt" id="' + id + "_"+ pTypeResource+'" data="'+pUrl+'"><span class="icon '+ typeResource + '"></span>' + name + '</span>';
                    html += '<a href="javascript:;" rel="#' +id + '_tag" title="Remove Source"><span class="DN">Remove Source</span></a>';
                    html += '</span>';
                    html += '</span>';
                    $SourcesContainer.append(html);
                    return true;
                }
            }
            return false;
        },
        _onRemoveSource: function(pEvent){
            var self = this;
            var target = jQuery(pEvent.target);
            if (target.is('span')) {
                target = target.parent();
            }
            if (target.is('a')) {
                jQuery(target.attr('rel')).remove();
                self._trigger('sourceRemoved', pEvent);
            }
            return;
        },
        destroy: function(){
            var self = this;
            //jQuery.widget.prototype.destroy.apply(self, arguments);
            self.element.autocomplete('destroy');
            self.sourceContainer.remove();
        }
    });
    jQuery.extend(jQuery.ui, {
        version: "@VERSION"
    });
}(jQuery));