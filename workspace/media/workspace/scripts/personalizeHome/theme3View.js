var theme3View = Backbone.Epoxy.View.extend({

	el: '#id_themeForm',

	template: null,
	files: [],
	inputCont: 0,
	
	events: {
	    "click #id_new_slide" : "addInput",
	},
	
	initialize: function(options){
		this.currentView = options.currentView;
		this.currentModel = options.currentModel;

		this.currentView.helpAndTips('show');
		that = this;
		this.files = [];
		this.template = _.template( $("#id_theme3Template").html() );		
		this.render();
		this.initCarrouselSection();
	},

	render: function(){
		this.$el.html(this.template(this.model.attributes));
		return this;
	},
	/*
	 * This function will initialize the images input based on the saved
	 * preference
	 */
	initCarrouselSection: function(){
		var that = this;		
		_.each(this.model.get('imageUrlCarrousel'), function(item, index){			
			var intId = that.inputCont;
			var inputId = "image"+intId;
			var linkText = gettext('ADMIN-HOME-SECTION-LINKTEXT');
			var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');	      
			var placeholderText = gettext('ADMIN-HOME-SECTION-LINKPLACEHOLDER');
			var buttonText = gettext('ADMIN-HOME-SECTION-BUTTONTEXT');
			var row = 
					'<tr class=\"template-upload fade\" id=\"row'+intId+'\">' +
						'<td class=\"draggableSection\"><i class=\"arrangeIcon\"></i></td>'+
						'<td>'+
							'<div class=\"clearfix\">'+
								'<div class=\"FL clearfix\">'+
									'<img src=\"'+item.image+'\" alt=\"\" class=\"FL\"/>'+
									'<div class=\"crop relative clearfix FL\">'+
										'<button class=\"absolute button small\">'+buttonText+'</button>'+
										'<input type=\"file\" id=\"'+inputId+'\" class=\"file FL\" tabindex=\"-1\"/>'+
									'</div>'+
								'</div>'+
								'<div class=\"FR\ clearfix">'+
									'<label for=\"link_'+intId+'\" class=\"FL\">'+linkText+'</label>'+
									'<div class=\"formErrorMessageContainer FL\">'+
										'<input type=\"url\" id=\"link_'+intId+'\" value=\"'+item.href+'\" class=\"field FL urlLink complete_url\" placeholder=\"'+placeholderText+'\"/>'+									
									'</div>'+	
									'<input type=\"button\" id=\"btn_'+intId+'\" class=\"remove FL\" value=\"'+deleteText+'\"/>'+
								'</div>'+	
							'</div>'+
						'</td>'+
					'</tr>';	
			
	        $("#image_table").append(row);

	        // Add spacebar, enter and click to browse button, to trigger file upload
					that.setBrowseButtonTrigger(intId);

	        $("#link_"+intId).on('change',function(){
	        	var image = that.model.get('imageUrlCarrousel')[index];
	        	image.href = $("#link_"+intId).val();
	        	that.model.get('imageUrlCarrousel').splice(index,1, image);	        	
	        	image = null;
        	});

	        // We make the table sortable
	        that.setTableSortable();

        
	        // When clicked delete button the object is removed from the model
		
	        $("#btn_"+intId).on('click',function(){
	        	that.model.attributes.imageUrlCarrousel.splice($('#'+inputId).closest('tr').index(),1)
	        	$.each(that.files, function( index, item ) {
            	    if (item.input[0].id.indexOf('#'+inputId) >= 0) {
            	    	that.files.splice(index,1)
            	    	return false; 	        
            	    }
	        	});	        	
	
	        	$(this).closest("tr").remove();
				
			});
	        that.setUploadable('#'+inputId);	        
	        that.inputCont+=1;
		});
		
	},

	setBrowseButtonTrigger: function(intId){

		$('#row'+intId+' .crop button').off("keypress").on("keypress", function(e) {
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

	/*
	 * This function is called when we want to add a new image input. The files
	 * already saved will be stored in image_table, whilst those input that are
	 * created when clicking "add new slide" will be added to image_saved table.
	 * This is done to reduce code complexity when sorting the inputs.
	 */
	addInput: function(){
		if($("#image_saved tr").length<1){
			var that = this;
			var intId= that.inputCont;			
			var inputId = "file-input"+intId;
			that.inputCont+=1;
			var linkText = gettext('ADMIN-HOME-SECTION-LINKTEXT');
			var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
			var placeholderText = gettext('ADMIN-HOME-SECTION-LINKPLACEHOLDER');
			var buttonText = gettext('ADMIN-HOME-SECTION-BUTTONTEXT');
			var row = 
				'<tr class=\"template-upload fade\" id=\"row'+intId+'\">' +					
					'<td>'+
						'<div class=\"clearfix\">'+
							'<div class=\"FL clearfix\">'+
								'<div class=\"crop relative clearfix\">'+
									'<button class=\"absolute button small\">'+buttonText+'</button>'+
									'<input type=\"file\" id=\"'+inputId+'\" class=\"file FL\" tabindex=\"-1\"/>'+
								'</div>'+
							'</div>'+
								'<div class=\"FR\ clearfix">'+
									'<label for=\"link_'+intId+'\"class=\"FL\">'+linkText+'</label>'+
									'<div class=\"formErrorMessageContainer FL\">'+
										'<input type=\"url\" id=\"link_'+intId+'\" class=\"field FL urlLink complete_url\" placeholder=\"'+placeholderText+'\"/>'+
									'</div>'+
									'<input type=\"button\" id=\"btn_'+intId +'\" class=\"remove FL\" value=\"'+deleteText+'\"/>'+
								'</div>'+
							'</div>'+
					'</td>'+
				'</tr>';
			
	    $("#image_saved").append(row);

	    // Add spacebar, enter and click to browse button, to trigger file upload
			this.setBrowseButtonTrigger(intId);


			$("#btn_"+intId).on('click',function(){	
				var table =  $("#btn_"+intId).closest("table");
				if(table.is("#image_table")){
					if(($("#image_table tr").length)==that.model.attributes.imageUrlCarrousel.length){		        	
			        	that.model.attributes.imageUrlCarrousel.splice($('#'+inputId).closest('tr').index(),1);
					}
					$.each(that.files, function( index, item ) {
						if (item.input[0].id.indexOf('#'+inputId) >= 0) {
							that.files.splice(index,1)
							return false;            	        
						}
					});	       
				}			
				$(this).closest("tr").remove();
			});
	        $("#link_"+intId).on('change',function(){
	        	var index = $("#link_"+intId).closest('tr').index();
	        	if(that.model.attributes.imageUrlCarrousel.length>index && that.model.attributes.imageUrlCarrousel[index]!= undefined){
	        		var image = that.model.get('imageUrlCarrousel')[index];
		        	image.href = $("#link_"+intId).val();
		        	that.model.get('imageUrlCarrousel').splice(index,1, image);		        	
	        	}
	    	});        
	        
	        that.setUploadable('#'+inputId);
		}
		else{
			$('#image_saved tbody td > div.clearfix').addClass('highlight');
			setTimeout( "$('#image_saved tbody td > div.clearfix').removeClass('highlight');",2000 );
		}
	},
	handleFiles:function (files, event) {		
		var input = event[0].id
		var img
		for (var i = 0; i < files.length; i++) {			
			var file = files[i];
			/*
			 * This code checks if browser has filereadar, and if it doesn't (IE <10) it will display
			 * a label with filename
			 * */
			var imageField = $("#"+input).parent().parent().find('img') 
			if (window.FileReader) {				
			    if (!imageField.length>0) {     
				      img = document.createElement("img");
				    }
				    else{
				      img = imageField[0]
				    }
			    	img.className += " obj";
				    img.file = file;
				    $("#"+input).parents('.crop').before(img);
				    
				    var reader = new FileReader();
				    reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
				    reader.readAsDataURL(file);

			} else {				
				var labelField  = $("#"+input).parent().parent().find('label')
				if (imageField.length>0) {
					imageField.remove()
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
				
				$("#"+input).parents('.crop').before(labelField);				
			}
			
		    var table =  $("#"+input).closest("table");		    
		    
		    // When we choose a file, we remove the input from the image_save
			// table and move it to image_table
		    if(table.is("#image_saved"))
		    {
		    	that.model.get('imageUrlCarrousel').push("");
		    	var row = $("#"+input).closest("tr");		    			    	
			    row.detach();		
			    
			    $("#image_table").append(row);
			    var tdSort = '<td class=\"draggableSection\"><i class=\"arrangeIcon\"></i></td>'
			    $('#image_table tr:last td:eq(0)').before(tdSort);
			    this.setTableSortable();
			 }
		   } 
	},

	validateUrl: function(){

		$('.complete_url').validate({
			rules: {
				complete_url:true
			}
		});  
   
	},
	
	setUploadable: function(input){
		
		$(input).fileupload({
            url: '/personalizeHome/upload/',
            dataType: 'json',
            timeout:60000,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
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
            		var found = false;            	
            		$.each(that.files, function( index, item ) {
            			//check the input whose image is going to be uploades is not already in the list
            			if (item.input[0].id.indexOf(input) >= 0) {
            				item.file = data
            				found = true;
            				return false; 	        
            			}            	   
            		});	 
 
            		if (!found) {
            			that.files.push({"input":data.fileInput, "file": data.files})
            		}
            		
            		that.handleFiles(data.files, data.fileInput)
            	}
            },
            done: function (e, data) {
            	/*
				 * After the file was submitted this function is called to set
				 * image attribute in the model and, then trigger save funciton
				 * if it is the last element in the table
				 *
				 **/

            	var input = $("#"+data.fileInput[0].id)
	            /* We replace the label for the img src, because we can now display img src due it is
	             *an external source
	            */
	            if (window.FileReader === undefined) {	
	            	input.parent().parent().find('label').remove()
	            	input.parent().parent().before("<img src="+data.result['url']+" alt=\"\"class=\"FL\"/>");
	            }    	
	            	
	            var inputRow = input.closest('tr');
	            var inputUrl = inputRow.find("input[type=url]");
	            var href ='';
	            if(typeof inputUrl.val()!= 'undefined'){ href= inputUrl.val(); }
	            that.model.get('imageUrlCarrousel').splice(inputRow.index(),1,{'image': data.result['url'],'href':href});				 
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
	setTableSortable: function(){
		$("#image_table tbody").sortable({
        	start: function(e, ui) {
        		$(this).attr('data-previndex', ui.item.index());
        	},
        	update: function(e, ui) {
        		// We sort the attribute in the model with splice
        		var newIndex = ui.item.index();
        	    var oldIndex = $(this).attr('data-previndex');
        	    $(this).removeAttr('data-previndex');	        	    
        	    that.model.get('imageUrlCarrousel').splice(newIndex, 0, that.model.get('imageUrlCarrousel').splice(oldIndex, 1)[0]);
        		
        	    
        	    $("#image_table tbody tr").each(function(i, item) {
        			var urlInput = $(this).find("input[type=url]");
	        	    var image = that.model.get('imageUrlCarrousel')[i];
		        	if(image!= undefined && image.href != urlInput.val()){
		        		image.href = urlInput.val();
		        	}
        		});	

        	}	        
        });		
	},
	save: function(event){		
		that = this;
		if($('.complete_url').length > 0){
			// set validate URL
			this.validateUrl();

			if( $(".complete_url").valid() ){
				var ajaxReqs = [];
				//We push the request into an array
				_.each(that.files, function(item, index){				
					ajaxReqs.push($("#"+item['input'][0].id).fileupload('send', {fileInput: item['input'],files: item['file']}));
				})

				if(that.files.length>0){
					//We loop through the request, once the all the ajax calls are done, we trigger the save preference
					$.when.apply($, ajaxReqs).then(function() {
						that.files = [];
						that.savePreference(event);
					})											
				}		
				else{
					this.savePreference(event);
				}		
			}else{
				$.gritter.add({
					title : gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
					text : gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TEXT'),
					image : '/static/workspace/images/common/ic_validationError32.png',
					sticky : false,
					time : 5000
				});
			}
		}
		
		else{
			this.savePreference(event);
		}	
	},
	
	savePreference: function(event){
			var btn_id = $(event.currentTarget).attr("id")
			var ob={};			
			if (btn_id === 'id_save' || btn_id === 'id_save_top') {
				this.currentModel.attributes.config = this.model.toJSON();
				this.currentModel.attributes.themeID = '3';
				ob['config'] = this.currentModel.attributes.config;
				ob['theme'] = this.currentModel.attributes.themeID;
				ob['type'] = 'save';
			} else {
				ob['config'] = this.model.toJSON();
				ob['theme'] = '3';
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
						window.open( preview_home,'','width=1024,height=500,resizable=yes,scrollbars=yes' );
					}
					
				},
				error: function(response) {
					$("#ajax_loading_overlay").hide();
					$.gritter.add({
						title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
						text : gettext('ADMIN-HOME-SECTION-ERROR-TEXT'),
						image : '/static/workspace/images/common/ic_validationError32.png',
						sticky : true,
						time : 3000
					});
				},
				url: '/personalizeHome/save/'
			});

		
	}

});