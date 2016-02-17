var theme8View = Backbone.Epoxy.View.extend({

	el: '#id_themeForm',

	buttonFiles: [],
	buttonsCont: 0,

	template: null,
 
	events:{
		"click #id_new_button": "addButtonsInput",
		"click #links_section tr .remove" : "removeRow"
	},

	initialize: function(options){

		// Inint options
		this.currentView = options.currentView;
		this.currentModel = options.currentModel;

		this.currentView.helpAndTips('show');
		that = this;
		this.template = _.template( $("#id_theme8Template").html() );
		this.initSliderSection();
		this.render();
		this.initButtonSection();
		this.colorPicker();		
	},

	render: function(){
		this.$el.html(this.template(this.model.attributes));	
		return this;
	},

	createAddTemplateImageInputRow: function(intId, inputId, section) {
		var categoryText = gettext('ADMIN-HOME-SECTION-CATEGORY-TO-OPEN-TEXT');
		var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
		var titleLabelText = gettext('ADMIN-HOME-SECTION-TITLE-LABEL');
		var titlePlaceHolderText = gettext('ADMIN-HOME-SECTION-TITLE-TEXT');
		var descriptionLabelText = gettext('APP-DESCRIPTION2-LABEL');
		var descriptionPlaceHolderText = gettext('APP-DESCRIPTION2-TEXT');
		var colorLabelText = gettext('ADMIN-HOME-SECTION-MOUSEOVER-BACKGROUND-TEXT');
		var buttonText = gettext('ADMIN-HOME-SECTION-BUTTONTEXT');
		var html = 
			'<tr class=\"template-upload fade\" id=\"row' + intId + '\">' +
				'<td>' +
					'<div class=\"clearfix\">' +

						'<div class=\"FL clearfix\">' +
							'<div class=\"crop relative clearfix FL\">' +
								'<button class=\"button small\">' + buttonText + '</button>' +
								'<input type=\"file\" id=\"' + inputId + '\" class=\"file FL\" tabindex=\"-1\"/>' +
							'</div>' +
						'</div>' +

						'<div class=\"FR\">' +
							'<input type=\"button\" id=\"del_' + section + intId + '\" class=\"remove FL\" value=\"' + deleteText + '\"/>' +
						'</div>' +
						
						'<div class=\"FR sliderData\">' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"title_' + section + intId + '\" class=\"FL\">' + titleLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"title_' + section + intId + '\" name=\"title_' + section + intId + '\" class=\"field FL requiredText\" placeholder=\"' + titlePlaceHolderText + '\" maxlength="55" />' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"description_' + section + intId + '\" class=\"FL\">' + descriptionLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"description_' + section + intId + '\" name=\"description_' + section + intId + '\" class=\"field FL requiredText\" placeholder=\"' + descriptionPlaceHolderText + '\" maxlength="150" />' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"category_' + intId + '\"class=\"FL\">' + categoryText + ':</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<select id=\"category_' + section + intId + '\" class=\"field category\">' +
									'</select>' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"background_color_' + section + intId + '\" class=\"FL\">' + colorLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<div id=\"background_color_' + section + intId + '\" class="colorPicker"><div></div></div>' +
										'<input type=\"hidden\" id=\"background_color_' + section + intId + '\" name=\"background_color_' + section + intId + '\" class=\"field FL requiredText\" />' +
									'</div>' +
								'</div>' +
							'</div>' +

						'</div>' +

					'</div>' +
				'</td>' +
			'</tr>';
		return html;
	},

	createSavedTemplateImageInputRow: function(rowIndex, item, inputId, section) {
		var categoryText = gettext('ADMIN-HOME-SECTION-CATEGORY-TO-OPEN-TEXT');
		var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
		var titleLabelText = gettext('ADMIN-HOME-SECTION-TITLE-LABEL');
		var titlePlaceHolderText = gettext('ADMIN-HOME-SECTION-TITLE-TEXT');
		var descriptionLabelText = gettext('APP-DESCRIPTION2-LABEL');
		var descriptionPlaceHolderText = gettext('APP-DESCRIPTION2-TEXT');
		var placeholderText = gettext('ADMIN-HOME-SECTION-LINKPLACEHOLDER');
		var colorLabelText = gettext('ADMIN-HOME-SECTION-MOUSEOVER-BACKGROUND-TEXT');
		var buttonText = gettext('ADMIN-HOME-SECTION-BUTTONTEXT');

		var html = 
			'<tr class=\"template-upload fade\" id=\"row' + rowIndex + '\">' +
				'<td class=\"draggableSection\"><i class=\"arrangeIcon\"></i></td>' +
				'<td>' +
					'<div class=\"clearfix\">' +

						'<div class=\"FL clearfix\">' +
							'<img src=\"' + item.image + '\" alt=\"\" class=\"FL\"/>' +
							'<div class=\"crop relative clearfix FL\">' +
								'<button class=\"button small\">' + buttonText + '</button>' +
								'<input type=\"file\" id=\"' + inputId + '\" class=\"file FL\" tabindex=\"-1\"/>' +
							'</div>' +
						'</div>' +

						'<div class=\"FR\">' +
							'<input type=\"button\" id=\"del_' + section + rowIndex + '\" class=\"remove FL\" value=\"' + deleteText + '\"/>' +
						'</div>' +

						'<div class=\"FR sliderData\">' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"title_' + section + rowIndex + '\" class=\"FL\">' + titleLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"title_' + section + rowIndex + '\" value=\"' + item.title + '\" name=\"title_' + section + rowIndex + '\" class=\"field FL requiredText\" placeholder=\"' + titlePlaceHolderText + '\" maxlength="55" />' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"description_' + section + rowIndex + '\" class=\"FL\">' + descriptionLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"description_' + section + rowIndex + '\" value=\"' + item.description + '\" name=\"description_' + section + rowIndex + '\" class=\"field FL requiredText\" placeholder=\"' + descriptionPlaceHolderText + '\" maxlength="150" />' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"category_' + rowIndex + '\"class=\"FL\">' + categoryText + ':</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<select id=\"category_' + section + rowIndex + '\" class=\"field category\">' +
									'</select>' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"background_color_' + section + rowIndex + '\" class=\"FL\">' + colorLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<div id=\"background_color_' + section + rowIndex + '\" class="colorPicker"><div></div></div>' +
										'<input type=\"hidden\" id=\"background_color_' + section + rowIndex + '\" value=\"' + item.color + '\" name=\"background_color_' + section + rowIndex + '\" class=\"field FL requiredText\" />' +
									'</div>' +
								'</div>' +
							'</div>' +

						'</div>' +

					'</div>' +
				'</td>' +
			'</tr>';
		return html;
	},

	initButtonSection: function() {
		var that = this;

		_.each(this.model.get('buttonSection'), function(item, index) {

			var intId = that.buttonsCont;
			var inputId = "btn_file_image" + intId;
			var row = that.createSavedTemplateImageInputRow(intId, item, inputId, "button");

			$("#nav_button_table").append(row);
            // load categories
    		$('#id_theme8ButtonStartingCategory option').each(function() {
    		    to_add = $(this).clone();
    		    $op = $("#category_button" + intId).append(to_add);
    		    if (to_add.val() == item.category){
    		        to_add.attr('selected', 'selected');    
		        }
                
            });
			// Add spacebar, enter and click to browse button, to trigger file upload
			that.setBrowseButtonTrigger(intId);

			$("#category_button" + intId).on('change', function() {
				var image = that.model.get('buttonSection')[index];
				image.category = $("#category_button" + intId).val();
				that.model.get('buttonSection').splice(index, 1, image);
				image = null;
			});
			
			$("#title_button" + intId).on('change', function() {
				var image = that.model.get('buttonSection')[index];
				image.title = $("#title_button" + intId).val();
				that.model.get('buttonSection').splice(index, 1, image);
				image = null;
			});
			
			$("#description_button" + intId).on('change', function() {
				var image = that.model.get('buttonSection')[index];
				image.description = $("#description_button" + intId).val();
				that.model.get('buttonSection').splice(index, 1, image);
				image = null;
			});

			// We make the table sortable
			that.setTableSortable($('#nav_button_table'), that.model.get('buttonSection'));

			// When clicked delete button the object is removed from the model

			$("#del_button" + intId).on('click', function() {
				that.model.attributes.buttonSection.splice($('#' + inputId).closest('tr').index(), 1)
				$.each(that.buttonFiles, function(index, item) {
					if (item.input[0].id.indexOf('#' + inputId) >= 0) {
						that.buttonFiles.splice(index, 1)
						return false;
					}
				});

				$(this).closest("tr").remove();

			});

			that.setUploadable($('#' + inputId), "button");
			that.colorPicker($('#row' + intId));
			that.buttonsCont += 1;
		});

	},
	
	addButtonsInput: function() {
		if ($("#nav_button_saved tr").length < 1) {
			var that = this;
			var intId = that.buttonsCont;
			var inputId = "btn_file_image" + intId;
			that.buttonsCont += 1;
			var row = that.createAddTemplateImageInputRow(intId, inputId, "button");
		
			$("#nav_button_saved").append(row);
            // load categories
    		$('#id_theme8ButtonStartingCategory option').each(function() {
                $("#category_button" + intId).append($(this).clone());
            });
			// Add spacebar, enter and click to browse button, to trigger file upload
			this.setBrowseButtonTrigger(intId);

			$("#del_button" + intId).on('click', function() {
				var table = $("#del_button" + intId).closest("table");
				if (table.is("#nav_button_table")) {
					if (($("#nav_button_table tr").length) == that.model.attributes.buttonSection.length) {
						that.model.attributes.buttonSection.splice($('#' + inputId).closest('tr').index(), 1);
					}
					$.each(that.buttonFiles, function(index, item) {
						if (item.input[0].id.indexOf('#' + inputId) >= 0) {
							that.buttonFiles.splice(index, 1)
							return false;
						}
					});
				}
				$(this).closest("tr").remove();
			});
			
			$("#category_button" + intId).on('change', function() {
				var index = $("#category_button" + intId).closest('tr').index();
				if (that.model.attributes.buttonSection.length > index && that.model.attributes.buttonSection[index] != undefined) {
						var image = that.model.get('buttonSection')[index];
						image.category = $("#category_button" + intId).val();
						that.model.get('buttonSection').splice(index, 1, image);
				}
			});
			
			$("#title_button" + intId).on('change', function() {
				var index = $("#title_button" + intId).closest('tr').index();
				if (that.model.attributes.buttonSection.length > index && that.model.attributes.buttonSection[index] != undefined) {
						var image = that.model.get('buttonSection')[index];
						image.title = $("#title_button" + intId).val();
						that.model.get('buttonSection').splice(index, 1, image);
				}
			});

			$("#background_color_button" + intId).on('change', function() {
				var index = $("#background_color_button" + intId).closest('tr').index();
				if (that.model.attributes.buttonSection.length > index && that.model.attributes.buttonSection[index] != undefined) {
						var image = that.model.get('buttonSection')[index];
						image.color = $("#background_color_button" + intId).val();
						that.model.get('buttonSection').splice(index, 1, image);
				}
			});

			that.setUploadable($('#' + inputId), "button");
			that.colorPicker($('#row' + intId));

		} else {
			$('#nav_button_saved tbody td > div.clearfix').addClass('highlight');
			setTimeout("$('#nav_button_saved tbody td > div.clearfix').removeClass('highlight');", 2000);
		}
	},

	setBrowseButtonTrigger: function() {

		$('.imageComponent .crop button').off("keypress").on("keypress", function(e) {
			if (e.which == 32 || e.which == 13) { // spacebar or enter
				e.preventDefault();
				$(this).parent().find('input[type=file]').trigger("click");
			}
		}).on("click", function(e) {
			e.preventDefault();
			$(this).parent().find('input[type=file]').trigger("click");
		});

	},

	setUploadable: function(input, section) {

		input.fileupload({
				url: '/personalizeHome/upload/',
				dataType: 'json',
				timeout: 60000,
				acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
				autoUpload: false,
				add: function(e, data) {
					if (data.files[0].size > 5000000) { // 5mb
						$.gritter.add({
							title: gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
							text: gettext('ADMIN-HOME-SECTION-MAXSIZE-TEXT'),
							image: '/static/workspace/images/common/ic_validationError32.png',
							sticky: false,
							time: 3000
						});
					} else {
						var found = false;
						var files = that.buttonFiles;
						$.each(files, function(index, item) {
							//check the input whose image is going to be uploades is not already in the list
							if (item.input[0].id.indexOf(input[0]) >= 0) {
								item.file = data
								found = true;
								return false;
							}
						});

						if (!found) {
							files.push({
								"input": data.fileInput,
								"file": data.files
							})
						}

						that.handleFiles(data.files, data.fileInput);
					}
				},
				done: function(e, data) {
					/*
					 * After the file was submitted this function is called to set
					 * image attribute in the model and, then trigger save funciton
					 * if it is the last element in the table
					 *
					 **/

					var input = $("#" + data.fileInput[0].id);
						/* We replace the label for the img src, because we can now display img src due it is
						 *an external source
						 */

					if (window.FileReader === undefined) {
						input.parent().parent().find('label').remove()
						input.parent().parent().before("<img src=" + data.result['url'] + " alt=\"\"class=\"FL\"/>");
					}

					var inputRow = input.closest('tr');
					var inputTitle = inputRow.find("input[name^='title']");
					var inputDescription = inputRow.find("input[name^='description']");
					var inputColor = inputRow.find("input[name*='color']");
					var href = '';
					var title = '';
					var description = '';
					var color = '';
					if (typeof inputTitle.val() != 'undefined') {
						title = inputTitle.val();
					}
					if (typeof inputDescription.val() != 'undefined') {
						description = inputDescription.val();
					}
					if (typeof inputColor.val() != 'undefined') {
						color = inputColor.val();
					}
					if (data.fileInput[0].id.indexOf("btn_file_image") >= 0) {
						that.model.get('buttonSection').splice(inputRow.index(), 1, {
							'image': data.result['url'],
							'href': href,
							'title': title,
							'description': description,
							'color': color
						});
					}

				},

				sequentialUploads: true,
				multipart: true,

			}).bind('fileuploadstart', function(e) {
				$("#ajax_loading_overlay").show();
			})
			.bind('fileuploadstop', function(e) {
				$("#ajax_loading_overlay").hide();
			})
			.bind('fileuploadfail', function(e, data) {
				if (data.errorThrown == "timeout") {
					$.gritter.add({
						title: gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
						text: gettext('ADMIN-HOME-SECTION-TIMEOUTERROR-TEXT'),
						image: '/static/workspace/images/common/ic_validationError32.png',
						sticky: false,
						time: 3000
					});
				} else {
					$.gritter.add({
						title: gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
						text: gettext('ADMIN-HOME-SECTION-ERROR-TEXT'),
						image: '/static/workspace/images/common/ic_validationError32.png',
						sticky: false,
						time: 3000
					});
				}

			});
	},

	handleFiles: function(files, event) {
		var input = event[0].id;
		var img;
		for (var i = 0; i < files.length; i++) {
			var file = files[i];
			/*
			 * This code checks if browser has filereadar, and if it doesn't (IE <10) it will display
			 * a label with filename
			 * */
			var imageField = $("#" + input).parent().parent().find('img')
			if (window.FileReader) {
				if (!imageField.length > 0) {
					img = document.createElement("img");
				} else {
					img = imageField[0]
				}
				img.className += " obj";
				img.file = file;
				$("#" + input).parents('.crop').before(img);

				var reader = new FileReader();
				reader.onload = (function(aImg) {
					return function(e) {
						aImg.src = e.target.result;
					};
				})(img);
				reader.readAsDataURL(file);

			} else {
				var labelField = $("#" + input).parent().parent().find('label')
				if (imageField.length > 0) {
					imageField.remove()
					labelField = $("<label>").text(file.name);
				} else {

					if (labelField.length > 0) {
						$(labelField).text(file.name)
					} else {
						labelField = $("<label>").text(file.name);
					}
				}

				$("#" + input).parents('.crop').before(labelField);
			}

			var table = $("#" + input).closest("table");

			// When we choose a file, we remove the input from the image_save
			// table and move it to image_table
			if (table.is("#nav_button_saved")) {
				that.model.get('buttonSection').push("");
				var row = $("#" + input).closest("tr");
				row.detach();

				$("#nav_button_table").append(row);
				var tdSort = '<td class=\"draggableSection\"><i class=\"arrangeIcon\"></i></td>'
				$('#nav_button_table tr:last td:eq(0)').before(tdSort);
				this.setTableSortable($("#nav_button_table"), that.model.get('buttonSection'));
			}
		}

	},

	setTableSortable: function(table, model_element) {
		table.children('tbody').sortable({
			start: function(e, ui) {
				$(this).attr('data-previndex', ui.item.index());
			},
			update: function(e, ui) {
				// We sort the attribute in the model with splice
				var newIndex = ui.item.index();
				var oldIndex = $(this).attr('data-previndex');
				$(this).removeAttr('data-previndex');
				if (model_element != undefined) {
					model_element.splice(newIndex, 0, model_element.splice(oldIndex, 1)[0]);
				}
				table.children('tbody tr').each(function(i, item) {
					var descriptionInput = $(this).find("input[type=text]");
					if (image != undefined && image.description != descriptionInput.val()) {
							image.description = descriptionInput.val();
					}
				});

			}
		});
	},

	calculateButtonRowWidth: function() {
		var that = this;

		var btnsPerRow = $("#id_buttonsPerRow").val();

		// If no value is set, the default value (20) will be set as row width
		if (btnsPerRow) {
			that.model.set('buttonsPerRowWidth', (100 / btnsPerRow).toString() );
		}			

	},

	save: function(event) {
		that = this;

		this.calculateButtonRowWidth();
		
		$.validator.addClassRules("requiredText", {
			required: true,
			minlength: 1
		});

		this.$el.parent().validate({

			rules: {
				id_buttonsPerRow: {
					number: true
				}
			},

			invalidHandler: function(event, validator) {

				var i = 0;
				for (i = 0; i < validator.invalidElements().length; i++) {
					//If the name is id_buttonsPerRow, then we display error message for non numeric
					if ($(validator.invalidElements()[i]).attr('name') == 'id_buttonsPerRow') {
						$.gritter.add({
							title: gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
							text: gettext('ADMIN-HOME-SECTION-NOTVALIDNUM-TEXT'),
							image: '/static/workspace/images/common/ic_validationError32.png',
							sticky: false,
							time: 5000
						});
					} else {

						$.gritter.add({
							title: gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
							text: gettext('ADMIN-HOME-SECTION-EMPTY-TEXT'),
							image: '/static/workspace/images/common/ic_validationError32.png',
							sticky: false,
							time: 5000
						});
					}

				}

			}

		});

		var ajaxReqs = [];
		//We push the request into an array

		_.each(that.buttonFiles, function(item, index) {
			ajaxReqs.push($("#" + item['input'][0].id).fileupload('send', {
				fileInput: item['input'],
				files: item['file']
			}));
		})

			if (that.buttonFiles.length > 0) {
				//We loop through the request, once the all the ajax calls are done, we trigger the save preference
				$.when.apply($, ajaxReqs).then(function() {
					that.saveButtons();
					that.buttonFiles = [];
					that.savePreference(event);
				})
			} else {
				$.when.apply($, ajaxReqs).then(function() {
					that.saveButtons();
					that.savePreference(event);
				});
			}
	},

	saveButtons : function (event) {
		//run through each row
		var buttonSection = this.model.get('buttonSection');
		$('#nav_button_table tr').each(function (i, row) {
			buttonSection[i].title = $(row).find("input[name^='title']").val();
			buttonSection[i].description = $(row).find("input[name^='description']").val();
			buttonSection[i].color = $(row).find("input[name*='color']").val();
			buttonSection[i].category = $(row).find("select[id^='category']").val();
		});
		this.model.set('buttonSection', buttonSection);
	},

	savePreference: function(event){
		this.setSliderSection();

		var btn_id = $(event.currentTarget).attr("id")
		var ob={};
		if (btn_id === 'id_save') {
			this.currentModel.attributes.config = this.model.toJSON();
			this.currentModel.attributes.themeID = '8';
			ob['config'] = this.currentModel.attributes.config;
			ob['theme'] = this.currentModel.attributes.themeID;
			ob['type'] = 'save';
		} else {
			ob['config'] = this.model.toJSON();
			ob['theme'] = '8';
			ob['type'] = 'preview';
		}
		console.log(ob);
		console.log(this.currentModel.attributes);
		$.ajax({
			type: 'POST',
			data: {
				'jsonString': saferStringify(ob)
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {

				// call global beforeSend func
				$.ajaxSettings.beforeSend(xhr, settings);

				$("#ajax_loading_overlay").show();
			},
			success: function(response) {
				$("#ajax_loading_overlay").hide();
				if(btn_id==="id_save"){
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
	},
	
	initSliderSection: function(){
		var initialResources = [];
		var resourceQuery='';
		_.each(this.model.attributes.sliderSection, function(item, index){
            resourceType=item.type;
            resourceQuery += item.id+",";
		});		
		$.when(
			$.ajax({					
				url: "/admin/suggest",
				type: "GET",
				dataType: "json",
				contentType: "application/json; charset=utf-8",
				data: {ids: resourceQuery, resources:['ds','vz']},            
			})).done( function(data){
				$('#id_theme8NameSuggest').taggingSources({
					source:function(request, response) {
						$.getJSON("/admin/suggest", { term: request.term, resources: ['ds','vz']}, response);
					}
					, minLength: 3
					, sources:data							
				});
			});
	},

	setSliderSection: function(){
	
		var resourceList = [];		
		var $lTags = $('[id*=id_tag][id$=_name]', '#id_source_container .tagsContent' );
		var $lSources = $('#id_source_container .tag');
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

	colorPicker: function() {

		var that = this;

	    $('input[type=hidden][name*=_color]').each(function(){
	        var divId = $(this).attr('name');
	        var divBGColor = $(this).val();
	        $('#'+divId+' div').css('background-color', 'rgba(' + divBGColor + ',1)');
	    });

	    $('.colorPicker').ColorPicker({
        
	        onBeforeShow: function() {
	            var bg_color = $(this).children(0).css('background-color');
	            if (bg_color != null) {
	                $(this).ColorPickerSetColor(bg_color);
	            }
	        },
	        onShow: function (colpkr) {
	            $(colpkr).fadeIn(500);
	            return false;
	        },
	        onHide: function (colpkr) {
	            $(colpkr).fadeOut(500);
	            return false;
	        },
	        onChange: function (hsb, hex, rgb) {
	            element = $(this).data('colorpicker').el;
	            $(element).find('div').css('background-color', 'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ',1)');
	            var elementId = $(element).attr('id');
	            $('input[name='+elementId+']').val( rgb.r + ',' + rgb.g + ',' + rgb.b );
	        }

	    });
	}

});
