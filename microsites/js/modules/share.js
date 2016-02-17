/*** SHARE ****/

var ShareBoxes = Backbone.Model.extend({

    defaults: {
        shareBoxes: []
    }

    , initialize: function(){
    }

    , add: function(pShareBox) {
        this.attributes.shareBoxes.push(pShareBox);
    }

    , display: function() {
        var att = this.attributes;
        for (i in att.shareBoxes) {
            att.shareBoxes[i].display();
        }
    }

    , redisplay: function(pShortUrl, pLongUrl) {
        var att = this.attributes;
        for (var i = 0; i < att.shareBoxes.length; i++) {
            if (att.shareBoxes[i] != undefined) {
                att.shareBoxes[i].redisplay(pShortUrl, pLongUrl);
            }
        }
    }
});

var ShareBox = Backbone.Model.extend({

    defaults: {
        $Container: null
        , shortUrl: null
        , longUrl: null
    }

    , initialize: function(){
    }

    , display: function() {
    }

    , redisplay: function(pShortUrl, pLongUrl) {
        var att = this.attributes;
        att.shortUrl = pShortUrl;
        att.longUrl = pLongUrl;
        this.display();
    }
});

var InputShareBox = ShareBox.extend({

    initialize: function(){
        var att = this.attributes;
        ShareBox.prototype.initialize.call(this);
        _.defaults(att, ShareBox.prototype.defaults);
        att.$Container.click(function(){ $(this).select(); });
        this.display();
    }

    , display: function() {
        var att = this.attributes;
        att.$Container.val(att.shortUrl);
    }

});

var TwitterShareBox = ShareBox.extend({

    defaults: {
        src: 'http://platform.twitter.com/widgets/tweet_button.html?'
        , title: ''
        , text: gettext( "SHARE-TWITTER-CHECKDS" ) + ' "{title}"'
        , count: 'vertical'
        , options: { 'count'     : 'vertical'
                     , 'lang'    : 'en'
                     , 'text'    : ''
                     , 'url'     : ''
                     , 'via'     : Configuration.APPLICATION_DETAILS.name
                     , 'related' : Configuration.APPLICATION_DETAILS.name
                     , 'counturl': ''
          }
    }

    , initialize: function(){
        var att = this.attributes;
        ShareBox.prototype.initialize.call(this);
        _.defaults(att, ShareBox.prototype.defaults);
        att.options.count = att.count;
        att.options.text = att.text.replace(/{title}/, att.title)
        this.display();
    }

    , display: function() {
        var att = this.attributes;
        att.$Container.attr('src', this.computeSrc());
    }

    , computeSrc: function() {
        var att = this.attributes;
        att.options.url = att.shortUrl;
        att.options.counturl = att.longUrl;
        var lSrc = att.src + $.param(att.options);
        return lSrc.replace(/\+/g, '%20');
    }

});

var FacebookShareBox = ShareBox.extend({

    defaults: {
        src: 'http://www.facebook.com/plugins/like.php?'
        , layout: 'box_count'
        , width: 55
        , height: 90
        , options: { 'app_id' :'239770912731187'
                     , 'href': ''
                     , 'send': 'false'
                     , 'layout': 'box_count'
                     , 'width' : 55
                     , 'show_faces': 'false'
                     , 'action': 'like'
                     , 'colorscheme': 'light'
                     , 'font': 'lucida grande'
                     , 'height': 90
                     , 'locale': 'en_US'
                     }
    }

    , initialize: function(){
        var att = this.attributes;
        ShareBox.prototype.initialize.call(this);
        _.defaults(att, ShareBox.prototype.defaults);
        att.options.layout = att.layout;
        att.options.width = att.width;
        att.options.height = att.height;
        this.display();
    }

    , display: function() {
        var att = this.attributes;
        att.$Container.attr('src', this.computeSrc());
    }

    , computeSrc: function() {
        var att = this.attributes;
        att.options.href = att.shortUrl;
        var lSrc = att.src + $.param(att.options);
        return lSrc;
    }

});

var GooglePlusShareBox = ShareBox.extend({

    defaults: {
        size: 'tall'
    }

    , initialize: function(){
        var att = this.attributes;
        ShareBox.prototype.initialize.call(this);
        _.defaults(att, ShareBox.prototype.defaults);
        this.display();
    }

    , display: function() {
        var att = this.attributes;
        try {
            if (gapi) {
                var result = gapi.plusone.render(att.$Container.get(0), {"size": att.size, "count": "true", "href": att.shortUrl});
            }
        } catch(e){}
    }
});

var LinkedinShareBox = ShareBox.extend({

    defaults: {
        src: ''
        , 'data_counter' : 'top'
        , options: { 
            'url' :''
            , 'data_counter' : 'top'
        }
    }

    , initialize: function(){
        var att = this.attributes;
        ShareBox.prototype.initialize.call(this);
        _.defaults(att, ShareBox.prototype.defaults);
        att.options.data_counter = att.data_counter;
        att.src = '/share/linkedin?';
        this.display();
    }

    , display: function() {
        var att = this.attributes;
        att.$Container.attr('src', this.computeSrc());
    }

    , computeSrc: function() {
        var att = this.attributes;
        att.options.url = att.shortUrl;
        var lSrc = att.src + $.param(att.options);
        return lSrc;
    }

});