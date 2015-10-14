var DatatableDatastreamFilterManager = DatatableFilterManager.extend({
    initialize: function(container, selector){
        DatatableFilterManager.prototype.initialize.call(this, container, selector);
        
		$('#id_create_datastream_overlay').overlay({ top: 'center'
                               , left: 'center'
                               , mask: {
                                   color: '#000'
                                   , loadSpeed: 200
                                   , opacity: 0.5
                                   , zIndex: 99999
                                }
                                , closeOnClick: false
                                , closeOnEsc: true
                                , load: false
                             });
		
		$('#id_create_view', this.get("selector")).click(function(){
			$('#id_create_datastream_overlay').data('overlay').load();
		});
    }
});