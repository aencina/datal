var select_statement_template = ['<selectStatement>',
    '<Select>',
        '<% if (isFullTable) { %>',
            '<Column>*</Column>',
        '<% } else if (columns.length !== 0) { %>',
            '<% _.each(columns, function (number) { %>',
                '<Column>column<%= number %></Column>',
            '<% }); %>',
        '<% } else if (cells.length !== 0) { %>',
            '<% _.each(cells, function (number) { %>',
                '<Column>cell<%= number %></Column>',
            '<% }); %>',
        '<% } else { %>',
            '<Column>*</Column>',
        '<% } %>',
    '</Select>',
    '<From>',
        '<Table>table<%= tableId %></Table>',
    '</From>',
    '<Where>',
        '<% _.each(rows, function (number) { %>',
        '<Filter>',
            '<Operand1>rownum</Operand1>',
            '<LogicalOperator>00</LogicalOperator>',
            '<Operand2><%= number %></Operand2>',
        '</Filter>',
        '<% }); %>',
        '<% _.each(filters, function (filter, index) { %>',
        '<Filter>',
            '<Operand1>column<%= filter.column %></Operand1>',
            '<LogicalOperator><%= filter.operator %></LogicalOperator>',
            '<% if (filter.type === \'fixed\') {%>',
                '<Operand2><%= filter.default %></Operand2>',
            '<% } else {%>',
                '<Operand2>parameter<%= filter.position %></Operand2>',
            '<% } %>',
        '</Filter>',
        '<% }); %>',
    '</Where>',
'</selectStatement>',
].join('');

var data_source_template = ['<dataSource>',
    '<% if (args.length > 0) {%>',
    '<EndPointMappings>',
        '<% _.each(args, function (arg) { %>',
            '<Mapping>',
                '<key><%= arg.name%></key>',
                '<value>parameter<%= arg.position%></value>',
            '</Mapping>',
        '<% }); %>',
    '</EndPointMappings>',
    '<% } %>',
    '<DataStructure>',
        '<Field id="table<%= tableId %>">',
            '<Headers>',
                '<% _.each(headers, function (row) { %>',
                    '<Row>row<%= row %></Row>',
                '<% }); %>',
            '</Headers>',
            '<type/>',
            '<format>',
                '<languaje/>',
                '<country/>',
                '<style/>',
            '</format>',
            '<Table>',
                '<% _.each(columns, function (column) { %>',
                '<Field id="column<%= column.column %>">',
                    '<alias/>',
                    '<type><%= column.type %></type>',
                    '<format>',
                        '<Symbols>',
                            '<decimals><%= column.decimalSeparator %></decimals>',
                            '<thousands><%= column.thousandSeparator %></thousands>',
                        '</Symbols>',
                        '<language><%= column.inputLanguage %></language>',
                        '<country><%= column.inputCountry || column.inputLanguage %></country>',
                        '<% if (column.type === \'NUMBER\') { %>',
                            '<style/>',
                            '<pattern><%= (column.inputPattern === \'custom\')? column.inputCustomPattern: column.inputPattern %></pattern>',
                        '<% } else if (column.type === \'DATE\') { %>',
                            '<style><%= (column.inputPattern === \'custom\')? column.inputCustomPattern: column.inputPattern %></style>',
                            '<pattern/>',
                        '<% } %>',
                    '</format>',
                    '<% if (column.type !== \'TEXT\') { %>',
                        '<DisplayFormat>',
                            '<pattern><%= (column.outputPattern === \'custom\')? column.outputCustomPattern: column.outputPattern %></pattern>',
                            '<% if (column.type === \'NUMBER\') { %>',
                                '<locale><%= column.numberDisplayLocale %></locale>',
                            '<% } else if (column.type === \'DATE\') { %>',
                                '<locale><%= column.dateDisplayLocale %></locale>',
                            '<% } %>',
                        '</DisplayFormat>',
                    '<% } %>',
                '</Field>',
                '<% }); %>',
            '</Table>',
        '</Field>',
    '</DataStructure>',
'</dataSource>'].join('');

