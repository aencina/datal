var DatatableSearchManager = Backbone.Model.extend({
    initialize: function(container, selector){
        $(this.get("container")).bind('search:get', _.bind(this.getSearch, this));
        $('.search_datatable').keypress(_.bind(this.onKeypress, this));
        // $('.search_datatable').blur(_.bind(this.onBlur, this));

        },
    getSearch: function(event) {
        $(this.get("container")).trigger('datatable:set:search', [this.get("search")]);
    },
    onKeypress: function(event) {
        if ( event.which == 13 ) {
            this.search();
        }
    },
    /*
    onBlur: function(event) {
        this.search();
    },
    */
    search : function(){
        this.set({search: $('.search_datatable').val()});
        $(this.get("container")).trigger('datatable:refresh:filter');
    }
});