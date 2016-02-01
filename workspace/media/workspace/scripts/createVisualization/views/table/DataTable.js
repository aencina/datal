function HandsontableClassRendererPatch(TD, cellProperties) {
  if (cellProperties.classArray) {
    TD.className = '';
    for (var i = 0; i < cellProperties.classArray.length; i++) {
      TD.classList.add('hot-sel-' + cellProperties.classArray[i]);
    }
  }
}

Handsontable.renderers.registerRenderer('selectedTextRenderer', function () {
  HandsontableClassRendererPatch(arguments[1], arguments[6]);
  return Handsontable.renderers.TextRenderer.apply(this, arguments);
});

Handsontable.renderers.registerRenderer('selectedNumericRenderer', function () {
  HandsontableClassRendererPatch(arguments[1], arguments[6]);
  return Handsontable.renderers.NumericRenderer.apply(this, arguments);
});

Handsontable.renderers.registerRenderer('selectedDateRenderer', function () {
  HandsontableClassRendererPatch(arguments[1], arguments[6]);
  return Handsontable.renderers.DateRenderer.apply(this, arguments);
});

Handsontable.renderers.registerRenderer('selectedLinkRenderer', function () {
  HandsontableClassRendererPatch(arguments[1], arguments[6]);
  return Handsontable.renderers.NumericRenderer.apply(this, arguments);
});

