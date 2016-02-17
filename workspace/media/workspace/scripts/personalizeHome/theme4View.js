var theme4View = Backbone.Epoxy.View.extend({

	el: '#id_themeForm',
	template: null,
	files: [],

	events:{
		"click #id_btnRemoveCover" : "removeCover",
	},

	initialize: function(options){
		this.currentView = options.currentView;
		this.currentModel = options.currentModel;

		this.currentView.helpAndTips('show');
		this.template = _.template( $("#id_theme4Template").html() );		
		this.initSliderSection();
		this.initLinkSection();
		this.render();
		this.initInput();
	},

	render: function(){
		var self = this;
		Backbone.Validation.bind(this, {
            valid: function (view, attr, selector) {
                self.setIndividualError(view.$('[name=id_theme4' + attr + ']'), attr, '');
            },
            invalid: function (view, attr, error, selector) {
                self.setIndividualError(view.$('[name=id_theme4' + attr + ']'), attr, error);
            }
        });
	        
		this.$el.html(this.template(this.model.attributes));
		return this;
	},

	setIndividualError: function(element, name, error){

        // If not valid
        if( error != ''){
            element.addClass('has-error');
            element.after('<p class="has-error">'+error+'</p>');

        // If valid
        }else{
            element.removeClass('has-error');
            element.next('p').remove();
        }

    },
	
	initInput: function () {
		var that = this;
		
		var coverUrl = that.model.attributes.coverUrl;
		
		if(typeof coverUrl !='undefined' && coverUrl!= ''){
			var img = $('<img>');
			img.attr('src', coverUrl);   
			$("#id_cover").parent().before(img);
			$("#id_btnRemoveCover").show();
		}

		// Add spacebar, enter and click to browse button, to trigger file upload
		that.setBrowseButtonTrigger();

		$('#id_cover').fileupload({
            url: '/personalizeHome/upload/',
            dataType: 'json',
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            timeout:60000,
            autoUpload: false,
            add: function (e, data) {
            	if (data.files[0].size > 5000000) { // 5mb
        			  $.gritter.add({
    					title : gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
    					text : gettext('ADMIN-HOME-SECTION-MAXSIZE-TEXT'),
    					image : '/static/workspace/images/common/ic_validationError32.png',
    					sticky : false,
    					time : 3000
        			  });
                  }
              	else {
              		that.files.splice(0,1,data);
                	that.handleFile(data.files)
                    return false;
              	}
            	                
            },
            done: function (e, data) {
	            /* We replace the label for the img src, because we can now display img src due it is
	             *an external source
	            */
	            	if (window.FileReader === undefined) {	            	
	            		$("#id_cover").parent().parent().find('label').remove()
	            		$("#id_cover").parent().before("<img src="+data.result['url']+" alt=\"\"class=\"FL\"/>");
	            	}    	
	            	
            	that.model.set('coverUrl',data.result['url']);
            	
            },
            
            sequentialUploads: true,
            multipart: true,
          
        }).bind('fileuploadstart', function (e) {$("#ajax_loading_overlay").show();})
          .bind('fileuploadstop', function (e) {$("#ajax_loading_overlay").hide();})
          .bind('fileuploadfail', function (e, data) {	
			  if(data.errorThrown == "timeout"){
				  $.gritter.add({
						title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
						text : gettext('ADMIN-HOME-SECTION-TIMEOUTERROR-TEXT'),
						image : '/static/workspace/images/common/ic_validationError32.png',
						sticky : false,
						time : 3000
					});
			  }
			  else{
				  $.gritter.add({
						title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
						text : gettext('ADMIN-HOME-SECTION-ERROR-TEXT'),
						image : '/static/workspace/images/common/ic_validationError32.png',
						sticky : false,
						time : 3000
					});  
			  }
			  
		  });
        
     
        
	},
	
	handleFile:function (files) {
		var img;
		for (var i = 0; i < files.length; i++) {
			var file = files[i];
			/*
			 * This code checks if browser has filereadar, and if it doesn't (IE <10) it will display
			 * a label with filename
			 * */
			var imageField = $("#id_cover").parent().parent().find('img') 
			if (window.FileReader) {
				if (!imageField.length>0) {
					img = document.createElement("img");
					$("#id_btnRemoveCover").show();
					
				}else{
					
					img = imageField[0]
				}
				img.classList.add("obj");
				img.file = file;
				$('#id_cover').parent().before(img);    				    
				var reader = new FileReader();
				reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
				reader.readAsDataURL(file);

			} else {				
				var labelField  = $("#id_cover").parent().parent().find('label')
				$("#id_btnRemoveCover").show();
				if (imageField.length>0) {
					$(imageField.remove())
					labelField = $("<label>").text(file.name);
				}
				else{
					
					if (labelField.length>0) {
						$(labelField).text(file.name)
					}
					else{
						labelField = $("<label>").text(file.name);
					}
				}
				
				$('#id_cover').parent().before(labelField);
			}
		}
	},

	setBrowseButtonTrigger: function(){

		$('.imageComponent .crop button').off("keypress").on("keypress", function(e) {
			if ( e.which == 32 || e.which == 13 ) { // spacebar or enter
				e.preventDefault();
				$(this).parent().find('input[type=file]').trigger("click");
			}
		}).on("click", function(e){
			e.preventDefault();

			// Esto triggerea un comportamiento erroneo en todos los campos input. Les hace abrir una ventana de subir archivo.
			//$(this).parent().find('input[type=file]').trigger("click");
			
		});

	},

	initSliderSection: function(){
		var initialResources = [];
		var sources = [];
		var resourceQuery='';
		_.each(this.model.attributes.sliderSection, function(item, index){
			resourceType=item.type;
            resourceQuery += item.id+",";
		});		

        // TODO (ignacio feijoo): Por favor, revisar porque no hay un sliderSection
        // en una cuenta recien creada
        // this.model.attributes.sliderSection = Array[0]
        if (typeof resourceType == 'undefined'){
            resourceType="source";
        }
		$.when(
                    
				$.ajax({
					url: "/admin/suggest",
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					data: {ids: resourceQuery, resources:["ds","vz"]},				
				})).done( function(data){
					$('#id_theme4nameSuggest').taggingSources({
						source:function(request, response) {
						    $.getJSON("/admin/suggest", { term: request.term, resources:['ds', 'vz']}, response);
						}
						, minLength: 3
						, sources: data
						, sourceContainer:'<div id=\"id_slider_container\" class=\"tagsContent\"></div>'
					});
				});
	},

	setSliderSection: function(){
	
		var resourceList = [];		
		var $lTags = $('[id*=id_tag][id$=_name]', '#id_slider_container .tagsContent' );
		var $lSources = $('#id_slider_container .tag');
	    var lData = '';
	    $lSources.each(function(i){
	    	var $lSource = $(this).find('.tagTxt');
	    	lData = $lSource.attr("id").split("_");
	        var id = lData[0];
	        var type = lData[1];
	        var obj = {
	                id: id,
	                type: type	                
	        };
	        resourceList.push(obj);	
	    });	    
		this.model.set('sliderSection', resourceList);
	},
	initLinkSection: function(){
		var initialResources = [];
		var sources = [];
		var resourceQuery='';
		_.each(this.model.attributes.linkSection, function(item, index){
			resourceQuery += item.id+",";
			resourceType= item.type;
		});		
		$.when(
				$.ajax({
					url: "/admin/suggest",
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					data: {ids: resourceQuery, resources:["ds","vz"]},				
				})).done( function(data){
					$('#id_theme4nameLinkSuggest').taggingSources({
						source:function(request, response) {
						    $.getJSON("/admin/suggest", { term: request.term.concat("*"), resources:['ds','vz']}, response);
						}
						, minLength: 3
						, sources: data
						, sourceContainer:'<div id=\"id_link_container\" class=\"tagsContent\"></div>'
					});
				});
	},
	setLinkSection: function(){
	
		var resourceList = [];		
		var $lTags = $('[id*=id_tag][id$=_name]', '#id_link_container .tagsContent' );
		var $lSources = $('#id_link_container .tag');
	    var lData = '';
	    $lSources.each(function(i){
	    	var $lSource = $(this).find('.tagTxt');
	    	lData = $lSource.attr("id").split("_");
	        var id = lData[0];
	        var type = lData[1];
	        var obj = {
	                id: id,
	                type: type	                
	        };
	        resourceList.push(obj);	
	    });	    
		this.model.set('linkSection', resourceList);		
	},
	removeCover: function(){
		if(this.model.get('coverUrl')!= undefined){		
			this.model.set('coverUrl', undefined);
		}
		var deleteBtn = $("#id_btnRemoveCover")
		var imageField = deleteBtn.parent().parent().find('img')
		
		if (false) {
			imageField.remove();
		}
		else{
			var labelField  = deleteBtn.parent().find('label')
			if (imageField.length>0) {
				imageField.remove()				
			}
			else{
				if (labelField.length>0) {
					labelField.remove();
				}				
			}
		}		
		deleteBtn.hide();
	},
	save: function(event){		
		that = this;
		if(that.files.length>0){
			$.when($("#id_cover").fileupload('send', {fileInput: that.files[0].fileInput ,files: that.files[0].files})).then(function(){
				that.files = [];
				that.savePreference(event);
			})			
											
		}		
		else{
			this.savePreference(event);
		}
		
	},

	savePreference: function(event){
	  if(this.model.isValid(true)){
		this.setSliderSection();
		this.setLinkSection();
		var btn_id = $(event.currentTarget).attr("id")
		var ob={};
		if (btn_id === 'id_save' || btn_id === 'id_save_top') {
			this.currentModel.attributes.config = this.model.toJSON();
			this.currentModel.attributes.themeID = '4';
			ob['config'] = this.currentModel.attributes.config;
			ob['theme'] = this.currentModel.attributes.themeID;
			ob['type'] = 'save';
		} else {
			ob['config'] = this.model.toJSON();
			ob['theme'] = '4';
			ob['type'] = 'preview';
		}
		$.ajax({
			type: 'POST',
			data: {
				'jsonString': saferStringify(ob)
			}, 
			dataType: 'json',
			beforeSend: function(xhr, settings){

				// call global beforeSend func
				$.ajaxSettings.beforeSend(xhr, settings);
				
				$("#ajax_loading_overlay").show();
			},
			success: function(response) {
				$("#ajax_loading_overlay").hide();
				if(btn_id==="id_save" || btn_id === 'id_save_top'){
					$.gritter.add({
						title : gettext('ADMIN-HOME-SECTION-SUCCESS-TITLE'),
						text : gettext('ADMIN-HOME-SECTION-SUCCESS-TEXT'),
						image : '/static/workspace/images/common/ic_validationOk32.png',
						sticky : false,
						time : 3500
					});
				}
				else{
					event.preventDefault();
					var preview_home = response['preview_home']						
					window.open( preview_home,'','width=1024,height=500,resizable=yes,scrollbars=yes');
				}
			},
			error: function(response) {
				$("#ajax_loading_overlay").hide();
				//jQuery.TwitterMessage({type: 'error', message: response.messages.join('. ')});
				$.gritter.add({
					title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
					text : gettext('ADMIN-HOME-SECTION-ERROR-TEXT'),
					image : '/static/workspace/images/common/ic_validationError32.png',
					sticky : true,
					time : ''
				});
			},
			url: '/personalizeHome/save/'
		});	
	  }
	}

});
