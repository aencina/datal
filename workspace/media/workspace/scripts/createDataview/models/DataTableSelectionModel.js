var DataTableSelectionModel = Backbone.Model.extend({
    validate: function (attrs, options) {
        var excelRange = attrs.excelRange,
            r = /^(([a-zA-Z]*)?(\d*)?:([a-zA-Z]*)?(\d*)?)?$/,
            validRange = true;

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
    },

    hasRange: function () {
        return this.has('excelRange') && this.get('excelRange') !== '';
    },

    getRange: function () {
        var excelRange = this.get('excelRange');
        if (_.isUndefined(excelRange)) {
            return undefined;
        } else {
            return DataTableUtils.excelToRange(this.get('excelRange'));
        }
    },

    validateMaxCol: function () {
        var range = this.getRange(),
            max = this.collection.maxCols;

        if (!_.isUndefined(range)) {
            return (range.from.col < max && range.to.col < max);
        }
    },

    validateMaxRow: function () {
        var range = this.getRange(),
            max = this.collection.maxRows;

        if (!_.isUndefined(range)) {
            return (range.from.row < max && range.to.row < max);
        }
    },

    getPreviousRange: function () {
        var prevExcelRange = this.previous('excelRange'),
            result;
        if (prevExcelRange !== undefined && prevExcelRange !== '') {
            try {
                result = DataTableUtils.excelToRange(prevExcelRange);
            } catch (exception) {
                console.error(exception);
            }
        }
        return result;
    }
});
