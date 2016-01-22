var DataTableUtils = {
  rangeToExcel: function (range) {
    return [this.coordsToExcelCell(range.from), ':',
          this.coordsToExcelCell(range.to)].join('');
  },

  excelToRange: function (excelRange) {
    var parts = excelRange.split(':');

    if (parts.length !== 2) {
      //throw 'InvalidRange';
      return;
    }

    var from = this.excelCellToCoords(parts[0]);
    var to = this.excelCellToCoords(parts[1]);

    return {from: from, to: to};
  },

  excelCellToCoords: function (cellStr) {
    var digits = cellStr.replace(/\D/g,'');
    var chars = cellStr.replace(/\d+/g, '');
    var row = (digits === '')? -1 : parseInt(digits) - 1;
    var col = this.excelColToInt(chars) - 1;

    if (isNaN(row)) throw 'InvalidRange';

    return {col: col, row: row};
  },

  coordsToExcelCell: function (coords) {
    return [
          (coords.col !== -1) ? this.intToExcelCol(coords.col + 1) : '', 
          (coords.row !== -1) ? coords.row + 1 : ''
        ].join('');
  },

  intToExcelCol: function (number) {
    var colName = '',
    dividend = Math.floor(Math.abs(number)),
    rest;

    while (dividend > 0) {
      rest = (dividend - 1) % 26;
      colName = String.fromCharCode(65 + rest) + colName;
      dividend = parseInt((dividend - rest)/26);
    }
    return colName;
  },

  excelColToInt: function (colName) {
    var digits = colName.toUpperCase().split(''),
      number = 0;

    for (var i = 0; i < digits.length; i++) {
      number += (digits[i].charCodeAt(0) - 64)*Math.pow(26, digits.length - i - 1);
    }

    return number;    
  },

  toServerExcelRange: function(excelRange){
    if (_.isUndefined(excelRange) || excelRange === '') return '';
    var range = DataTableUtils.excelToRange(excelRange);

    if (range.from.row === -1 && range.to.row === -1) {
      excelRange = _.map(_.range(range.from.col, range.to.col + 1), function (col) {
        return 'Column:' + DataTableUtils.intToExcelCol(col + 1);
      }).join(',');
    }

    return excelRange;
  },

  parseEngineExcelRange: function (serverRange) {
    var self = this,
      col,
      accum;

    if (_.isUndefined(serverRange)) {
        return serverRange;
    };

    if (serverRange.indexOf('Column:') !== -1) {
      // Computes column numbers
      cols = serverRange.split(',').map(function (item) {
          return self.excelColToInt(item.replace('Column:', ''));
      });

      // Accumulates column numbers into ranges of consecutive columns
      accum = _.reduce(cols, function(memo, item) {
        if (memo.length !== 0 && memo[memo.length-1][1] + 1 === item) {
          memo[memo.length-1][1] = item;
        } else {
          memo.push([item,item]);
        }
        return memo;
      }, []);

      // Maps array of ranges into excel formated range
      serverRange = _.map(accum, function (range) {
        return DataTableUtils.intToExcelCol(range[0]) + ':' + DataTableUtils.intToExcelCol(range[1]);
      }).join(',');

    }
    return serverRange;
  },

};
