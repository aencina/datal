var dataStreamHitsView = Backbone.View.extend({

  el: '#id_datastreamHits',  
    
  events:{

  },
    
  initialize: function() {

    this.listenTo(this.model, "change:data", this.render); 
      
    this.invoke();    

  },
  
  render: function() { 

    var properties = {
      title: '',
      width: 270, height: 100 ,
      hAxis: {title: ''},
      vAxis: {title: '', format:'#'},
      legend : 'none'
    };

    var chart = new google.visualization.LineChart( this.$el[0] );
    chart.draw(this.model.attributes.data, properties);

    return this;

  },
    
  invoke: function(){

    var dataStream = this.options.dataStream.attributes;
      
    var url  = '/rest/datastreams/'+ dataStream.revision_id + '/hits.json';
            
    var ajax = $.ajax({ 
      url: url,
      dataType: 'json',
      success: _.bind(this.onInvokeSuccess, this), 
      error: _.bind(this.onInvokeError, this)
    });

  },
  
  onInvokeSuccess: function(response){

    var data    = {};
    data.rows   = [];
    data.cols   = [];
    var chartData;

    // Set headers for line chart
    for (var i = 0; i <= 1; i++) {
        var col = {};
        col.id = i + '_' + '';
        col.label = '';
        if(i == 1){
            var header = '';
            col.id = i + '_' + header;
            col.label = header;
        }
        if (i == 0) {
            col.type = 'string';
        }
        else {
            col.type = 'number';
        }
        data.cols.push(col);
    }
    
    // Set data for line chart
    for (var i = 1; i < response.chart.length; i++) {
        chartData = { c: [] };
        var header;
        header = { v: '' };
        chartData.c.push(header);
        var stat = response.chart[i][1];
        var value = { v: stat };
        chartData.c.push(value);
        data.rows.push(chartData);
    }

    this.model.set('data', new google.visualization.DataTable(data) );

  },
  
  onInvokeError: function(){
      
  }

});
