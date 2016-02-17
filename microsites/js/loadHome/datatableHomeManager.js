var DatatableHomeManager = DatatableManager.extend({
    initialize: function(container, selector, url, delete_revision_url, delete_url, submit_url, modal_container) {
        $(this.get("container")).bind('datatable:set:search', _.bind(this.setSearch, this));
        $(this.get("container")).bind('datatable:set:categories', _.bind(this.setCategories, this));
        $(this.get("container")).bind('datatable:set:type', _.bind(this.setStatus, this));
        $(this.get("container")).bind('datatable:set:source_choice', _.bind(this.setSourceChoice, this));
        
        $(this.get("container")).bind('datatable:set:whom', _.bind(this.setWhom, this));
        $(this.get("container")).bind('datatable:set:page', _.bind(this.setPage, this));
        $(this.get("container")).bind('datatable:set:sort', _.bind(this.setSort, this));
        $(this.get("container")).bind('datatable:set:items_per_page', _.bind(this.setItemsPerPage, this));
        $(this.get("container")).bind('datatable:refresh:search', _.bind(this.refreshTableSearch, this));
        $(this.get("container")).bind('datatable:refresh:filter', _.bind(this.refreshTableFilter, this));
        $(this.get("container")).bind('datatable:refresh:pagination', _.bind(this.refreshTablePagination, this));
        $(this.get("container")).bind('datatable:refresh:sort', _.bind(this.refreshTableSort, this));
        $(this.get("container")).bind("datatable:refresh:items_per_page", _.bind(this.refreshTableItemsPerPage, this));
        $(this.get("container")).bind("datatable:refresh:create_dataset", _.bind(this.refreshTableCreateDataset, this));
        $(this.get("container")).bind("datatable:refresh:edit_dataset", _.bind(this.refreshTableEditDataset, this));
        
        $(this.get("container")).bind("datatable:set_checkboxes_state", _.bind(this.setCheckboxesState, this));

//        $(this.get("container")).bind("datatable:tablesorter", function() {
//          $table = $(this).find("table");
//          $table.stupidtable();
//          $table.bind('beforetablesort', function(e, data) {
//            // Get the clicked col
//            var col = $(this).find("th")[data.column];
//            if (col) {
//              // Remove all existing class and add the current direction as a class
//              $(col).removeClass().addClass(data.sortDir);
//            }
//          });
//        });
//        $(this.get("container")).trigger("datatable:tablesorter");
    },
    setSourceChoice: function(event, type) {
        this.set({source_choice_filters: type});
    },
    getRowTemplate: function(msg) {
    
        var className = '';

        if(msg.type == 'DT'){
            className = 'ic_Dset';
        }else if(msg.type == 'DS'){
            className = 'ic_Data';
        }else if(msg.type == 'db'){
            className = 'ic_Dashboard';
        }else if(msg.type == 'VZ'){
            className = 'ic_Chart';
        }

        var templ = "<tr id='id_<%= revision.id %>'>";
        
        templ += "<td class='viewInfo'>\
                <div class='" + className + "'></div><a href='<%= revision.permalink %>' target='_blank'><strong><%= revision.title %></strong> </a> <% if(revision.account_name){ %> <span class='sep'> | </span> <%= revision.account_name %> <% } %> <span class='sep'> | </span>  <%= revision.category %></td>";
           
        var date = new Date(msg.created_at);
        templ += "<td class='date' data-sort-value='" + date.getTime() + 
                    "'><span class='longDateFormat'>" + 
                    $.datepicker.formatDate( (Configuration.language == "en")?"MM d, yy":"d 'de' MM 'de' yy", date
				    , { monthNames: $.datepicker.regional[ (Configuration.language == "en")? "": Configuration.language ].monthNames }) 
				    + "</span></td>";
        templ +="</tr>";

        var tpl = _.template(templ); // , {variable: 'revision'});
        var html = tpl({revision: msg});
        return html;
        // return _.template(templ, {variable: 'revision'})(msg);
        // return _.template(templ, {revision: msg});
    },
    drawRow: function(msg) {
        $('table tbody', this.get("selector")).append(this.getRowTemplate(msg));
    },
    getFormParameters: function(data) {
        $(this.get("container")).trigger("filter:get:categories");
        $(this.get("container")).trigger("filter:get:type");
        $(this.get("container")).trigger("filter:get:source_choice");
        $(this.get("container")).trigger("filter:get:owner");
        $(this.get("container")).trigger("search:get");
        $(this.get("container")).trigger("pagination:get:page");
        $(this.get("container")).trigger("pagination:get:items_per_page");
        $(this.get("container")).trigger("header:sort:get");

        if (this.get("category_filters") != '') {
            data.category_filters = this.get("category_filters");
        }else{
            data.category_filters = '';
        }
        if (this.get("status_filters") != '') {
            data.type = this.get("status_filters");
        }else{
            data.type = '';
        }

        if (this.get("whom") == true) {
            data.all = true;
        }else{
            data.all = false;
        }
        
        if (this.get("search") != '') {
            data.search = this.get("search");
        }

        data.page = this.get("page");
        data.items_per_page = this.get("items_per_page");
        data.order = this.get("column.number");
        if (this.get("column.ascending") == true) {
            data.order_type = 'ascending';
        }
        else {
            data.order_type = 'descending';
        }

        // Get data directly from DOM
        var filters = [
          {attr: "entity_filters", element: "#id_filter_entity"},
          {attr: "type_filters", element: "#id_filter_type"},
          {attr: "category_filters", element: "#id_filter_category"}
        ];

        for (var i in filters) {
          var filter = filters[i];
          var val = $(this.get("container")).find(filter.element + " option:selected").val();
          if (val) {
            data[filter.attr] = val;
          }
        }

        return data;
    }
});
