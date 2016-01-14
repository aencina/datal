var DatasetModel = Backbone.Model.extend({
    idAttribute: 'dataset_revision_id',

    url: function () {
        var args = this.args.toJSON();
        var wargs = {};

        _.filter(args, function (arg) {
            return arg.editable;
        }).map(function (arg) {
            wargs[arg.name] = arg.value;
        });
        return ['/rest/datasets/',
                this.get('dataset_revision_id'),
                '/tables.json?',
                $.param({
                    limit: 100,
                    wargs: JSON.stringify(wargs)
                })
            ].join('');
    },

    initialize: function (attributes) {
        this.sources = new SourcesCollection(attributes.sources || []);
        this.tags = new TagsCollection(attributes.tags || []);
        this.args = new ArgumentsCollection();
        this.parseImplDetails(attributes.impl_details);
        this.listenTo(this.args, 'change:value', function (model, value, other) {
            this.fetch();
        }, this);
    },

    parse: function (response) {
        return {
                tables: response
            };
    },

    parseImplDetails: function (impl_details) {
        var $xml = $($.parseXML(impl_details)),
            $args = $xml.find('args > *');

        var args = _.map($args, function (arg) {
            var $node = $(arg);
            return {
                    name: arg.nodeName,
                    mappedName: arg.nodeName,
                    value: $node.text(),
                    editable: ($node.attr('editable') === 'True')
                };
        });
        this.args.reset(args);
    },

    getTables: function () {
        return _.range(0, this.get('tables').length);
    },

    getArgsAsParams: function (offset) {
        var args = this.args.toJSON(),
            offset = offset || 0;

        return _.filter(args, function (arg) {
                return arg.editable;
            }).map(function (arg, index) {
                return {
                    position: offset + index,
                    name: arg.mappedName,
                    description: '',
                    'default': arg.value
                };
            });
    }
})