var DataTableView = Backbone.View.extend({

  events: {
    'mousedown .ht_clone_top_left_corner.handsontable': 'onClickCorner'
  },

  typeToRenderer: {
    TEXT: 'selectedTextRenderer',
    LINK: 'selectedLinkRenderer',
    NUMBER: 'selectedNumericRenderer',
    DATE: 'selectedDateRenderer'
  },

  initialize: function (options) {
    var self = this,
      tableData = options.dataview,
      columns;

    this._enableFulllRowSelection   = options.enableFulllRowSelection || false;

    this._classId = undefined;
    this.utils = DataTableUtils;

    this._selectedCoordsCache = [];

    // Si el
    if (tableData.columns) {
      columns = _.map(tableData.columns, function (col) {
        return {
          renderer: self.typeToRenderer[col.fType]
        };
      });
    } else {
      columns = _.map(tableData.rows[0] || [], function (cell) {
        return {
          renderer: self.typeToRenderer['TEXT']
        };
      });
    }

    this.data = tableData.rows;
    if (columns.length === 0) {
      return;
    }

    this.table = new Handsontable(this.$('.table-view').get(0), {
      rowHeaders: true, colHeaders: true,
      readOnly: true,
      readOnlyCellClassName: 'htDimmed-datal', // the regular class paints text cells grey
      // renderAllRows: true, // Turns off virtual rendering
      allowInsertRow: false, allowInsertColumn: false,
      disableVisualSelection: ['current', 'area'],
      colWidths: 80,
      columns: columns,
      manualColumnResize: true,
      manualRowResize: true,
      stretchH: 'all',
      viewportRowRenderingOffset: 60
    });

    this.table.addHook('afterSelection', function (r1, c1, r2, c2) {
      var selection = self.parseSelection(r1, c1, r2, c2)
      self.paintCoords(selection)
    });
    // Selects a range
    this.table.addHook('afterSelectionEnd', function (r1, c1, r2, c2) {
      var selection = self.parseSelection(r1, c1, r2, c2);
      self.cacheSelection(selection);
      self.trigger('afterSelection', {});
    });
    
    this.table.addHook('afterOnCellMouseOver', function (event, coords, TD) {
      self._fullTableMode = false;
      self._fullColumnMode = (coords.row === -1 && coords.col !== -1);
      self._fullRowMode = (coords.col === -1 && coords.row !== -1);
      self._fullTableMode = (coords.col === -1 && coords.row === -1);
    });

    
    this.listenTo(this.collection, 'add', this.onAddSelected, this);
    this.listenTo(this.collection, 'remove', this.onRmSelected, this);
    this.listenTo(this.collection, 'reset', this.onReset, this);
    this.listenTo(this.collection, 'change', this.onChageSelected, this);

    this.setTableHeight();
  },

  paintCoords: function(coords) {
    if (this._classId) {
      var cells = this.coordsToCells(coords);
      this._addCellsMeta(cells, this._classId);
      this.table.render();
    }
  },

  setClassId: function(classId) {
    this._classId = classId;
  },

  parseSelection: function (r1, c1, r2, c2) {
      var selection;
      if (this._fullRowMode) {
        if (this._enableFulllRowSelection) {
          selection ={
            from: {row: r1, col: -1},
            to: {row: r2, col: -1}
          };
        } else {
          // We are changing the selection behavior in the case of full rows because the engine
          // does not currently support them (i.e. 6:6). The following is how one would re-enable
          // full row selection in the same way as is done for columns.
          selection = {
            from: {row: r1, col: c1},
            to: {row: r2, col: c2}
          };
        }
      } else if (this._fullColumnMode) {
        selection = {
          from: {row: -1, col: c1},
          to: {row: -1, col: c2}
        };
      } else {
        selection ={
          from: {row: r1, col: c1},
          to: {row: r2, col: c2}
        };
      }
      return selection;
  },

  render: function () {
    var self = this;
    if (_.isUndefined(this.table)) {
      return;
    }
    this.table.loadData(this.data);
    _.each(this.collection.models, function (model) {
      self.onAddSelected(model, false);
    });

    this.table.render();
  },

  setTableHeight: function(){

    $(window).resize(function(){

      var table = $('.table-view'),
          windowHeight = $(window).height();

      if( table.length > 0){

        var tableHeight =
          windowHeight
        - parseFloat( $('.global-navigation').height() )
        - parseFloat( $('.context-menu').height() )
        - parseFloat( table.parent().css('padding-top').split('px')[0] )
        - 30 // As margin bottom
        ;

        table.css('height', tableHeight+'px');

      }

    }).resize();
      
  },

  cacheSelection: function (coords) {
    if (coords) {
      this._selectedCoordsCache.push(coords);
    } else {
      this._selectedCoordsCache = []
    }
  },

  onClickCorner: function (e) {
    this.cacheSelection({
      from: {row: -1, col: -1},
      to: {row: -1, col: -1}
    });
    this._fullTableMode = true;
    this.trigger('afterSelection');
  },

  coordsToCells: function (coords) {
    var cells = [],
      rows = _.range(coords.from.row, coords.to.row + 1),
      cols = _.range(coords.from.col, coords.to.col + 1);

    if (coords.from.row === -1) {
      rows = _.range(0, this.table.countRows());
    }
    if (coords.from.col === -1) {
      cols = _.range(0, this.table.countCols());
    }

    _.each(rows, function (r) {
      _.each(cols, function (c) {
        cells.push({row: r, col: c});
      });
    });
    return cells;
  },

  _addCellsMeta: function (cells, selId) {
    var ids;
    for (var i = 0; i < cells.length; i++) {
      ids = this.table.getCellMeta(cells[i].row, cells[i].col).classArray || [];
      at = ids.indexOf(selId)
      if (at === -1) {
        ids.push(selId);
        this.table.setCellMeta(cells[i].row, cells[i].col, 'classArray', ids);
      }
    };
  },

  _rmCellsMeta: function (cells, selId) {
    var ids;
    for (var i = 0; i < cells.length; i++) {
      ids = this.table.getCellMeta(cells[i].row, cells[i].col).classArray || [];
      ids.splice(ids.indexOf(selId), 1);
      this.table.setCellMeta(cells[i].row, cells[i].col, 'classArray', ids);
    };
  },

  _rmAllCellsMeta: function (selId) {
    var ids,
      rows = this.table.countRows(),
      cols = this.table.countCols(),
      cells = this.coordsToCells({from:{row:0, col:0}, to:{row: rows-1, col: cols-1}}),
      at;

    for (var i = 0; i < cells.length; i++) {
      ids = this.table.getCellMeta(cells[i].row, cells[i].col).classArray || [];
      at = ids.indexOf(selId);
      if (at === -1) continue;
      ids.splice(at, 1);
      this.table.setCellMeta(cells[i].row, cells[i].col, 'classArray', ids);
    };
  },

  _resetMeta: function () {
    var rows = this.table.countRows(),
      cols = this.table.countCols(),
      cells = this.coordsToCells({from:{row:0, col:0}, to:{row: rows-1, col: cols-1}});

    for (var i = 0; i < cells.length; i++) {
      this.table.setCellMeta(cells[i].row, cells[i].col, 'classArray', []);
    };
  },

  getSelection: function () {
    var mode;
    var self = this;

    if (this._fullTableMode) {
      mode = 'table';
    } else if (this._fullColumnMode) {
      mode = 'col';
    } else if (this._fullRowMode) {
      mode = 'row';
    } else {
      mode = 'cell';
    }

    return {
      excelRange:_.compact(_.map(this._selectedCoordsCache, function(ele) { return self.utils.rangeToExcel(ele) })),
      mode: mode
    };
    
  },

  onAddSelected: function (model, render) {
    var range = model.getRange();
    if (!range) return;
    var self = this;
    var cells = _.flatten(_.compact(_.map(range, function(ele) { return self.coordsToCells(ele);})))
    this._addCellsMeta(cells, model.get('classname'));
    if (!_.isUndefined(render) && render) {
      this.table.render();
    }
  },

  onRmSelected: function (model) {
    var range = model.getRange();
    if (!range) return;
    var self = this;
    var cells = _.flatten(_.compact(_.map(range, function(ele) { return self.coordsToCells(ele);})))
    this._rmCellsMeta(cells, model.get('classname'));
    this.table.render();
  },

  onChageSelected: function (model) {
    var id = model.get('classname');
    var self = this;
    var previousRange = model.getPreviousRange(),
      range = model.getRange(),
      previousCells = [],
      cells = [];

    if (previousRange === undefined) {
      // this._rmAllCellsMeta(id);
    } else {
      previousCells = _.flatten(_.compact(_.map(previousRange, function(ele) { return self.coordsToCells(ele);})))
    }
    this._rmCellsMeta(previousCells, id);

    if (!model.isValid()) {
      this._rmAllCellsMeta(id);
    }

    if (range !== undefined) {
      cells = _.flatten(_.compact(_.map(model.getRange(), function(ele) { return self.coordsToCells(ele);})))
    }
    this._addCellsMeta(cells, id);

    this.table.render();
  },

  onReset: function (what) {
    this._resetMeta();
    this.table.render();
  },

  selectRange: function (excelRange) {
    var range = this.utils.excelToRange(excelRange),
      from = range.from,
      to = range.to;

    this.table.selectCell(from.row, from.col, to.row, to.col);
  }

});
