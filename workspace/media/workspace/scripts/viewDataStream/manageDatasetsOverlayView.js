var ManageDatasetsOverlayView = Backbone.View.extend({
	
	el: "#id_addDataview",
	
	listDatasets: null,
	clientSideFilter: null,
	grid: null,
	paginator: null,

	events: {

	},

	initialize: function(options) {

		// Init Overlay
		this.$el.overlay({
			top: 'center',
			left: 'center',
			mask: {
				color: '#000',
				loadSpeed: 200,
				opacity: 0.5,
				zIndex: 99999
			}
		});

		// Init List
		this.initList();

		// Render
		this.render();

	},

	render: function(){
		this.$el.find("#dataset_grid").html(this.grid.render().$el);
		this.$el.find("#dataset_paginator").html(this.paginator.render().$el);
		this.$el.find('.backgrid-paginator ul').addClass("pager center");
		this.$el.find("#id_filter_dataSets").html( this.clientSideFilter.render().el );
		this.$el.data('overlay').load();
	},

	initList: function(){

		// Init the collection with django view list of datasets.        
		this.listDatasets = new ListDatasets({});

		var self = this;

		var clickableRow = Backgrid.Row.extend({
			events: {
				"click": "rowClicked"
			},
			rowClicked: function () {
				window.location = Configuration.createDataViewUrl + '?dataset_revision_id=' + this.model.get('id');
			}
		});

		var columns = [
			{
				name: "title",
				label: gettext('APP-GRID-CELL-TITLE'),
				cell: "string",
				sortable: true,
				editable: false
			},{
				name: "category",
				label: gettext('APP-GRID-CELL-CATEGORY'),
				cell: "string",
				sortable: true,
				editable: false
			}, {
				name: "type_nice",
				label: gettext('APP-GRID-CELL-TYPE'),
				cell: "text",
				sortable: false,
				editable: false
			}, {
				name: "author",
				label: gettext('APP-GRID-CELL-AUTHOR'),
				cell: "text",
				sortable: true,
				editable: false
			}, {
				name: "status_nice",
				label:  gettext('APP-GRID-CELL-STATUS'),
				cell: "text",
				sortable: false,
				editable: false
			}
		];

		this.grid = new Backgrid.Grid({
			row: clickableRow,
			columns: columns,
			collection: this.listDatasets,
      		emptyText: gettext('APP-NO-RESOURCES-FOUND-TEXT'),
		});

		this.paginator = new Backgrid.Extension.Paginator({
			collection: this.grid.collection,
		});

		this.listDatasets.fetch({
			reset: true
		});

		this.listDatasetView = new ListDatasetView({
			datasetCollection: this.listDatasets,
			grid: this.grid,
			paginator: this.paginator
		});

		this.clientSideFilter = new Backgrid.Extension.ServerSideFilter({
			collection: this.listDatasets,
			placeholder: gettext('APP-FILTER-TEXT'),
			fields: ['title'],
			wait: 150
		});

	},



});