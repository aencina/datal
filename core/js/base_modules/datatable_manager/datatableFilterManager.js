var DatatableFilterManager = Backbone.Model.extend({
    initialize: function(container, selector){
        $('.filter_category', this.get("selector")).click(_.bind(this.onClickCategoryFilter, this));
        $('.filter_all', this.get("selector")).click(_.bind(this.onClickAllFilter, this));
        $('.filter_mine', this.get("selector")).click(_.bind(this.onClickMineFilter, this));
        $('.filter_status', this.get("selector")).click(_.bind(this.onClickStatusFilter, this));
        $('.one_category_filter', this.get("selector")).click(_.bind(this.onClickOneCategory, this));
        
        $(this.get("container")).bind("filter:get:categories",  _.bind(this.sendCategories, this));
        $(this.get("container")).bind("filter:get:status",  _.bind(this.sendStatus, this));
        $(this.get("container")).bind("filter:get:whom",  _.bind(this.sendWhom, this));
    },
    sendCategories: function() {
	    $(this.get("container")).trigger('datatable:set:categories', [this.get("categories")]);	
    },
    sendOneCategory: function(category) {
        this.set({"categories": category});
	    $(this.get("container")).trigger('datatable:set:categories', [this.get("categories")]);	
    },
        
    sendStatus: function() {
        $(this.get("container")).trigger('datatable:set:status', [this.get("status")]);  
    },
    sendWhom: function() {
        $(this.get("container")).trigger('datatable:set:whom', [this.get("whom")]);  
    },
    updateCategories: function() {
		var temp_filters = '';
        $('.filter_category > span.filter-active', this.get("selector")).each(function(i, e) {
            temp_filters += $(e).parent().data("id") + ',';            
        });
        if (temp_filters != '') {
            temp_filters = temp_filters.substring(0, temp_filters.length-1);
        }
        this.set({"categories": temp_filters});
    },
    cleanCategories: function(){
        this.set({"categories": ''});
        $('span.filter-active').removeClass('filter-active');
    },
    updateStatus: function() {
        var temp_filters = '';
        $('.filter_status > span.filter-active', this.get("selector")).each(function(i, e) {
            temp_filters += $(e).parent().data("id") + ',';            
        });
        if (temp_filters != '') {
            temp_filters = temp_filters.substring(0, temp_filters.length-1);
        }
        this.set({"status": temp_filters});
    },
    updateMine: function() {
        if (!$('.filter_mine', this.get("selector")).hasClass('filter-active')) {
            $('.filter_mine', this.get("selector")).toggleClass('filter-active');
            $('.filter_all', this.get("selector")).toggleClass('filter-active');    
            this.set({"whom": false});            
        }
    },
    updateAll: function() {
        if (!$('.filter_all', this.get("selector")).hasClass('filter-active')) {
            $('.filter_all', this.get("selector")).toggleClass('filter-active');
            $('.filter_mine', this.get("selector")).toggleClass('filter-active');
            this.set({"whom": true});
        }
    },
    onClickCategoryFilter: function(event) {
        event.preventDefault();
        var $Target = $(event.target);
		$Target.toggleClass('filter-active');
		this.updateCategories();
		this.sendCategories();
        $(this.get("container")).trigger('datatable:refresh:filter');
    },
    onClickOneCategory: function(event) {
        event.preventDefault();
        var $Target = $(event.currentTarget);
        category = $Target.data("category");
        sel = $('span[title="'+category+'"]')[0];
		$(sel).addClass('filter-active');
		this.sendOneCategory( category );
        $(this.get("container")).trigger('datatable:refresh:filter');
    },
    emulateClickCategoryFilter: function(category){
        sel = $('span[title="'+category+'"]')[0];
        $(sel).trigger('click');
    },
        
    onClickAllFilter: function(event) {
        event.preventDefault();
        this.updateAll();
        this.sendWhom();
        $(this.get("container")).trigger('datatable:refresh:filter');
    },
    onClickMineFilter: function(event) {
        event.preventDefault();
        this.updateMine();
        this.sendWhom();
        $(this.get("container")).trigger('datatable:refresh:filter');
    },
    onClickStatusFilter: function(event) {
        event.preventDefault();
        var $Target = $(event.target);
		$Target.toggleClass('filter-active');
		this.updateStatus();
		this.sendStatus();
        $(this.get("container")).trigger('datatable:refresh:filter');
    }
});
