var ManageDatastreamsOverlayView = Backbone.View.extend({

	el: "#id_addVisualization",

	listDatastreams: null,
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
		this.$el.find("#visualization_grid").html(this.grid.render().$el);
		this.$el.find("#visualization_paginator").html(this.paginator.render().$el);
		this.$el.find('.backgrid-paginator ul').addClass("pager center");
		this.$el.find("#id_filter_visualization").html( this.clientSideFilter.render().el );
		
		var self = this,
			myTimeer = setInterval(function(){
			self.$el.data('overlay').load();
			clearInterval(myTimeer);
		},200);

	},

	initList: function(){

		// Init the collection with django view list of visualizations.
		this.listDatastreams = new ListDatastreams({});

		var self = this;

		var clickableRow = Backgrid.Row.extend({
			events: {
				"click": "rowClicked"
			},
			rowClicked: function () {
				window.location = Configuration.createVisualizationUrl + '?datastream_revision_id=' + this.model.get('id');
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
			collection: this.listDatastreams,
      emptyText: gettext('APP-NO-RESOURCES-FOUND-TEXT'),
		});

		this.paginator = new Backgrid.Extension.Paginator({
			collection: this.grid.collection,
		});

		this.listDatastreams.fetch({
			reset: true
		});

		this.listDatastreamView = new ListDatastreamView({
			visualizationCollection: this.listDatastreams,
			grid: this.grid,
			paginator: this.paginator
		});

		this.clientSideFilter = new Backgrid.Extension.ServerSideFilter({
			collection: this.listDatastreams,
			placeholder: gettext('APP-FILTER-TEXT'),
			fields: ['title'],
			wait: 150
		});

	},



});