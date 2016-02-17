var DatatableHomeFilterManager = DatatableFilterManager.extend({
    initialize: function(container, selector){
        $('.filter_category', this.get("selector")).click(_.bind(this.onClickCategoryFilter, this));
        //$('.filter_all', this.get("selector")).click(_.bind(this.onClickAllFilter, this));
        $("#apply_filters", this.get("selector")).click(_.bind(this.onClickApplyFilters, this));
        $("#id_filter_entity", this.get("selector")).change(_.bind(this.onChangeEntity, this));
        $('.one_category_filter').click(_.bind(this.onClickOneCategory, this));
        
        $('.filter_type', this.get("selector")).click(_.bind(this.onClickTypeFilter, this));
        
        $(this.get("container")).bind("filter:get:categories",  _.bind(this.sendCategories, this));
        $(this.get("container")).bind("filter:get:type",  _.bind(this.sendType, this));

        //$(this.get("container")).bind("filter:get:source_choice",  _.bind(this.sendSourceChoice, this));
        $(this.get("container")).bind("filter:get:whom",  _.bind(this.sendWhom, this));

        $(this.get("container")).on("click", "#goto_entity", function(e) {
          e.preventDefault();
          var url = $("#entities option:selected").data('url');
          if (url) {
            if (url.match("^(http|https)://") == null) {
              url = "http://" + url;
            }

            window.open(url);
          }
        });

        this.set({"whom": true});
        this.sendWhom();
    },
    updateAll: function() {
        if ($('.filter_all', this.get("selector")).hasClass('filter-active')) {
            $('.filter_type span', this.get("selector")).removeClass('filter-active');
            this.set({"whom": true});
        }
    },
    updateCategories: function() {
        var temp_filters = '';
        $('.filter_category > span.filter-active', this.get("selector")).each(function(i, e) {
            temp_filters += $(e).data("category") + ',';            
        });
        if (temp_filters != '') {
            temp_filters = temp_filters.substring(0, temp_filters.length-1); 
        }

        this.set({"categories": temp_filters});
    },
    /*
    onClickAllFilter: function(event) {
        event.preventDefault();
        $('.filter_all', this.get("selector")).addClass('filter-active')
        this.updateAll();
        this.sendWhom();
        $(this.get("container")).trigger('datatable:refresh:filter');
    },
    */

    onClickApplyFilters: function(event) {
      event.preventDefault();
      $(this.get("container")).trigger('datatable:refresh:filter');
    },

    onChangeEntity: function(event) {
      var $el = $(event.currentTarget);
      var val = $el.find("option:selected").val();
      $.ajax({
        url: "/home/update_categories/",
        data: {account_id: val}
      })
    },

    onClickTypeFilter: function(event) {
        event.preventDefault();
        var $Target = $(event.target);
        $Target.toggleClass('filter-active');
        this.updateType();
        this.sendType();
        this.sendWhom();
        $(this.get("container")).trigger('datatable:refresh:filter');
    },
    updateType: function() {
        var temp_filters = '';
        $('.filter_type > span.filter-active', this.get("selector")).each(function(i, e) {
            temp_filters += $(e).parent().attr('data') + ',';            
        });
        if (temp_filters != '') {
            temp_filters = temp_filters.substring(0, temp_filters.length-1);
            $('.filter_all', this.get("selector")).removeClass('filter-active');
            this.set({"whom": false});
        }else{
            this.set({"whom": true});
            this.sendWhom();
        }
        this.set({"type": temp_filters});
    },
    sendType: function() {
        $(this.get("container")).trigger('datatable:set:type', [this.get("type")]);
    },
});
