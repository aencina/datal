var DataTableSelectionModel = Backbone.Model.extend({
    validate: function (attrs, options) {
        var excelRanges = attrs.excelRange,
            r = /^(([a-zA-Z]*)?(\d*){1}:([a-zA-Z]*)?(\d*)?){1}$/,
            validRange = true;

        if (excelRanges) {
            for (i = 0; i < excelRanges.length; i++) { 
                excelRange = excelRanges[i];
                if (excelRange === undefined) {
                    return;
                } else {
                    validRange = r.test(excelRange);
                    validRange = validRange && this.validateMaxCol();
                    validRange = validRange && this.validateMaxRow();
                    if (!validRange) {
                        return 'invalid-range';
                    }
                }
            }
        }
    },

    hasRange: function () {
        return this.has('excelRange') && this.get('excelRange') !== '';
    },

    getRange: function () {
        var excelRange = this.get('excelRange');
        if (_.isUndefined(excelRange)) {
            return undefined;
        } else {
            return _.compact(_.map(this.get('excelRange'), function(ele) {return DataTableUtils.excelToRange(ele);}));
        }
    },

    validateMaxCol: function () {
        var ranges = this.getRange(),
            max = this.collection.maxCols;

        if (!_.isUndefined(ranges)) {
            return _.every(ranges, function(range) {return (range.from.col < max && range.to.col < max) })
        }
    },

    validateMaxRow: function () {
        var ranges = this.getRange(),
            max = this.collection.maxRows;

        if (!_.isUndefined(ranges)) {
            return _.every(ranges, function(range) {return (range.from.row < max && range.to.row < max) })
        }
    },

    getPreviousRange: function () {
        var prevExcelRange = this.previous('excelRange'),
            result;
        if (prevExcelRange !== undefined && prevExcelRange !== '') {
            try {
                result = _.compact(_.map(prevExcelRange, function(ele) {return DataTableUtils.excelToRange(ele);}));
            } catch (exception) {
                console.error(exception);
            }
        }
        return result;
    }
});