var DataviewModel = Backbone.Model.extend({

    select_statement_template: _.template(select_statement_template),
    data_source_template: _.template(data_source_template),

    idAttribute: 'dataview_revision_id',

    defaults:{
        title: undefined,
        description: undefined,
        category: undefined,
        notes: '',

        dataset_revision_id: undefined,

        tableId: 0,
        status: 0,

        // TODO: remove this hardcoded params and use the model's data
        rdf_template: '',
        bucket_name: '',
        user_id: 1647,
        limit: 50
    },

    initialize: function (attributes) {
        this.data = new Backbone.Model();
        this.selection = new DataTableSelectedCollection();

        this.filters = new FiltersCollection();
        this.formats = new ColumnsCollection();
        this.editMode = attributes.edit_mode
        this.datastream_revision_id = attributes.datastream_id;
    },

    url: '/rest/datastreams/sample.json/',

    attachDataset: function (attributes) {
        this.dataset = new DatasetModel(attributes);
        this.on('change:tableId', this.onChangeTableId, this);

        // Trigger initially to get the default table rows and cols
        this.listenTo(this.dataset, 'change:tables', function () {
            this.onChangeTableId(this.dataset, 0);
        }, this);

        // Dataview sources and Tags are initially cloned from those in the dataset.
        this.sources = this.dataset.sources.clone();
        this.tags = this.dataset.tags.clone();
    },

    fetch: function (options) {
        var self = this,
            params = this.dataset.pick([
                'end_point',
                'impl_type',
                'impl_details',
                'rdf_template',
                'bucket_name'
            ]);

        var filters = this.filters.toSampleFilters();
        _.extend(params, filters);

        // NOTE: here the datasource param does not contain an underscore, like it does in save
        params.datasource = this.getDataSource();

        params.select_statement = this.getSelectStatement();
        params.limit = 50;

        return $.ajax({
                type: "POST",
                url: this.url,
                data: params,
                dataType: 'json'
            }).then(function (response) {
                self.parse(response);
                return response;
            });
    },

    parse: function (response) {
        if (response.fType === 'TEXT') {
            response = {
                "fLength":1,
                "fType":"ARRAY",
                "fTimestamp":response.fTimestamp,
                "fArray":[{
                    "fStr":response.fStr,
                    "fType":"TEXT"
                }],
                "fRows":1,
                "fCols":1
            };
        }
        var columns = _.first(response.fArray, response.fCols);

        var rows = _.map(_.range(0, response.fRows), function (i) {
            var row = response.fArray.slice(i*response.fCols, (i+1)*response.fCols);
            return _.pluck(row, 'fStr');
        });

        var rowsRaw = _.map(_.range(0, response.fRows), function (i) {
            var row = response.fArray.slice(i*response.fCols, (i+1)*response.fCols);
            return row;
        }).filter(function (row) {
            // filtrar las filas que son headers
            return _.isUndefined(row[0].fHeader) || !row[0].fHeader;
        });

        var headers = _.filter(response.fArray, function (cell) {
            return !_.isUndefined(cell.fHeader) && cell.fHeader;
        });

        this.data.set('columns', columns);
        this.data.set('headers', headers);
        this.data.set('rowsRaw', rowsRaw);
        this.data.set('response', response);
        this.data.set('rows', rows);
    },

    validation: {
        title: [
            {
                required: true,
                msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
            },{
                maxLength: 80,
                msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 80 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
            }
        ],
        description: [
            {
                required: true,
                msg: gettext('VALIDATE-REQUIREDFIELD-TEXT')
            },{
                maxLength: 250,
                msg: gettext('VALIDATE-MAXLENGTH-TEXT-1') + ' 250 ' + gettext('VALIDATE-MAXLENGTH-TEXT-2')
            },{
                fn: function(value, attr, computedState){
                    if( $.trim(computedState.title) === $.trim(value) ) {
                        return gettext('APP-TITSUBDES-NOTEQUALS');
                    }
                }
            }
        ],
    },

    save: function () {
        var self = this,
            params = this.pick([
                'rdf_template',

                'title',
                'description',
                'category',
                'notes',
                'status',
            ]);

        var filterParameters = this.filters.toFormSet();

        var datasetArguments = this.dataset.getArgsAsParams(filterParameters.length);
        dataviewParameters = filterParameters.concat(datasetArguments);

        var parametersParams = this.toFormSet(dataviewParameters, 'parameters');

        var tags = this.tags.map(function (model) {
            return {name: model.get('tag__name')};
        });

        var sources = this.sources.map(function (model) {
            return {
                name: model.get('source__name'),
                url: model.get('source__url')
            };
        });

        var tagsParams = this.toFormSet(tags, 'tags');
        var sourcesParams = this.toFormSet(sources, 'sources');

        _.extend(params, parametersParams);
        _.extend(params, tagsParams);
        _.extend(params, sourcesParams);

        params.dataset_revision_id = this.dataset.get('dataset_revision_id');
        params.select_statement = this.getSelectStatement();
        params.data_source = this.getDataSource();

        if (this.editMode) {
            params.datastream_revision_id = this.datastream_revision_id
            return $.ajax({
                    type: 'POST',
                    url: '/dataviews/edit/' + this.datastream_revision_id + '/',
                    data: params,
                    dataType: 'json'
                });
        } else {
            return $.ajax({
                    type: 'POST',
                    url: '/dataviews/create/',
                    data: params,
                    dataType: 'json'
                });
        }
    },

    onChangeTableId: function (model, value) {
        var tables = this.dataset.get('tables'),
            rows;
        if (tables.length !== 0) {
            rows = tables[value];
            this.set('totalCols', _.isUndefined(rows[0])? 0: rows[0].length );
            this.set('totalRows', rows.length);
        }
    },

    toFormSet: function (list, prefix) {
        var result = {},
            total = list.length;

        _.each(list, function (item, index) {
            _.each(item, function (value, key) {
                result[prefix + '-' + index + '-' + key] = value;
            });
        });
        result[prefix + '-TOTAL_FORMS'] = total;
        result[prefix + '-INITIAL_FORMS'] = 0;
        return result;
    },
    addCategory: function(category_id, category_name) {
        this.set('category', category_id)
    },
    addTitle: function(title) {
        this.set('title', title)
    },
    addDescription: function(title) {
        this.set('description', title)
    },
    addNotes: function(notes) {
        this.set('notes', notes)
    },
    addSources: function(sources) {
        this.sources = new SourcesCollection(sources)
    },
    addTags: function(tags) {
        this.tags = new TagsCollection(tags)  
    },
    addSelectStatement: function(statement, params) {
        if (window.DOMParser) {
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(statement, "text/xml");
        }
        else { // Internet Explorer
            xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
            xmlDoc.async = false;
            xmlDoc.loadXML(statement);
        }
        var filters = xmlDoc.getElementsByTagName("Filter");
        var rowFiltersCount = 0
        if (filters.length > 0 ) {
            for (var i = 0; i < filters.length; i++) {
                filter = filters[i]
                operand = filter.getElementsByTagName('Operand1')[0].textContent
                if (operand == 'rownum') {
                    row_index = parseInt(filter.getElementsByTagName("Operand2")[0].textContent) + 1
                    this.selection.add({
                        classname: 'row',
                        mode: 'row',
                        excelRange: row_index + ":" + row_index
                    })
                    rowFiltersCount += 1
                } else {
                    column_number = operand.replace('column', '')
                    filterModel = new FilterModel()
                    filterModel.set('column',column_number)
                    filterModel.set('excelCol', DataTableUtils.intToExcelCol(parseInt(column_number) + 1))
                    filterModel.set('operator', filter.getElementsByTagName("LogicalOperator")[0].textContent)

                    operand2 = filter.getElementsByTagName("Operand2")[0].textContent
                    if (operand2.indexOf('parameter') >= 0) {
                        position = parseInt(operand2.replace('parameter', ''))
                        for (var j = 0; j < params.length; j++) {
                            if ( params[j].position == position ) {
                                filterModel.set('default', params[j].default)
                                filterModel.set('name', params[j].name)
                                filterModel.set('description', params[j].description)
                                filterModel.set('type', 'parameter')
                                filterModel.set('position', position)
                                break
                            }
                        }
                    } else {
                        filterModel.set('default', operand2)
                        filterModel.set('type', 'fixed')
                    }
                    this.filters.add(filterModel)
                }
            }
        } 
        var columns = xmlDoc.getElementsByTagName("Column");
        if (columns.length == 1 && columns[0].textContent == "*" && rowFiltersCount == 0) {
            this.selection.add({
                classname: 'table',
                mode: 'table',
                excelRange:  ":"
            })
        } else if (columns.length > 0 && columns[0].textContent != "*") {
            if ( columns[0].textContent.indexOf('column') >= 0 ) {
                for (var i = 0; i < columns.length; i++) {
                    columna = columns[i]
                    col_index = parseInt(columna.textContent.replace("column", ""))
                    col_letter = DataTableUtils.intToExcelCol(col_index+1)
                    this.selection.add({
                        classname: 'col',
                        mode: 'col',
                        excelRange: col_letter + ":" + col_letter
                    })
                }
            } else if (columns[0].textContent.indexOf('cell') >= 0) {
                init_number = parseInt(columns[0].textContent.replace("cell", ""))
                last_number = parseInt(columns[columns.length-1].textContent.replace("cell", ""))
                totals = this.get('totalCols')
                this.selection.add({
                    classname: 'cell',
                    mode: 'cell',
                    excelRange: DataTableUtils.rangeToExcel({
                        from: {
                            row:parseInt(init_number/totals),
                            col: init_number % totals
                        },
                        to: {
                            row:parseInt(last_number/totals),
                            col:last_number % totals
                        }
                    })
                })
            }
        }
    },
    getSelectStatement: function () {
        var tableId = this.get('tableId'),
            isFullTable = this.selection.hasItemsByMode('table'),
            columnModels = this.selection.getItemsByMode('col'),
            columns = _.uniq(_.reduce(columnModels, function(memo, model, key, list){
                var range = model.getRange()
                Array.prototype.push.apply(memo, _.range(range.from.col, range.to.col+1));
                return memo 
            }, [])),
            totalCols = this.get('totalCols'),
            cellModels = this.selection.getItemsByMode('cell'),
            rowModels = this.selection.getItemsByMode('row'),
            rows = _.uniq(_.reduce(rowModels, function(memo, model, key, list){
                var range = model.getRange()
                Array.prototype.push.apply(memo, _.range(range.from.row, range.to.row+1));
                return memo 
            }, []));

            cells = []
            for (var x = 0; x < cellModels.length; x++) {
                var range = cellModels[x].getRange();
                for (var z = 0; z <= range.to.row - range.from.row; z++) {
                    var row = z + range.from.row
                    for (var y = 0; y <= range.to.col - range.from.col; y++) {
                        var col = y + range.from.col
                        cells.push( row * totalCols + col )
                    }
                }

            }

        return this.select_statement_template({
            isFullTable: isFullTable,
            tableId: tableId,
            columns: columns,
            cells: cells,
            rows: rows,
            filters: this.filters.toJSON()
        });
    },

    getColumns: function () {
        var self = this;
        var formats = this.formats.clone();
        var availableColumns = _.range(0, this.get('totalCols'));

        _(availableColumns).each(function (columnId) {
            if (_.isUndefined(formats.get(columnId))) {
                formats.add({column: String(columnId)});
            }
        });
        return formats.map(function (model) {
            var obj = model.toJSON();
            if (!_.isUndefined(obj.inputLocale)) {
                var parts = obj.inputLocale.split('_');
                obj.inputLanguage = parts[0];
                obj.inputCountry = (parts.length > 1)? parts[1]: undefined;
            }
            return obj;
        });
    },
    addDataSource: function(source) {
        var validFormats = [
          "#,###",
          "$ #,###",
          "#,###.##",
          "$ #,###.##",
        ]
         if (window.DOMParser) {
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(source, "text/xml");
        }
        else { // Internet Explorer
            xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
            xmlDoc.async = false;
            xmlDoc.loadXML(source);
        }
        var headers = xmlDoc.getElementsByTagName("Headers")[0].getElementsByTagName("Row");
        if (headers.length > 0 ) {
            for (var i = 0; i < headers.length; i++) {
                header = headers[i]
                row_index = parseInt(header.textContent.replace('row', '')) + 1
                this.selection.add({
                    classname: 'header',
                    mode: 'header',
                    excelRange: row_index + ":" + row_index
                })
            }
        } 
        var columns = xmlDoc.getElementsByTagName("Table")[0].getElementsByTagName("Field");
        if (columns.length > 0) {
            for (var i = 0; i < columns.length; i++) {
                column = columns[i]
                obj = {}
                obj.column = column.getAttribute('id').replace('column', '')
                obj.type = column.getElementsByTagName('type')[0].textContent
                if (obj.type != 'TEXT') {
                    obj.decimalSeparator = column.getElementsByTagName('decimals')[0].textContent
                    obj.thousandSeparator = column.getElementsByTagName('thousands')[0].textContent
                    if (!obj.decimalSeparator || !obj.thousandSeparator) {
                        delete obj.decimalSeparator
                        delete obj.thousandSeparator
                        obj.separatorType = 'locale'
                    } else {
                        obj.separatorType = 'symbol'
                    }
                    obj.inputLanguage = column.getElementsByTagName('language')[0].textContent
                    obj.inputCountry = column.getElementsByTagName('country')[0].textContent
                    if (obj.inputLanguage == obj.inputCountry) {
                        obj.inputLocale = obj.inputLanguage
                    } else {
                        obj.inputLocale = obj.inputLanguage + '_' + obj.inputCountry
                    }
                    if (obj.type == 'NUMBER') {
                        obj.inputPattern = column.getElementsByTagName('format')[0].getElementsByTagName('pattern')[0].textContent
                    } else if (obj.type == 'DATE') {
                        obj.inputPattern = column.getElementsByTagName('format')[0].getElementsByTagName('style')[0].textContent
                    }
                    if (validFormats.indexOf(obj.inputPattern) < 0) {
                        obj.inputCustomPattern = obj.inputPattern
                        obj.inputPattern = 'custom'
                    }
                    obj.outputPattern = column.getElementsByTagName('DisplayFormat')[0].getElementsByTagName('pattern')[0].textContent
                    if (validFormats.indexOf(obj.outputPattern) < 0) {
                        obj.outputCustomPattern = obj.outputPattern
                        obj.outputPattern = 'custom'
                    }

                    if (obj.type == 'NUMBER') {
                        obj.numberDisplayLocale = column.getElementsByTagName('DisplayFormat')[0].getElementsByTagName('locale')[0].textContent
                    } else if (obj.type == 'DATE') {
                        obj.dateDisplayLocale = column.getElementsByTagName('DisplayFormat')[0].getElementsByTagName('locale')[0].textContent
                    }
                    obj.excelCol = DataTableUtils.intToExcelCol(obj.column)
                    this.formats.add(obj)
                }

            }
        }
    },
    getDataSource: function () {
        var tableId = this.get('tableId'),
            filterCount = this.filters.length,
            columns = this.getColumns(),
            headerModels = this.selection.getItemsByMode('header'),
            headers = _.map(headerModels, function (model) {
                return model.getRange().from.row;
            }),
            argsList = this.dataset.args.toJSON(),
            args;

        args = _.filter(argsList, function (arg) {
            return arg.editable;
        }).map(function (arg, index) {
            arg.position = filterCount + index;
            return arg;
        });

        return this.data_source_template({
            args: args,
            tableId: tableId,
            headers: headers,
            columns: columns
        });
    }
});
